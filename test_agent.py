from agent_logic import generate_summary

# Dummy input like what spreadsheet_utils gives
dummy_data = [
    {
        "project": "Whitefield Villa",
        "last_updated_days_ago": 5,
        "pending_tasks": ["Assign site engineer", "Confirm timeline"]
    },
    {
        "project": "Koramangala Flat",
        "last_updated_days_ago": 1,
        "pending_tasks": []
    }
]

summary = generate_summary(dummy_data)
print(summary)
