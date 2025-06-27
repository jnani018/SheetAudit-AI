# SheetAudit-AI
Autonomous Project Summary Agent for Google Sheets
SheetAudit-AI is an intelligent, LLM-powered auditing system that automates daily project updates by analyzing checklist data stored in Google Sheets. Designed for renovation workflows, it leverages GPT-4o and LangChain to generate human-like progress summaries and deliver them via email.

# What It Does
Connects to multiple Google Sheets — each one represents a renovation project

Extracts raw checklist data and calculates task completion percentages

Compares today's progress with yesterday's using locally stored JSON snapshots

Flags issues like skipped sheets, paused projects, and missing updates

Detects new projects and categorizes their current state (not started, in-progress, almost done)

Generates a clean daily summary written in human style using GPT-4o via LangChain

Automatically sends the summary via email to stakeholders on a scheduled basis

Supports daily tracking, accountability, and quick status visibility

# Tech Stack
LangChain + GPT-4o (OpenAI) for natural language generation

Google Cloud APIs (Sheets + Drive) for accessing live project data

Python for automation logic and processing

JSON snapshots for daily state comparison

SMTP for secure email dispatch

Modular, lightweight design — easy to extend, retrain, or plug into other workflows

# Limitations / Known Issues
Initially attempted using Hugging Face + Mistral 7B to run the summarization locally,Failed due to hardware limitations (model size too large for local setup)

Finetuning setup attempted via train_script.py which works for mistral model but GPT-style models do not support direct finetuning

Task scheduling is not yet fully automated — setting it up on cloud (e.g., via Cloud Functions or cron on VPS) is needed for production use. For now Using Task scheduler on windows which schedules the task locally.
