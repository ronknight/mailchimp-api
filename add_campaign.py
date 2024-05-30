import os
import json
import datetime
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("API_KEY")
SERVER_PREFIX = os.getenv("SERVER_PREFIX")
LIST_ID = os.getenv("AUDIENCE_ID")

if not API_KEY or not SERVER_PREFIX or not LIST_ID:
    raise ValueError("API_KEY, SERVER_PREFIX, and LIST_ID must be set in the .env file")

try:
    client = Client()
    client.set_config({
        "api_key": API_KEY,
        "server": SERVER_PREFIX
    })

    # Create a campaign
    campaign_data = {
        "type": "regular",
        "recipients": {
            "list_id": LIST_ID,
            "segment_opts": {
                "saved_segment_id": 179536,
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
                        "value": "b"
                    }
                ]
            }
        },
        "settings": {
            "subject_line": "🔥 Hot Arrivals: Mini Backpacks with Licensed Characters!🔥",
            "from_name": "4sgm.com Wholesale Store",
            "reply_to": "iss@4sgm.com"
        }
    }

    # Log the request data
    request_log_path = 'logs/add_campaign_request.json'
    with open(request_log_path, 'a') as request_log_file:
        json.dump(campaign_data, request_log_file, indent=4)
        request_log_file.write('\n')

    response = client.campaigns.create(campaign_data)
    print(response)

    # Log the response data with a timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    response_log_path = f'logs/add_campaign_response_{timestamp}.json'
    with open(response_log_path, 'w') as response_log_file:
        json.dump(response, response_log_file, indent=4)

except ApiClientError as error:
    print("Error: {}".format(error.text))
    # Log the error data with a timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    error_log_path = 'logs/add_campaign_error.log'
    with open(error_log_path, 'a') as error_log_file:
        error_log_file.write(f"{timestamp}: {error.text}\n")
