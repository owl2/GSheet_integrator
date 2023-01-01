from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import pandas as pd


class GSheet():
    """A class with function to extract Gsheet and put it into S3 in csv."""

    def __init__(self) -> None:
        pass

    def gsheet_connector(self, token_file: str = 'token.json', SCOPES: list[str] = ['https://www.googleapis.com/auth/spreadsheets.readonly']) -> None:
        """Function that create credentials.json file to use for Gsheet API.""" 
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(token_file):
            creds = Credentials.from_authorized_user_file(token_file, SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(token_file, 'w') as token:
                token.write(creds.to_json())

        return creds

    def gsheet_extract(self, SAMPLE_SPREADSHEET_ID: str, SAMPLE_RANGE_NAME: str) -> pd.DataFrame:
        """Function that deals with the GSheet API and returns the attached dataframe."""
        creds = self.gsheet_connector()
        
        try:
            service = build('sheets', 'v4', credentials=creds)

            # Call the Sheets API
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                        range=SAMPLE_RANGE_NAME).execute()
            values = result.get('values', [])

            if not values:
                print('No data found.z')
                return

            df = pd.DataFrame(values[1:], columns=values[0])

        except HttpError as err:
            print(err)

        return df