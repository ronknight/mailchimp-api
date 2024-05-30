import os
import json
import logging
from dotenv import load_dotenv
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError

# Load environment variables from .env file
load_dotenv()

# Retrieve Mailchimp API key, server prefix, and audience ID from environment variables
API_KEY = os.getenv("API_KEY")
SERVER_PREFIX = os.getenv("SERVER_PREFIX")
AUDIENCE_ID = os.getenv("AUDIENCE_ID")

# Setup logging
logging.basicConfig(filename='logs/get_list_member_info_response_timestamp.json', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

def fetch_all_members(client, audience_id):
    members = []
    offset = 0
    count = 1000  # maximum number of members per request
    while True:
        try:
            response = client.lists.get_list_members_info(audience_id, count=count, offset=offset)
            members.extend(response['members'])
            if len(response['members']) < count:
                break
            offset += count
        except ApiClientError as error:
            error_message = "Error fetching list members: {}".format(error.text)
            logging.error(error_message)
            print(error_message)
            return None
    return members

def create_segment(client, audience_id, name, member_emails):
    try:
        # Define segment options
        segment_options = {
            "conditions": [
                {
                    "condition_type": "EmailAddress",
                    "field": "email_address",
                    "op": "starts",
                    "value": "a"
                },
                {
                    "condition_type": "MergeField",
                    "field": "SRC",
                    "op": "eq",
                    "value": "NL-Batch1-A-B"
                }
            ]
        }

        # Create the segment with segment options
        response = client.lists.create_segment(
            audience_id, 
            {"name": name, "options": segment_options}
        )
        segment_id = response['id']
        
        # Add members to the segment
        client.lists.add_segment_members(audience_id, segment_id, {"members_to_add": member_emails})
        
        return segment_id
    except ApiClientError as error:
        error_message = "Error creating segment: {}".format(error.text)
        logging.error(error_message)
        print(error_message)
        return None

try:
    # Initialize Mailchimp client
    client = MailchimpMarketing.Client()
    client.set_config({
        "api_key": API_KEY,
        "server": SERVER_PREFIX
    })

    # Fetch all list members
    members = fetch_all_members(client, AUDIENCE_ID)

    if members:
        # Filter members based on SRC and email starting with "a"
        filtered_members = [
            member for member in members
            if member.get('merge_fields', {}).get('SRC') == 'NL-Batch1-A-B' and member['email_address'].startswith('a')
        ]

        # Extract emails from filtered members into a dictionary
        email_dict = {member['email_address']: member['merge_fields'] for member in filtered_members}

        # Create segment with filtered members
        segment_id = create_segment(client, AUDIENCE_ID, "NL-Batch1-A-B-a", list(email_dict.keys()))

        if segment_id:
            print("Segment created successfully with ID:", segment_id)
            logging.info("Segment created successfully with ID: {}".format(segment_id))
        else:
            print("Error creating segment.")
    else:
        print("No members found in the audience.")
except ApiClientError as error:
    # Handle API client errors
    error_message = "Error: {}".format(error.text)
    logging.error(error_message)
    print(error_message)
