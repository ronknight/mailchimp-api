import os
import json
from dotenv import load_dotenv
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError

# Load environment variables from .env file
load_dotenv()

# Retrieve Mailchimp API key, server prefix, and audience ID from environment variables
API_KEY = os.getenv("API_KEY")
SERVER_PREFIX = os.getenv("SERVER_PREFIX")
AUDIENCE_ID = os.getenv("AUDIENCE_ID")

def fetch_all_members(client, audience_id):
    members = []
    offset = 0
    count = 1000  # maximum number of members per request
    while True:
        response = client.lists.get_list_members_info(audience_id, count=count, offset=offset)
        members.extend(response['members'])
        if len(response['members']) < count:
            break
        offset += count
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
        print("Error creating segment: {}".format(error.text))
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

    # Filter members based on SRC and email starting with "a"
    filtered_members = [
        member for member in members
        if member.get('merge_fields', {}).get('SRC') == 'NL-Batch1-A-B' and member['email_address'].startswith('a')
    ]

    # Extract emails from filtered members
    member_emails = [member['email_address'] for member in filtered_members]

    # Create segment with filtered members
    segment_id = create_segment(client, AUDIENCE_ID, "Segment Name", member_emails)

    if segment_id:
        print("Segment created successfully with ID:", segment_id)

except ApiClientError as error:
    # Handle API client errors
    print("Error: {}".format(error.text))
