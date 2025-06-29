# Event Scheduler API

A minimalistic REST API built with Python Flask for handling events. This API provides you with a means of standard CRUD (Create, Read, Update, Delete) operations on event data, which gets persisted to a local JSON file automatically.

## Features

- Create events with title, optional description, start time, and end time.
- Get a list of all events ordered by start time.
- Update event details.
- Delete events.
- Saved data to `events.json` (so it survives restarts).

##  Getting Started

To have the Event Scheduler API running on your local machine, do the following:

### Requirements

* Python 3.6+
* `pip` (Python package installer)

### ⬇️ Installation

1. Clone the repository or download files:

```
event_scheduler/
├── app.py
├── events.json
├── requirements.txt
```

2.  **Install dependencies:**
    This project only needs Flask. Although a `requirements.txt` is typical, for just Flask, you can install directly:
```bash
    pip install Flask
    ```
    *(If you want to use `requirements.txt`, put a file named `requirements.txt` in the project root that contains only `Flask`, then execute `pip install -r requirements.txt`)*

3.  **Initialize `events.json` (if you don't have it):**
The application will create `events.json` automatically if it doesn't exist. But if you prefer it to be an empty array on your first run, you can manually create it:
    ```json
    []
    ```
    Save this to `events.json` in the same directory as your `app.py` file.

### Running the Application

Run the Flask app using:

```bash
python app.py
```

You will see output like:

```
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

The API is now ready at:
```
http://127.0.0.1:5000
```

---

## API Usage Examples

You can try out the API with tools such as `curl` (command line), Postman, Insomnia, or an equivalent HTTP client.

---

### 1. Create an Event

**Endpoint:** `POST /events`
**Description:** Creates a new event record.
**Request Body (JSON):**
    * `title` (string, **required**): Event name.
    * `start_time` (string, **required**): Event start date and time in `YYYY-MM-DD HH:MM` format.
* `end_time` (string, **required**): The end date and time of the event in `YYYY-MM-DD HH:MM` format.
* `description` (string, optional): A full description of the event.

**Example Request:**
    ```bash
    curl -X POST [http://127.0.0.1:5000/events](http://127.0.0.1:5000/events) \
      -H "Content-Type: application/json" \
      -d '{
         "title": "Doctor Appointment",
        "description": "Annual checkup",
        "start_time": "2025-07-01 10:00",
        "end_time": "2025-07-01 11:00"
      }'
    ```
**Sample Success Response (Status: 201 Created):**json
    {
"id": "b14d4d35-b50c-43f7-b067-cf580eb0f2ee",
      "title": "Doctor Appointment",
      "description": "Annual checkup",
      "start_time": "2025-07-01 10:00",
      "end_time": "2025-07-01 11:00"
    }
    ```

---

## 2. List All Events

**Endpoint:** `GET /events`
**Description:** Retrieves a list of all events, sorted chronologically by their `start_time`.
**Example Request:**
```bash
    curl [http://127.0.0.1:5000/events](http://127.0.0.1:5000/events)
    ```
**Sample Success Response (Status: 200 OK):**json
    [
      {
        "id": "b14d4d35-b50c-43f7-b067-cf580eb0f2ee",
        "title": "Doctor Appointment",
        "description": "Annual checkup",
"start_time": "2025-07-01 10:00",
        "end_time": "2025-07-01 11:00"
      }, {
        "id": "another-event-id",
        "title": "Team Standup",
        "description": "
"start_time": "2025-07-02 09:30",
        "end_time": "2025-07-02 10:00"
      }
    ]
    ```

---

## 3. Update an Event

**Endpoint:** `PUT /events/<event_id>`
**Description:** Updates the details of an existing event. You only need to include the fields you want to change in the request body.
**URL Parameter:** `<event_id>` (string): ID of the event to update (e.g., `b14d4d35-b50c-43f7-b067-cf580eb0f2ee`).
**Request Body (JSON):** (Optional fields to update: `title`, `description`, `start_time`, `end_time`).

**Example Request:**
    ```bash
    curl -X PUT [http://127.0.0.1:5000/events/b14d4d35-b50c-43f7-b067-cf580eb0f2ee](http://127.0.0.1:5000/events/b14d4d35-b50c-43f7-b067-cf580eb0f2ee) \
      -H "Content-Type: application/json" \
      -d '{
        "title": "Updated Appointment",
        "start_time": "2025-07-01 09:00"
    }
**Sample Success Response (Status: 200 OK):**json
    {
      "id": "b14d4d35-b50c-43f7-b067-cf580eb0f2ee",
      "title": "Updated Appointment",
      "description": "Annual checkup",
      "start_time": "2025-07-01 09:00",
      "end_time": "2025-07-01 11:00"
}



## 4. Delete an Event

**Endpoint:** `DELETE /events/<event_id>`
**Description:** Deletes an event by its unique ID.
**URL Parameter:** `<event_id>` (string): The unique ID of the event to delete.

**Example Request:**
    ```bash
    curl -X DELETE [http://127.0.0.1:5000/events/b14d4d35-b50c-43f7-b067-cf580eb0f2ee](http://127.0.0.1:5000/events/b14d4d35-b50c-43f7-b067-cf580eb0f2ee)
    ```
**Sample Success Response (Status: 200 OK):**json
{
      "message": "Event deleted"
    }
```



## 5. Search Events

**Endpoint:** `GET /events/search`
**Description:** Finds events by searching for matching keywords in their `title` or `description`.
**Query Parameter:** `q` (string, **mandatory**): The search query.
**Example Request:**
    ```bash
    curl "[http://127.0.0.1:5000/events/search?q=meeting]"
    ```
**Sample Success Response (Status: 200 OK):**json
[
      {
        "id": "another-event-id",
        "title": "Team Standup",
        "description": "Weekly team meeting",
        "start_time": "2025-07-02 09:30",
        "end_time": "2025-07-02 10:00"
      }

]


## Important Notes & Error Handling

**Date/Time Format:**  All `start_time` and `end_time` values in requests **must** be in the `YYYY-MM-DD HH:MM` format.
    * **Invalid Date Format Error Example:**
      
        {"error": "Invalid datetime format. UseAPAC-MM-DD HH:MM"}
      
**Missing Required Fields:** When you send a `POST` request with a missing `title`, `start_time`, or `end_time`, you will get:
  
    {"error": "Missing field: [field_name]"}

**Event Not Found:** If you attempt to update or delete an event by using an `event_id` that doesn't exist, you will get:

    {"error": "Event not found"}

**Production Use:** The development server provided by Flask is fine for local development and testing. For a production deployment, it's recommended to use a production-grade WSGI server such as Gunicorn or uWSGI.

---

## License

This project is open-source and licensed under the [MIT License](LICENSE).
````