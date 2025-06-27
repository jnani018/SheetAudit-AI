# 🧠 SheetAudit-AI: Autonomous Project Summary Agent for Google Sheets
SheetAudit-AI is an intelligent auditing system powered by GPT-4o and LangChain, designed to analyze multiple project checklists stored in Google Sheets and generate daily progress summaries automatically.

🔍 What it does:
Connects to multiple Google Sheets, each representing a renovation project

Reads raw checklist data from each project and calculates actual task completion percentages

Compares today’s progress with yesterday’s snapshot using stored JSON data

Flags stale or skipped sheets, detects new projects, and highlights progress changes

Generates human-like email summaries via GPT-4o using LangChain prompt chaining

Automatically emails the summaries to stakeholders

Fully supports daily scheduling and project-level compliance tracking

⚙️ Tech Stack:
LangChain + GPT-4o (OpenAI) for intelligent summarization

Google Sheets API for spreadsheet access and data extraction

Python + JSON storage for snapshot-based comparison

Secure email dispatching using SMTP

Modular design for easy extension and training
