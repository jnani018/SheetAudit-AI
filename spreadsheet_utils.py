'''import os
import datetime
import pytz
from google.oauth2 import service_account
from googleapiclient.discovery import build
import gspread
from dotenv import load_dotenv

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets.readonly']
SERVICE_FILE = os.getenv('GOOGLE_SERVICE_JSON')
FOLDER_ID = os.getenv('DRIVE_FOLDER_ID')

credentials = service_account.Credentials.from_service_account_file(SERVICE_FILE, scopes=SCOPES)

def get_drive_service():
    return build('drive', 'v3', credentials=credentials)

def get_sheet_client():
    return gspread.authorize(credentials)

def get_project_files():
    service = get_drive_service()
    query = f"'{FOLDER_ID}' in parents and mimeType='application/vnd.google-apps.spreadsheet'"
    results = service.files().list(q=query, fields="files(id, name, modifiedTime)").execute()
    print(f"Using folder ID: {FOLDER_ID}")
    return results.get('files', [])

def get_checklist_status(file_id, file_name):
    gc = get_sheet_client()
    sh = gc.open_by_key(file_id)

    # Last modified check
    drive_service = get_drive_service()
    file_meta = drive_service.files().get(fileId=file_id, fields='modifiedTime').execute()
    last_updated = datetime.datetime.fromisoformat(file_meta['modifiedTime'].replace('Z', '+00:00'))
    now = datetime.datetime.now(pytz.UTC)
    delta = now - last_updated

    # Read raw data from all sheets
    all_data = {}
    for ws in sh.worksheets():
        values = ws.get_all_values()
        all_data[ws.title] = values  # Store as list of rows

    return {
        "project": file_name,
        "last_updated_days_ago": delta.days,
        "raw_data": all_data  # This will be passed to LLM
    }'''
import os, datetime, pytz
from google.oauth2 import service_account
from googleapiclient.discovery import build
import gspread
from dotenv import load_dotenv

load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets.readonly",
]
SERVICE_FILE = os.getenv("GOOGLE_SERVICE_JSON")
FOLDER_ID    = os.getenv("DRIVE_FOLDER_ID")
credentials  = service_account.Credentials.from_service_account_file(SERVICE_FILE, scopes=SCOPES)

def _drive():
    return build("drive", "v3", credentials=credentials)

def _gspread():
    return gspread.authorize(credentials)

def get_project_files():
    query = f"'{FOLDER_ID}' in parents and mimeType='application/vnd.google-apps.spreadsheet'"
    result = _drive().files().list(q=query, fields="files(id, name, modifiedTime)").execute()
    return result.get("files", [])

def get_checklist_status(file_id, file_name):
    gc = _gspread()
    sh = gc.open_by_key(file_id)
    drive_service = _drive()
    file_meta = drive_service.files().get(fileId=file_id, fields='modifiedTime').execute()
    last_updated = datetime.datetime.fromisoformat(file_meta['modifiedTime'].replace('Z', '+00:00'))
    now = datetime.datetime.now(pytz.UTC)
    delta = now - last_updated

    all_data = {}
    for ws in sh.worksheets():
        all_data[ws.title] = ws.get_all_values()

    return {
        "project": file_name,
        "last_updated_days_ago": delta.days,
        "raw_data": all_data
    }

def completion_ratio(raw_data: dict) -> int:
    done, total = 0, 0
    for sheet in raw_data.values():
        if not sheet: continue
        header, *rows = sheet
        if "Done?" not in header: continue
        idx = header.index("Done?")
        for row in rows:
            if len(row) <= idx: continue
            total += 1
            if str(row[idx]).strip().lower() in ["true", "yes", "1"]:
                done += 1
    return round((done / total) * 100) if total > 0 else 0
