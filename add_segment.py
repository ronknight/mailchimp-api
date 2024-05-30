import os
import json
import datetime
import argparse
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError
from dotenv import load_dotenv

# Ensure logs directory exists
os.makedirs('logs', exist_ok=True)

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("API_KEY")
SERVER_PREFIX = os.getenv("SERVER_PREFIX")
LIST_ID = os.getenv("AUDIENCE_ID")

if not API_KEY or not SERVER_PREFIX or not LIST_ID:
    raise ValueError("API_KEY, SERVER_PREFIX, and LIST_ID must be set in the .env file")

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Append a letter to the segment name and condition value.')
parser.add_argument('letter', help='Letter to append to the segment name and condition value')
args = parser.parse_args()

try:
    client = Client()
    client.set_config({
        "api_key": API_KEY,
        "server": SERVER_PREFIX
    })

    segment_data = {
        "name": f"NL-Batch1-A-B-{args.letter}",
        "options": {
            "match": "all",
            "conditions": [
                {
                    "condition_type": "TextMerge",
                    "field": "SRC",
                    "op": "is",
                    "value": "NL-Batch1-A-B"
                },
                {
                    "condition_type": "EmailAddress",
                    "field": "EMAIL",
                    "op": "starts",
                    "value": args.letter
                }
            ]
        }
    }

    # Log the request data
    request_log_path = 'logs/add_segment_request.json'
    with open(request_log_path, 'a') as request_log_file:
        json.dump(segment_data, request_log_file, indent=4)
        request_log_file.write('\n')

    response = client.lists.create_segment(LIST_ID, segment_data)
    print(response)

    # Log the response data with a timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    response_log_path = f'logs/add_segment_response_{timestamp}.json'
    with open(response_log_path, 'w') as response_log_file:
        json.dump(response, response_log_file, indent=4)

except ApiClientError as error:
    print("Error: {}".format(error.text))
    # Log the error data with a timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    error_log_path = f'logs/add_segment_error_{timestamp}.json'
    with open(error_log_path, 'w') as error_log_file:
        json.dump({"error": error.text}, error_log_file, indent=4)
