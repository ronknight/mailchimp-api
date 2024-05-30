import os
import json
import datetime
import argparse
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve API key and server prefix from environment variables
API_KEY = os.getenv("API_KEY")
SERVER_PREFIX = os.getenv("SERVER_PREFIX")

# Ensure API_KEY and SERVER_PREFIX are provided
if not API_KEY or not SERVER_PREFIX:
    raise ValueError("API_KEY and SERVER_PREFIX must be set in the .env file")

# Set up argument parsing
parser = argparse.ArgumentParser(description='Get MailChimp campaign info.')
parser.add_argument('CAMPAIGN_ID', type=str, help='The campaign ID')
args = parser.parse_args()
CAMPAIGN_ID = args.CAMPAIGN_ID

try:
    # Initialize Mailchimp client
    client = Client()
    client.set_config({
        "api_key": API_KEY,
        "server": SERVER_PREFIX
    })

    # Log the request data
    request_log_path = 'logs/get_campaign_request.json'
    request_data = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "campaign_id": CAMPAIGN_ID
    }
    os.makedirs(os.path.dirname(request_log_path), exist_ok=True)
    with open(request_log_path, 'a') as request_log_file:
        json.dump(request_data, request_log_file)
        request_log_file.write('\n')

    # Get information about the campaign
    response = client.campaigns.get(CAMPAIGN_ID)
    print(response)

    # Log the response data with a timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    response_log_path = f'logs/get_campaign_response_{timestamp}.json'
    with open(response_log_path, 'w') as response_log_file:
        json.dump(response, response_log_file, indent=4)

except ApiClientError as error:
    # Handle API client errors
    print("Error: {}".format(error.text))
    
    # Log the error data with a timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    error_log_path = 'logs/get_campaign_error.log'
    with open(error_log_path, 'a') as error_log_file:
        error_log_file.write(f"{timestamp}: {error.text}\n")
