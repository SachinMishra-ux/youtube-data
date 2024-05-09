from google.oauth2.credentials import Credentials  # Import Credentials class
import json  # Import json module to handle JSON file reading

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

def authenticate():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        with open('token.json', 'r') as token:
            creds_data = json.load(token)
            creds = Credentials.from_authorized_user_info(creds_data)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/Users/sachinmishra/Desktop/personal/Youtubedata/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds

'''
if __name__ == '__main__':
    credentials = authenticate()
    print("Authentication Successful!")
'''