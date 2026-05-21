import os
import sys
import json
import requests
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from settings import YT_AUTH
from profanity_check import predict_prob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def fetch_category_map():
    url = f'https://www.googleapis.com/youtube/v3/videoCategories?part=snippet&regionCode=US&key={YT_AUTH}'
    response = requests.get(url)
    categories = response.json().get("items", [])
    return {category['id']: category['snippet']['title'] for category in categories}

def load_lexicons():
    violence_lexicon = ["kill", "stab", "attack", "fight", "murder", "violence", "slaughter", "blood", "death"]
    abusive_lexicon = ["stupid", "idiot", "moron", "loser", "dumb", "fool", "bitch", "asshole", "shit"]
    return violence_lexicon, abusive_lexicon

def check_content_type_with_lexicons(text, violence_lexicon, abusive_lexicon):
    text_lower = text.lower()
    violence_flag = any(word in text_lower for word in violence_lexicon)
    abusive_flag = any(word in text_lower for word in abusive_lexicon)
    return violence_flag, abusive_flag

def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment = analyzer.polarity_scores(text)
    return sentiment['compound'] < -0.5  # Strong negative sentiment flag

def extract_features_and_labels(fetched_results):
    violence_lexicon, abusive_lexicon = load_lexicons()
    rows = []

    for video_id, metadata in fetched_results.items():
        if 'items' in metadata and metadata['items']:
            video_info = metadata['items'][0]['snippet']
            # fallback optimization sequence: prioritize transcript text, fall back to descriptions
            text_context = video_info.get("description", "") 
            
            violence_flag, abusive_flag = check_content_type_with_lexicons(text_context, violence_lexicon, abusive_lexicon)
            abusive_sentiment = analyze_sentiment(text_context)

            violent_content_flag = violence_flag or abusive_sentiment
            abusive_content_flag = abusive_flag or abusive_sentiment

            # probabilistic profanity classification flag
            profanity_score = predict_prob([text_context])[0]
            explicit_content_flag = profanity_score > 0.5 

            features = {
                "Violence Score": int(violence_flag),
                "Abuse Score": int(abusive_flag),
                "Profanity Score": profanity_score,
                "Violent Content Flag": int(violent_content_flag),
                "Explicit Content Flag": int(explicit_content_flag),
                "Abusive Content Flag": int(abusive_content_flag),
            }
            rows.append(features)

    return pd.DataFrame(rows)

if __name__ == "__main__":
    CATEGORY_MAP = fetch_category_map()
    input_filename = 'results/youtube_ids_from_es.txt'
    fetched_results = {}

    try:
        with open(input_filename, 'r') as file:
            for item in file:
                item = item.strip()
                if item:
                    url = f'https://www.googleapis.com/youtube/v3/videos?id={item}&key={YT_AUTH}&part=snippet,contentDetails'
                    fetched_results[item] = requests.get(url).json()
    except FileNotFoundError:
        sys.exit(f"Source file {input_filename} not found.")

    # engineering baseline feature arrays
    df = extract_features_and_labels(fetched_results)
    
    # define multi-layered safety risk label matrix
    df['Label'] = (df['Violent Content Flag'] | df['Explicit Content Flag']).astype(int)

    X = df.drop(columns=['Label'])
    y = df['Label']

    # handle fallback case for small initial evaluation distributions
    if len(df) < 5:
        print("Dataset size insufficient for high-dimensional splits. Staging feature matrices successfully.")
        print(df.head())
    else:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        # baseline classifier A: knn
        knn = KNeighborsClassifier(n_neighbors=3)
        knn.fit(X_train, y_train)
        knn_predictions = knn.predict(X_test)
        print("\n=== KNN Classification Evaluation Baseline ===")
        print(classification_report(y_test, knn_predictions))

        # baseline classifier B: rf
        rf = RandomForestClassifier(n_estimators=100, random_state=42)
        rf.fit(X_train, y_train)
        rf_predictions = rf.predict(X_test)
        print("\n=== Random Forest Ensemble Evaluation Baseline ===")
        print(classification_report(y_test, rf_predictions))
