import os
from dotenv import load_dotenv
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError

# Load environment variables from .env file
load_dotenv()

# Retrieve Mailchimp API key, server prefix, and audience ID from environment variables
API_KEY = os.getenv("API_KEY")
SERVER_PREFIX = os.getenv("SERVER_PREFIX")
AUDIENCE_ID = os.getenv("AUDIENCE_ID")
COLUMN_SOURCE = "SRC"  # Specifying the name of the column for filtering

# Define characters to segment by
characters = [chr(i) for i in range(97, 123)] + [str(i) for i in range(0, 10)]

# Function to create a segment in Mailchimp audience
def create_segment(client, audience_id, segment_name, emails):
    try:
        # Creating a segment object with filtering condition
        segment = {
            "name": segment_name,
            "static_segment": emails
        }

        # Calling Mailchimp API to create the segment
        response = client.lists.create_segment(audience_id, segment)

        print(f"Segment '{segment_name}' created successfully.")
        return response

    except ApiClientError as error:
        # Handling API client errors
        print("Error creating segment: {}".format(error.text))

# Function to fetch members and filter based on the SRC field
def fetch_unique_emails(client, audience_id, column_source, value):
    try:
        unique_emails = []
        offset = 0
        count = 1000

        while True:
            # Fetching batch of members
            response = client.lists.get_list_members_info(audience_id, count=count, offset=offset, fields="members.email_address,members.merge_fields")

            if 'members' in response:
                for member in response['members']:
                    # Check if the SRC field matches the value
                    if column_source in member['merge_fields'] and member['merge_fields'][column_source] == value:
                        unique_emails.append(member['email_address'])

                # Break the loop if there are no more members to fetch
                if len(response['members']) < count:
                    break

                offset += count
            else:
                break

        return unique_emails

    except ApiClientError as error:
        # Handle API client errors
        print(f"Error fetching members: {error.text}")
        return []

# Function to check audience information
def check_audience(client, list_id):
    try:
        response = client.lists.get_list(list_id)
        print("Audience Information:")
        print(response)
        return response
    except ApiClientError as error:
        print("Error: {}".format(error.text))
        return None

# Main function
def main():
    # Initializing the Mailchimp client
    client = MailchimpMarketing.Client()
    client.set_config({
        "api_key": API_KEY,
        "server": SERVER_PREFIX
    })

    # Checking the audience information
    audience_info = check_audience(client, AUDIENCE_ID)
    
    if audience_info:
        # Fetch unique emails with the specified criteria
        unique_emails = fetch_unique_emails(client, AUDIENCE_ID, COLUMN_SOURCE, "NL-Batch1-A-B")

        if unique_emails:
            # Segment the emails based on the first character
            for char in characters:
                # Filter emails that start with the current character
                filtered_emails = [email for email in unique_emails if email.startswith(char)]
                if filtered_emails:
                    segment_name = f"Segment-NL-Batch1-A-B-{char.upper()}"
                    create_segment(client, AUDIENCE_ID, segment_name, filtered_emails)
                else:
                    print(f"No emails found for segment starting with '{char}'")
        else:
            print("No emails found with the specified criteria.")

# Running the main function if the script is executed directly
if __name__ == "__main__":
    main()
