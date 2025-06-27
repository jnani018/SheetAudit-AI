from email_utils import send_email

sample = """
Test mail from reno-agent system.
Project: Indiranagar 2BHK
- Last updated: 4 days ago
- Pending: Assign engineer, Confirm site call
"""

send_email(sample)
