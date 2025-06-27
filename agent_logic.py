'''# agent_logic.py
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",  # or gpt-4o / gpt-3.5-turbo
    temperature=0.3,
    max_tokens=800
)

prompt = ChatPromptTemplate.from_template("""
You are an AI assistant writing short daily summaries about ongoing home renovation projects.

You receive two JSON lists:
- YESTERDAY: List of projects with raw sheet data (multiple sheets per project)
- TODAY: Same structure, with today’s updated data

Each project includes:
- name
- days since last update
- raw_data (sheet-wise row data in list-of-lists format)

Your job:
- Carefully compare the raw rows and structure for each project
- Write a natural, short, human-readable update for the team
- Mention what progressed, what didn’t, and what needs attention
- Do not follow a checklist or fixed format
- Do not repeat headings like “Status Overview” or “Recommendations”
- Just write 3–5 clear lines per project like a smart project lead would write

###
YESTERDAY:
{previous}

###
TODAY:
{current}

Write one combined email body for the team covering all projects.
Avoid headings. Keep it smart and natural.
""")

chain = prompt | llm

def generate_summary(previous, current):
    return chain.invoke({
        "previous": previous,
        "current": current
    }).content'''

import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from spreadsheet_utils import completion_ratio

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3, max_tokens=900)

prompt = ChatPromptTemplate.from_template("""
You are an autonomous renovation-project auditor.

You receive:
- YESTERDAY (list of projects with their raw data)
- TODAY (list of projects with updated raw data and a completion_pct)

Each project contains:
- project: project name
- last_updated_days_ago: number of days since anyone modified it
- raw_data: dictionary of sheet_name: sheet_values (2D lists)
- completion_pct: overall percentage of all tasks marked as done

Instructions:
1. For each project, compare yesterday and today.
2. Calculate and report progress change (if any) in %.
3. Flag any sheet (except the first one) that is mostly empty or skipped. Use normal sheet flow: sales → engineer → etc.
4. If any sheet hasn’t been touched for 5+ days, say it's paused and don’t report on it tomorrow.
5. Detect new projects (not present yesterday). Based on their completion_pct:
   - <5%: say “new checklist, not yet started”
   - 5–60%: say “checklist started, some progress made”
   - >60%: say “checklist mostly done, finish the rest soon”
6. Write one smart paragraph per project (3–4 lines max). Be clear and concise.
7. Don’t use headings, sections, or bullet points — just human-style status summaries.

###
YESTERDAY:
{previous}

###
TODAY:
{current}

Write the full combined email update for all projects.
""")

chain = prompt | llm

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

def generate_summary(prev: list, curr: list, today_filename=None):
    for project in curr:
        project["completion_pct"] = completion_ratio(project["raw_data"])

    # Save today’s snapshot (optional if filename passed)
    if today_filename:
        save_today_snapshot(today_filename, curr)

    return chain.invoke({
        "previous": json.dumps(prev, indent=2),
        "current": json.dumps(curr, indent=2)
    }).content


'''
import json
import os
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from huggingface_hub import login
from spreadsheet_utils import completion_ratio

# Load environment variables
load_dotenv()

# Constants
MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.1"
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

# Authenticate to Hugging Face
login(token=HUGGINGFACE_TOKEN)

# Load model and tokenizer with token access
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_auth_token=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype="auto",
    device_map="auto",
    use_auth_token=True
)

# Create text generation pipeline
text_generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=700,
    do_sample=True,
    temperature=0.7,
    top_p=0.95,
    pad_token_id=tokenizer.eos_token_id
)

# Main summary generation function
def generate_summary(prev: list, curr: list) -> str:
    for project in curr:
        project["completion_pct"] = completion_ratio(project["raw_data"])

    prompt = f"""
You are an autonomous renovation-project auditor.

YESTERDAY:
{json.dumps(prev, indent=2)}

TODAY:
{json.dumps(curr, indent=2)}

Write a short, smart summary update for the project team. Include:
- Progress difference
- Completion percentage
- Skipped sheets
- Any stale work
- Notes for new projects
Avoid bullet points, be natural and helpful.
"""

    result = text_generator(prompt)[0]["generated_text"]
    return result[len(prompt):].strip()
'''
