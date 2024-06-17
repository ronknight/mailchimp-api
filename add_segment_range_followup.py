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

# Retrieve API key, server prefix, and list ID from environment variables
API_KEY = os.getenv("API_KEY")
SERVER_PREFIX = os.getenv("SERVER_PREFIX")
LIST_ID = os.getenv("AUDIENCE_ID")

# Ensure API_KEY, SERVER_PREFIX, and LIST_ID are provided
if not API_KEY or not SERVER_PREFIX or not LIST_ID:
    raise ValueError("API_KEY, SERVER_PREFIX, and LIST_ID must be set in the .env file")

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Append a letter to the segment name and condition value.')
parser.add_argument('batch_name', help='Base name of the segment')
parser.add_argument('greater', help='Starting character to append to the segment name and condition value')
parser.add_argument('less', help='Ending character to append to the segment name and condition value')
parser.add_argument('part', help='Chunk name to append to the segment name and condition value')

args = parser.parse_args()

try:
    # Initialize Mailchimp client
    client = Client()
    client.set_config({
        "api_key": API_KEY,
        "server": SERVER_PREFIX
    })

    # Prepare segment data with the provided letters
    segment_data = {
        "name": f"{args.batch_name}_{args.part}",  # Append part to the segment name
        "options": {
            "match": "all",
            "conditions": [
                {
                    "condition_type": "TextMerge",
                    "field": "SRC",
                    "op": "is",
                    "value": args.batch_name  # batch name
                },
                {
                    "condition_type": "EmailAddress",
                    "field": "EMAIL",
                    "op": "greater",
                    "value": args.greater  # Append the starting character to the condition value
                },
                {
                    "condition_type": "EmailAddress",
                    "field": "EMAIL",
                    "op": "less",
                    "value": args.less  # Append the ending character to the condition value
                }
            ]
        }
    }

    # Log the request data
    request_log_path = 'logs/add_segment_range_request.json'
    with open(request_log_path, 'a') as request_log_file:
        json.dump(segment_data, request_log_file, indent=4)
        request_log_file.write('\n')

    # Create the segment in Mailchimp
    response = client.lists.create_segment(LIST_ID, segment_data)
    print(response)

    # Log the response data with a timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    response_log_path = f'logs/add_segment_range_response_{timestamp}.json'
    with open(response_log_path, 'w') as response_log_file:
        json.dump(response, response_log_file, indent=4)

except ApiClientError as error:
    # Handle API client errors
    print("Error: {}".format(error.text))
    
    # Log the error data with a timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    error_log_path = f'logs/add_segment_range_error_{timestamp}.json'
    with open(error_log_path, 'w') as error_log_file:
        json.dump({"error": error.text}, error_log_file, indent=4)
