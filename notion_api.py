from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Get token and DB ID from environment variables
NOTION_TOKEN = os.environ.get("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")
DATABASE_ID = os.environ.get("2603cb131a8b80a5b807d3fe1fcff973")

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def add_entry(entry, date, category, metric, value, notes=""):
    url = "https://api.notion.com/v1/pages"
    data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Entry": {"title": [{"text": {"content": entry}}]},
            "Date": {"date": {"start": date}},
            "Category": {"select": {"name": category}},
            "Metric": {"rich_text": [{"text": {"content": metric}}]},
            "Value": {"number": value},
            "Notes": {"rich_text": [{"text": {"content": notes}}]}
        }
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

@app.route("/add", methods=["POST"])
def add():
    body = request.json
    entry = body.get("entry")
    date = body.get("date")
    category = body.get("category")
    metric = body.get("metric")
    value = body.get("value")
    notes = body.get("notes", "")
    
    result = add_entry(entry, date, category, metric, value, notes)
    return jsonify(result)

@app.route("/", methods=["GET"])
def home():
    return {"status": "Notion API Bridge is running 🚀"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
