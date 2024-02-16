import gspread
from google.oauth2.service_account import Credentials
from gspread.utils import ValueRenderOption

# Set up the credentials
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_file('/Users/izmalk/Library/CloudStorage/Dropbox/spreadsheeter/smart-idiom-414523-5d2f119bbbdd.json', scopes=scope)
client = gspread.authorize(creds)

print(client.list_spreadsheet_files())
# Open the spreadsheet
spreadsheet = client.open('TW_searching_2024').sheet1  # Use the actual name of your spreadsheet

# Add a new line
row = [None, spreadsheet.get('B1', value_render_option=ValueRenderOption.unformatted).first(),
       None, None, None, None, None, None, None, None, "Link4", "Comments4"]  # Example row data you want to add
spreadsheet.append_row(row)  # Adds a new row with your data

print("Finished.")
