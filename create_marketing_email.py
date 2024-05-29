import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError

# Replace these with your own values
API_KEY = 'your_api_key'
SERVER_PREFIX = 'your_server_prefix'  # e.g., 'us10'
LIST_ID = 'your_list_id'
FROM_NAME = 'Your Name'
REPLY_TO = 'your_email@example.com'
SUBJECT = 'Your Email Subject'
CAMPAIGN_TITLE = 'Your Campaign Title'

client = MailchimpMarketing.Client()
client.set_config({
    "api_key": API_KEY,
    "server": SERVER_PREFIX
})

def create_campaign():
    try:
        response = client.campaigns.create({
            "type": "regular",
            "recipients": {
                "list_id": LIST_ID
            },
            "settings": {
                "subject_line": SUBJECT,
                "title": CAMPAIGN_TITLE,
                "from_name": FROM_NAME,
                "reply_to": REPLY_TO
            }
        })
        return response['id']
    except ApiClientError as error:
        print("Error creating campaign: {}".format(error.text))

def set_campaign_content(campaign_id, html_content):
    try:
        response = client.campaigns.set_content(campaign_id, {
            "html": html_content
        })
        print("Campaign content set successfully")
    except ApiClientError as error:
        print("Error setting campaign content: {}".format(error.text))

def send_campaign(campaign_id):
    try:
        response = client.campaigns.send(campaign_id)
        print("Campaign sent successfully")
    except ApiClientError as error:
        print("Error sending campaign: {}".format(error.text))

if __name__ == "__main__":
    campaign_id = create_campaign()
    if campaign_id:
        html_content = """
        <html>
        <body>
        <h1>Welcome to our Newsletter</h1>
        <p>This is an example of a marketing email.</p>
        </body>
        </html>
        """
        set_campaign_content(campaign_id, html_content)
        send_campaign(campaign_id)
