<p><a target="_blank" href="https://app.eraser.io/workspace/Lh3VRw97MxtTtBm1XpZd" id="edit-in-eraser-github-link"><img alt="Edit in Eraser" src="https://firebasestorage.googleapis.com/v0/b/second-petal-295822.appspot.com/o/images%2Fgithub%2FOpen%20in%20Eraser.svg?alt=media&amp;token=968381c8-a7e7-472a-8ed6-4a6626da5501"></a></p>

# MailChimp API Scripts
This repository contains three Python scripts that interact with the MailChimp API to perform various tasks related to campaigns and segments.

1. `add_segment.py` 
2. `add_segment_range.py` 
3. `add_campaign.py` 
4. `get_campaign.py` 
## Prerequisites
Before running these scripts, you'll need to set up the following:

- Python 3.x installed
- Mailchimp Marketing API key
- Mailchimp server prefix (e.g., `us1` , `us2` , etc.)
- Mailchimp audience (list) ID
1. Install the `mailchimp-marketing`  library:
```bash
pip install mailchimp-marketing
```
1. Install the python-dotenv library:
```bash
pip install python-dotenv
```
1. Create a .env file in the root directory of the project and add the following environment variables:
Replace your_mailchimp_api_key, your_mailchimp_server_prefix, and your_mailchimp_audience_id with the appropriate values from your MailChimp account.

## Setup
1. Clone this repository or download the code files.
2. Create a `.env`  file in the project root directory and add the following environment variables: Replace the placeholders with your actual Mailchimp API key, server prefix, and audience ID.API_KEY=your_mailchimp_api_key
SERVER_PREFIX=your_mailchimp_server_prefix
AUDIENCE_ID=your_mailchimp_audience_id
3. Install the required Python packages by running:pip install -r requirements.txt
## Scripts
### `get_campaign.py` 
This script retrieves information about a specific MailChimp campaign. It logs the request and response data in the logs directory.

Usage:

```bash
python get_campaign.py CAMPAIGN_ID
```
Replace CAMPAIGN_ID with the ID of the campaign you want to retrieve. You can get the CAMPAIGN_ID if you don't have it from the campaign url, it is the value of parameter "id".

### `add_segment.py` 
This script creates a new segment in the specified Mailchimp audience based on the provided batch name.

Usage:

```bash
python add_segment.py batch_name
```
Replace `batch_name` with the desired name for the segment.

### `add_segment_range.py` 
This script creates a new segment in the specified Mailchimp audience based on the provided batch name, email address range, and part name.

Usage:

```bash
python add_segment_range.py batch_name greater less part
```
- `batch_name` : The base name for the segment.
- `greater` : The starting character of the email address range.
- `less` : The ending character of the email address range.
- `part` : The part name to be appended to the segment name.
### `add_campaign.py` 
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
├── add_segment_range_request.json
├── add_segment_range_response_20240604_195307.json
├── add_segment_request.json
├── add_segment_response_20230530_123456.json
├── get_campaign_error.log
├── get_campaign_request.json
└── get_campaign_response_20230530_123456.json
```
## Dependencies
The scripts use the following Python packages:

- `mailchimp_marketing` : Mailchimp Marketing API client library
- `python-dotenv` : Loads environment variables from a `.env`  file
These dependencies are listed in the `requirements.txt` file and will be installed automatically when running `pip install -r requirements.txt`.

## License
This project is licensed under the MIT License.


<!-- eraser-additional-content -->
## Diagrams
<!-- eraser-additional-files -->
<a href="/README-MailChimp API Scripts Flowchart-1.eraserdiagram" data-element-id="3QY7rmV6Rz3Kh75SquPbz"><img src="/.eraser/Lh3VRw97MxtTtBm1XpZd___3Jivg2tjMecMlrHwbIVIBR8f7U03___---diagram----bae7e67746269694449413830429fe3c-MailChimp-API-Scripts-Flowchart.png" alt="" data-element-id="3QY7rmV6Rz3Kh75SquPbz" /></a>
<!-- end-eraser-additional-files -->
<!-- end-eraser-additional-content -->
<!--- Eraser file: https://app.eraser.io/workspace/Lh3VRw97MxtTtBm1XpZd --->