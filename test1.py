from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Path to your service account key file
SERVICE_ACCOUNT_FILE = 'path/to/your/credentials.json'

# Define the scopes
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Authenticate and construct service
credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('sheets', 'v4', credentials=credentials)

# The ID of your spreadsheet
spreadsheet_id = 'spreadsheetId'

# Specify the range and values to append
range_name = 'Sheet1!A1'  # Example range, adjust as necessary
values = [
    ["Value1", "Value2", "Value3"],  # This is the row you want to add
    # Add more rows if necessary
]
value_input_option = 'USER_ENTERED'

# How the input data should be interpreted
value_range_body = {
    "values": values
}

request = service.spreadsheets().values().append(
    spreadsheetId=spreadsheet_id, range=range_name,
    valueInputOption

google-api-python-client google-auth-httplib2 google-auth-oauthlib
