import os
import sys
import json
import datetime
import requests
import pandas as pd
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from YT_API_KEY import YT_AUTH  # centralized API authentication module

def fetch_category_map():
    """retrieves and maps numerical YT category ids to text labels"""
    url = f'https://www.googleapis.com/youtube/v3/videoCategories?part=snippet&regionCode=US&key={YT_AUTH}'
    response = requests.get(url)
    categories = response.json().get("items", [])
    return {category['id']: category['snippet']['title'] for category in categories}

# initialize category mapping layer
CATEGORY_MAP = fetch_category_map()

def fetch_transcript(video_id):
    """
    defensive extraction logic to retrieve video closed-captions
    handles videos with disabled or unavailable transcripts without stalling pipeline
    """
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = " ".join([entry['text'] for entry in transcript])
        return full_text
    except (TranscriptsDisabled, NoTranscriptFound):
        return "Transcript not available"

if __name__ == "__main__":
    video_id_list = 'results/youtube_ids_from_es.txt'
    fetched_results = {}

    try:
        with open(video_id_list, 'r') as file:
            for item in file:
                item = item.strip()
                if item:
                    url = f'https://www.googleapis.com/youtube/v3/videos?id={item}&key={YT_AUTH}&part=snippet'
                    video_metadata = requests.get(url).json()
                    transcript_text = fetch_transcript(item)
                    fetched_results[item] = {
                        "metadata": video_metadata,
                        "transcript": transcript_text
                    }
    except FileNotFoundError:
        sys.exit(f"Source file {video_id_list} not found. Ensure Step 1 extraction ran successfully.")

    # save JSON raw data dump
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    json_output_file = f'results/video_details_created_at_{timestamp}.json'
    with open(json_output_file, 'w') as file:
        json.dump(fetched_results, file)

    #parse and structure fields for structured evaluation datasets
    rows = []
    for video_id, data in fetched_results.items():
        items = data.get("metadata", {}).get("items", [])
        if not items:
            continue
        
        video_metadata = items[0].get("snippet", {})
        transcript_text = data.get("transcript", "")
        category_id = video_metadata.get("categoryId")
        category_label = CATEGORY_MAP.get(category_id, "Unknown")

        rows.append({
            "Video ID": video_id,
            "Title": video_metadata.get("title"),
            "Description": video_metadata.get("description"),
            "Published At": video_metadata.get("publishedAt"),
            "Channel Title": video_metadata.get("channelTitle"),
            "Tags": ", ".join(video_metadata.get("tags", [])),
            "Category ID": category_id,
            "Category Label": category_label,
            "Default Audio Language": video_metadata.get("defaultAudioLanguage"),
            "Transcript": transcript_text,
        })

    # save structured matrix for down-stream modeling layers
    df = pd.DataFrame(rows)
    excel_output_filename = 'results/video_information_with_transcripts.xlsx'
    df.to_excel(excel_output_filename, index=False)

    print(f"Pipeline Step 2 Complete: Saved enriched records to {excel_output_filename}")
