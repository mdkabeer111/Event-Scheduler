from flask import Flask, jsonify, request
import uuid
import json
from datetime import datetime

app = Flask(__name__)
DATA_FILE = 'events.json'

# Load events from file
try:
    with open(DATA_FILE, 'r') as f:
        events = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    events = []

def save_events():
    with open(DATA_FILE, 'w') as f:
        json.dump(events, f, indent=4)

def parse_datetime(dt_str):
 return datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")

@app.route('/events', methods=['POST'])
def create_event():
    data = request.json
    
    # Validate required fields
    required_fields = ['title', 'start_time', 'end_time']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    
    # Handle ID if provided
    if 'id' in data:
        try:
            # Convert ID to integer if it's a string
            provided_id = int(data['id'])
        except ValueError:
            return jsonify({"error": "ID must be an integer"}), 400
        
        # Check if ID already exists
        if any(event['id'] == provided_id for event in events):
            return jsonify({"error": "Event ID already exists"}), 409
    else:
        # Generate new ID if not provided
        provided_id = max(event['id'] for event in events) + 1 if events else 1
    
    # Create event
    event = {
        "id":  str(provided_id),
        "title": data["title"],
        "description": data.get("description", ""),
        "start_time": data["start_time"],
        "end_time": data["end_time"]
    }
    
    events.append(event)
    save_events()
    return jsonify(event), 201

@app.route('/events', methods=['GET'])
def list_events():
    """
    List all events sorted by start_time.
    """
    sorted_events = sorted(events, key=lambda e: parse_datetime(e["start_time"]))
    return jsonify(sorted_events)

@app.route('/events/<event_id>', methods=['PUT'])
def update_event(event_id):
    data = request.json
    for event in events:
        if event["id"] == event_id:
          event["title"] = data.get("title", event["title"])
          event["description"] = data.get("description", event["description"])
          event["start_time"] = data.get("start_time", event["start_time"])
          event["end_time"] = data.get("end_time", event["end_time"])
          save_events()
          return jsonify(event)
    return jsonify({"error": "Event not found"}), 404

@app.route('/events/<event_id>', methods=['DELETE'])
def delete_event(event_id):
    global events
    events = [e for e in events if e["id"] != event_id]
    save_events()
    return jsonify({"message": "Event deleted"})

@app.route('/events/search', methods=['GET'])
def search_events():
    """
    Search events by title or description.
    Example: GET /events/search?q=meeting
    """
    query = request.args.get('q', '').strip().lower()

    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400

    results = []
    for event in events:
        title_match = query in event["title"].lower()
        description_match = query in event["description"].lower()
        if title_match or description_match:
            results.append(event)

    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)      