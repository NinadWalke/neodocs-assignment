# neodocs-assignment

*Backend Engineer Assessment – Local HTTP API using Python standard library and SQLite.*

---


## Prerequisites

- Python 3.10+

- SQLite (bundled with Python)

- Unix-like shell (Linux / macOS)

## Setup & Run Instructions

1. Create database directory

```bash
mkdir -p data
```

2. Set environment variables

```bash
export DATABASE_PATH=./data/tests.db
export SERVER_HOST=127.0.0.1
export SERVER_PORT=8000
```

3. Initialize the database

```bash
python scripts/init_db.py
```

Expected output:

```bash
Database initialized successfully.
```

4. Start the server

Run from the project root:

```bash
python -m app.server
```

Expected output:

```bash
Server running on http://127.0.0.1:8000
```

---

## API Usage

### Insert a test record (POST /tests)

```bash
curl -X POST http://127.0.0.1:8000/tests \
  -H "Content-Type: application/json" \
  -d '{
    "test_id": "t123",
    "patient_id": "p001",
    "clinic_id": "c001",
    "test_type": "CBC",
    "result": "Normal"
  }'
```

Expected response:

- HTTP 201 Created

- JSON response containing a request_id

Duplicate test_id will return:

- HTTP 409 Conflict

### Fetch tests by clinic (GET /tests)

```bash
curl "http://127.0.0.1:8000/tests?clinic_id=c001"
```

Expected response:

- HTTP 200 OK

- JSON list of tests (empty list if none found)

Missing clinic_id:

- HTTP 400 Bad Request

---

## Design Questions

---

1. Why did you choose this framework?

--- 

- I chose this framework because we get full control over request parsing which in turn helps us to parse the data as need for the `test report`. We can customize it the way we wantt exactly.

- Since the constraints also mentioned to refrain from using Flask, ORMs, etc and also a standard library ensures minimal dependencies, we can also force explicit handling of validation and therefore it comes in handy. 

- That is why I chose http.server

---

2. Where can this system fail?

---

- This system can fail when there's invalid input. 

- As we're using no ORMs and directly interacting with the DB, constraint violations can sometimes cause a failure on the backend.

---

3. How would you debug a data inconsistency issue?

---

- We can use structured logs to trace the exact inconsistency occurence and reason for the same.
- We'll then reproduce the issue against a local database.
- We'll monitor the lifecycle and figure out the exact point of the transaction where it is inconsistent.
- Finally, we'll modify and fix that lifecycle, test it again against a local DB and then push it to prodction.

---

4. What would change in production vs local?

---

- In production, we'll replace SQLite with either Postgres or MongoDB Atlas.
- We'll add proper metrics and logs for each transaction
- We'll need to integrate frameworks like Flask to avoid reinventing the wheel and write cleaner and scalable code
- We'll also need to implement authentication, we're already validating requests but we have to ensure they're coming from an authorized party.