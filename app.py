from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

app = Flask(__name__)
Mongo = MongoClient(MONGO_URL)  # adapt your Mongo URI
db = Mongo.myrepo
events = db.events


@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    event = {}
    now = datetime.utcnow().isoformat() + "Z"

    if data.get('pull_request'):
        pr = data['pull_request']
        author = pr['user']['login']
        from_b = pr['head']['ref']
        to_b = pr['base']['ref']
        pr_id = str(pr['id'])
        ts = pr['created_at']

        if data['action'] == 'opened':
            event = {
                "request_id": pr_id,
                "author": author,
                "action": "PULL_REQUEST",
                "from_branch": from_b,
                "to_branch": to_b,
                "timestamp": ts
            }
        elif data['action'] == 'closed' and pr.get('merged'):
            event = {
                "request_id": pr_id,
                "author": author,
                "action": "MERGE",
                "from_branch": from_b,
                "to_branch": to_b,
                "timestamp": ts
            }

    elif data.get('commits'):
        commit_id = data['head_commit']['id'][:6]
        author = data['pusher']['name']
        to_b = data['ref'].split('/')[-1]
        event = {
            "request_id": commit_id,
            "author": author,
            "action": "PUSH",
            "from_branch": "",
            "to_branch": to_b,
            "timestamp": now
        }

    if event:
        events.insert_one(event)
    return 'Webhook received!', 200

@app.route('/events')
def get_events():
    all_events = list(events.find().sort('_id', -1).limit(20))
    for e in all_events:
        e['_id'] = str(e['_id'])  # convert ObjectId to string for JSON
    return jsonify(all_events)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)