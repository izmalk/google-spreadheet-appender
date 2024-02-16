import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Set up the credentials
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/izmalk/Library/CloudStorage/Dropbox/spreadsheeter/smart-idiom-414523-5d2f119bbbdd.json', scope)
client = gspread.authorize(creds)

# Open the spreadsheet
spreadsheet = client.open('TW searching_2024').sheet1  # Use the actual name of your spreadsheet

# Add a new line
row = ["Test", "test2", "test3"]  # Example row data you want to add
spreadsheet.append_row(row)  # Adds a new row with your data
print("Finished")


