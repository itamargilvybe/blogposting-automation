from oauth2client.service_account import ServiceAccountCredentials
import gspread
from config import GSPREAD_CREDS_JSON
import datetime
import json

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials_dict = json.loads(GSPREAD_CREDS_JSON)
credentials = ServiceAccountCredentials.from_json_keyfile_dict(
    credentials_dict, scope
)

gc = gspread.authorize(credentials)

def open_spreadsheet(spreadsheet_name):
    try:
        sheet = gc.open(spreadsheet_name)
        return sheet
    except Exception as e:
        print(f"Error opening spreadsheet: {type(e).__name__}: {e}")
        return None

def get_unused_keyword():
    sheet = "keywords"
    try:
        sheet = open_spreadsheet("keywords")
        worksheet = sheet.worksheet('Sheet1')
        rows = worksheet.get_all_records()
        for row in rows:
            if not row['Used on']:
                return row['Keyword']
        return None
    except Exception as e:
        print(f"Error getting unused keyword: {e}")
        return None

def mark_keyword_used(keyword):
    try:
        sheet = open_spreadsheet("keywords")
        worksheet = sheet.worksheet('Sheet1')
        
        # Find the cell containing the keyword
        cell = worksheet.find(keyword)
        if not cell:
            print(f"Could not find keyword '{keyword}' in spreadsheet")
            return None
            
        # Update the 'Used on' column (column B) with current date
        worksheet.update_cell(cell.row, 2, datetime.datetime.now().strftime("%Y-%m-%d"))
        print(f"Updated keyword '{keyword}' in row {cell.row}")
        return None
    except Exception as e:
        print(f"Error updating spreadsheet: {e}")
        return None
