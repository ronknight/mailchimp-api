import os
from dotenv import load_dotenv
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError

# Load environment variables from .env file
load_dotenv()

# Retrieve Mailchimp API key and server prefix from environment variables
API_KEY = os.getenv("API_KEY")
SERVER_PREFIX = os.getenv("SERVER_PREFIX")
AUDIENCE_ID = os.getenv("AUDIENCE_ID")

# Define characters to segment by
characters = [chr(i) for i in range(97, 123)] + [str(i) for i in range(10)]

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

    except ApiClientError as error:
        # Handling API client errors
        print("Error creating segment: {}".format(error.text))

# Function to fetch emails based on specified criteria
def fetch_emails_by_character(client, character):
    try:
        # Define the filter criteria
        filter_criteria = {
            "count": 1000,
            "fields": "members.email_address"
        }

        # Fetch members based on filter criteria
        response = client.lists.get_list_members_info(AUDIENCE_ID, **filter_criteria)

        # Check if the response is successful
        if response.status_code == 200:
            data = response.json()
            if data.get("members", None):
                emails = [member["email_address"] for member in data["members"] if member["email_address"].lower().startswith(character)]
                return emails
            else:
                print(f"No members found for character '{character}'.")
                return []
        else:
            print(f"Failed to fetch members. Status code: {response.status_code}")
            return []

    except ApiClientError as error:
        # Handle API client errors
        print(f"Error fetching emails starting with '{character}': {error.text}")
        return []

# Function to check audience information
def check_audience(client, audience_id):
    try:
        # Call Mailchimp API to get information about the specified audience
        response = client.lists.get_list(audience_id)

        # Check if the response is successful
        if response.get("id", None) == audience_id:
            return response  # Return the audience information
        else:
            print("Failed to fetch audience information. Audience not found.")
            return None

    except ApiClientError as error:
        # Handle API client errors
        print(f"Error fetching audience information: {error.text}")
        return None


# Main function
def main():
    # Initializing the Mailchimp client
    client = MailchimpMarketing.Client()
    client.set_config({
        "api_key": API_KEY,
        "server": SERVER_PREFIX
    })

    # Check audience information
    audience_info = check_audience(client, AUDIENCE_ID)
    if audience_info:
        print("Audience Information:")
        print(audience_info)
        print()

        # Creating segments for each character
        for char in characters:
            segment_name = f"Segment-{char}"
            emails = fetch_emails_by_character(client, char)
            if emails:
                create_segment(client, AUDIENCE_ID, segment_name, emails)

    else:
        print("Failed to fetch audience information. Exiting...")

# Running the main function if the script is executed directly
if __name__ == "__main__":
    main()
