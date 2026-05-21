import sys
import os
from elasticsearch import Elasticsearch
from urllib import parse

# initialize Elasticsearch client securely using env variables
ES_PASSWORD = os.getenv("ES_PASSWORD", "SECURE_PASSWORD_PLACEHOLDER")

es = Elasticsearch(
    ["https://localhost:9200"],  # target ES server proxy log cluster
    ca_certs="config/certs/http_ca.crt",
    verify_certs=True,
    basic_auth=('elastic', ES_PASSWORD),
    request_timeout=60
)

es_index = "postman_logs_v3"

try:
    if es.ping():
        print("Connected to Elasticsearch successfully.")
    else:
        print("Could not connect to Elasticsearch cluster.")
except Exception as error:
    print(f"Connection failed: {error}")

def retrieve_youtube_ids(index_name):
    """
    queries Elasticsearch to isolate captured network traffic logs
    containing explicit YouTube video identifiers.
    """
    query = {
        "_source": ["youtube_video_id"],
        "size": 1000,
        "query": {
            "exists": {"field": "youtube_video_id"}
        }
    }

    result = es.search(index=index_name, body=query)
    ids = [hit['_source']['youtube_video_id'] for hit in result['hits']['hits']]
    return ids

if __name__ == "__main__":
    youtube_ids = retrieve_youtube_ids(es_index)

    # output directory configured relative to the project structure
    os.makedirs('results', exist_ok=True)
    output_file = 'results/youtube_ids_from_es.txt'
    
    with open(output_file, 'w') as file:
        for video_id in youtube_ids:
            file.write(f"{video_id}\n")

    print(f"Pipeline Step 1 Complete: Saved {len(youtube_ids)} YouTube IDs to {output_file}")
