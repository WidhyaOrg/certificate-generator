from __future__ import print_function
import pickle
import os.path
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from modules.certificate import Certificates

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
#https://docs.google.com/spreadsheets/d/13Czdsi-i3FwKjx8YNqSP04-x6WZ6gamAoPD82UZmJSs/edit?usp=sharing
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
RANGE_NAME = os.getenv('RANGE_NAME')

class Validate(object):

    def __init__(self, email):
        self.given_mail = email

    def get_data(self):
        """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        email_list, name_list = [], []
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'modules/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('modules/token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            return [],[]
        else:
            for row in values:
                email_list += [row[1]]
                name_list += [row[2]]

        return email_list, name_list

    def is_registered(self, email):
        email_list, name_list = self.get_data()
        if(email in email_list):
            print(name_list[email_list.index(email)])
            return name_list[email_list.index(email)]
        else:
            return 0

    def generate_certificate(self):
        name = self.is_registered(self.given_mail)
        if(name == 0):
            return "Please fill the feedback form!"
        else:
            certificate = Certificates(name=name, access='single')
            cert = certificate.generate()

            return name
