import os
from dotenv import load_dotenv
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
import json
import datetime

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("API_KEY")
SERVER_PREFIX = os.getenv("SERVER_PREFIX")

def append_log_to_file(data, filename):
    # If the file does not exist, create it with an empty list
    if not os.path.exists(filename):
        with open(filename, 'w') as file:
            json.dump([], file)
    
    # Read existing data
    with open(filename, 'r') as file:
        logs = json.load(file)

    # Append new data
    logs.append(data)

    # Write back to file
    with open(filename, 'w') as file:
        json.dump(logs, file, indent=4)

def log_to_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

try:
    # Initialize the Mailchimp client
    client = MailchimpMarketing.Client()
    client.set_config({
        "api_key": API_KEY,
        "server": SERVER_PREFIX
    })

    # Prepare the request data without the API key
    request_data = {
        "timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "server_prefix": SERVER_PREFIX,
        "endpoint": "/lists"
    }

    # Append the request data to a JSON file
    request_log_filename = "logs/get_list_requests_log.json"
    append_log_to_file(request_data, request_log_filename)

    # Get all lists in the Mailchimp account
    response = client.lists.get_all_lists()

    # Pretty print the JSON response
    print("Get list logs are created.")

    # Log the response data to a JSON file
    response_filename = f"logs/get_list_response_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.json"
    log_to_file(response, response_filename)

except ApiClientError as error:
    # Handle API client errors
    error_data = {
        "timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "error": error.text
    }
    error_filename = f"logs/get_list_error_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.json"
    log_to_file(error_data, error_filename)
    print("Error: {}".format(error.text))
