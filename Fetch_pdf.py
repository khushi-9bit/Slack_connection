import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import requests

# Load token from environment
slack_token = os.getenv("SLACK_BOT_TOKEN")
client = WebClient(token=slack_token)

try:
    channel_id = "C064UPNG8JU"
    response = client.files_list(channel=channel_id)

    pdf_file_url = None
    for file in response['files']:
        if file['mimetype'] == 'application/pdf':
            pdf_file_url = file['url_private_download']
            break

    if pdf_file_url:
        print("✅ PDF file found! Downloading...")

        headers = {'Authorization': f'Bearer {slack_token}'}
        pdf_response = requests.get(pdf_file_url, headers=headers)

        with open("downloaded_file.pdf", "wb") as f:
            f.write(pdf_response.content)

        print("✅ PDF downloaded successfully!")
    else:
        print("❌ No PDF found in the channel.")

except SlackApiError as e:
    print(f"❌ Error: {e.response['error']}")
