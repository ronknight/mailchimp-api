import os
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("API_KEY")
SERVER_PREFIX = os.getenv("SERVER_PREFIX")
AUDIENCE_ID = os.getenv("AUDIENCE_ID")

if not API_KEY or not SERVER_PREFIX:
    raise ValueError("API_KEY and SERVER_PREFIX must be set in the .env file")

try:
    client = Client()
    client.set_config({
        "api_key": API_KEY,
        "server": SERVER_PREFIX
    })

    response = client.lists.list_segments(AUDIENCE_ID)
    print("Segments Audience ID:")
    print(json.dumps(response, indent=4))  # Pretty print audience information

except ApiClientError as error:
  print("Error: {}".format(error.text))