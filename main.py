
from spreadsheet_utils import get_project_files, get_checklist_status
from agent_logic import generate_summary
from datetime import date, timedelta
from spreadsheet_utils import get_project_files, get_checklist_status
from agent_logic import generate_summary, load_yesterday_snapshot
from email_utils import send_email

def main():
    today = date.today()
    yesterday = today - timedelta(days=1)

    today_filename = f"{today}.json"
    yesterday_filename = f"{yesterday}.json"

    files = get_project_files()
    current_data = [get_checklist_status(f['id'], f['name']) for f in files]
    previous_data = load_yesterday_snapshot(yesterday_filename)

    summary = generate_summary(previous_data, current_data, today_filename)
    send_email(summary)

if __name__ == "__main__":
    main()

'''
import os
import json
import datetime
from spreadsheet_utils import get_project_files, get_checklist_status
from agent_logic import generate_summary
from email_utils import send_email

STORAGE_PATH = "storage"

def save_today_snapshot(filename, data):
    os.makedirs(STORAGE_PATH, exist_ok=True)
    with open(os.path.join(STORAGE_PATH, filename), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def load_yesterday_snapshot(filename):
    path = os.path.join(STORAGE_PATH, filename)
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)

    today_file = f"{today}.json"
    yesterday_file = f"{yesterday}.json"

    # 1. Gather all project spreadsheet data
    files = get_project_files()
    current_data = []
    for f in files:
        status = get_checklist_status(f['id'], f['name'])
        current_data.append(status)

    # 2. Load yesterday's data
    previous_data = load_yesterday_snapshot(yesterday_file)

    # 3. Generate summary
    summary = generate_summary(previous_data, current_data)

    # 4. Send email
    send_email(summary)

    # 5. Save today's snapshot
    save_today_snapshot(today_file, current_data)

if __name__ == "__main__":
    main()
'''