from __future__ import print_function
import httplib2
import os
import time
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import sys
import time
try:
    import argparse
    #flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

flags = None
# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Lumos'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = ''
    rangeName = 'Sheet1!A1:A2'

    if len(sys.argv)==1:
        start_time=time.time()*1000.0
        while True:
            result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=rangeName).execute()
            values = result.get('values', [])
            if not values:
                print('No data found.')
            else:
                print(values[0][0]+" "*(3-len(values[0][0]))+" | "+values[1][0]+" "*(3-len(values[0][0]))+" "+str(time.time()*1000.0-start_time))
            start_time=time.time()*1000.0
            time.sleep(0.4)
    elif len(sys.argv)==3 and (sys.argv[2]=="on" or sys.argv[2]=="off"):
        range_="A"+sys.argv[1]
        value_range_body={"range": range_,"majorDimension":"ROWS","values": [[sys.argv[2]]]}
        request = service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range=range_, valueInputOption="RAW", body=value_range_body).execute()
        result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=rangeName).execute()
        values = result.get('values', [])
        if not values:
            print('No data found.')
        else:
            print(values[0][0]+" "*(3-len(values[0][0]))+" | "+values[1][0]+" "*(3-len(values[0][0])), end="\r")
    else:
        print("Garbage detector beeping.")



if __name__ == '__main__':
    main()
