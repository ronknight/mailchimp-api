# MailChimp API Scripts

This repository contains three Python scripts that interact with the MailChimp API to perform various tasks related to campaigns and segments.

## Prerequisites

Before running these scripts, you'll need to set up the following:

1. Install the `mailchimp-marketing` library:

```bash
pip install mailchimp-marketing
```

2. Install the python-dotenv library:

```bash
pip install python-dotenv
```

3. Create a .env file in the root directory of the project and add the following environment variables:

```bash
API_KEY=your_mailchimp_api_key
SERVER_PREFIX=your_mailchimp_server_prefix
AUDIENCE_ID=your_mailchimp_audience_id
```

Replace your_mailchimp_api_key, your_mailchimp_server_prefix, and your_mailchimp_audience_id with the appropriate values from your MailChimp account.

## Scripts

1. get_campaign.py
This script retrieves information about a specific MailChimp campaign. It logs the request and response data in the logs directory.

Usage:
```bash
python get_campaign.py CAMPAIGN_ID
```
Replace CAMPAIGN_ID with the ID of the campaign you want to retrieve.

2. add_segment.py
This script creates a new MailChimp segment based on the provided batch and letter. It appends the batch name and letter to the segment name and condition value, and logs the request and response data in the logs directory.

Usage:
```bash
python add_segment.py BATCHNAME LETTER
```
Replace LETTER with the letter you want to append to the segment name and condition value.

3. add_campaign.py
This script creates a new MailChimp campaign targeting a specific segment. It logs the request and response data in the logs directory.
Note: This script is hard-coded to create a campaign with a specific subject line, from name, and reply-to address. You may need to modify the campaign_data dictionary in the script to customize the campaign settings according to your requirements.

Usage:
```bash
python add_campaign.py
```

## Logs
The scripts create log files in the logs directory to keep track of requests, responses, and errors. The log file names are generated based on the timestamp and script name.

```bash
logs/
├── add_campaign_error.log
├── add_campaign_request.json
├── add_campaign_response_20230530_123456.json
├── add_segment_error_20230530_123456.json
├── add_segment_request.json
├── add_segment_response_20230530_123456.json
├── get_campaign_error.log
├── get_campaign_request.json
└── get_campaign_response_20230530_123456.json
```

## License
This project is licensed under the MIT License.