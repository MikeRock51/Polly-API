# Polly-API: FastAPI Poll Application

A comprehensive poll application built with FastAPI, SQLite, and JWT authentication. Users can register, log in, create, retrieve, vote on, and delete polls. The project includes both a FastAPI server and a Python client library for easy API integration.

## Features

### Server Features
- User registration and login (JWT authentication)
- Create, retrieve, and delete polls
- Add options to polls (minimum of two options required)
- Vote on polls (authenticated users only)
- View poll results with vote counts
- SQLite database with SQLAlchemy ORM
- Modular code structure for maintainability
- Comprehensive error handling and logging

### Client Features
- Complete Python client library (`client.py`)
- All API endpoints supported
- JWT authentication handling
- Comprehensive error handling with detailed logging
- Type hints for better IDE support
- Pagination support for poll retrieval
- Easy-to-use functions for all operations

## Project Structure

```
Polly-API/
├── api/
│   ├── __init__.py
│   ├── auth.py
│   ├── database.py
│   ├── models.py
│   ├── routes.py
│   └── schemas.py
├── client.py          # 🆕 Python client library
├── main.py
├── polls.db           # SQLite database (created automatically)
├── requirements.txt
├── openapi.yaml       # OpenAPI specification
└── README.md
```

## Setup Instructions

1. **Clone the repository**

```bash
git clone <your-repo-url>
cd Polly-API
```

2. **Set up a Python virtual environment (recommended)**

A virtual environment helps isolate your project dependencies.

- **On Unix/macOS:**

  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

- **On Windows (cmd):**

  ```cmd
  python -m venv venv
  venv\Scripts\activate
  ```

- **On Windows (PowerShell):**

  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```

To deactivate the virtual environment, simply run:

```bash
deactivate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set environment variables (optional)**

Create a `.env` file in the project root to override the default secret key:

```
SECRET_KEY=your_super_secret_key
```

5. **Run the application**

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## API Usage

### 1. Register a new user

- **Endpoint:** `POST /register`
- **Body:**

```json
{
  "username": "yourusername",
  "password": "yourpassword"
}
```

### 2. Login

- **Endpoint:** `POST /login`
- **Body (form):**
  - `username`: yourusername
  - `password`: yourpassword
- **Response:**

```json
{
  "access_token": "...",
  "token_type": "bearer"
}
```

### 3. Get all polls

- **Endpoint:** `GET /polls`
- **Query params:** `skip` (default 0), `limit` (default 10)
- **Authentication:** Not required

### 4. Create a poll

- **Endpoint:** `POST /polls`
- **Headers:** `Authorization: Bearer <access_token>`
- **Body:**

```json
{
  "question": "Your poll question",
  "options": ["Option 1", "Option 2"]
}
```

### 5. Get a specific poll

- **Endpoint:** `GET /polls/{poll_id}`
- **Authentication:** Not required

### 6. Vote on a poll

- **Endpoint:** `POST /polls/{poll_id}/vote`
- **Headers:** `Authorization: Bearer <access_token>`
- **Body:**

```json
{
  "option_id": 1
}
```

### 7. Get poll results

- **Endpoint:** `GET /polls/{poll_id}/results`
- **Authentication:** Not required
- **Response:**

```json
{
  "poll_id": 1,
  "question": "Your poll question",
  "results": [
    {
      "option_id": 1,
      "text": "Option 1",
      "vote_count": 3
    },
    {
      "option_id": 2,
      "text": "Option 2",
      "vote_count": 1
    }
  ]
}
```

### 8. Delete a poll

- **Endpoint:** `DELETE /polls/{poll_id}`
- **Headers:** `Authorization: Bearer <access_token>`

## Using the Python Client Library

The project includes a comprehensive Python client library (`client.py`) that makes it easy to interact with the API programmatically.

### Client Setup

```python
from client import (
    register_user, login_user, create_poll, get_polls,
    delete_poll, vote_on_poll, get_poll_results
)
```

### Client Usage Examples

#### 1. User Registration and Login

```python
# Register a new user
register_result = register_user("myusername", "mypassword")
print(register_result["message"])  # "User registered successfully"

# Login to get JWT token
login_result = login_user("myusername", "mypassword")
if login_result["success"]:
    token = login_result["data"]["access_token"]
    print("Login successful!")
```

#### 2. Create and Manage Polls

```python
# Create a new poll (requires authentication)
poll_result = create_poll(
    question="What's your favorite programming language?",
    options=["Python", "JavaScript", "Java", "Go", "Rust"],
    token=token
)
if poll_result["success"]:
    poll_id = poll_result["data"]["id"]
    print(f"Poll created with ID: {poll_id}")
```

#### 3. Retrieve Polls with Pagination

```python
# Get polls with pagination
polls_result = get_polls(skip=0, limit=10)
if polls_result["success"]:
    polls = polls_result["data"]
    print(f"Retrieved {len(polls)} polls")

    # Check if there are more results
    if polls_result["pagination"]["has_more"]:
        next_result = get_polls(skip=10, limit=10)
```

#### 4. Vote on a Poll

```python
# Vote on a poll (requires authentication)
vote_result = vote_on_poll(
    poll_id=1,
    option_id=2,  # ID of the option to vote for
    token=token
)
if vote_result["success"]:
    print("Vote recorded successfully!")
```

#### 5. Get Poll Results

```python
# Get results for a specific poll (no authentication required)
results_result = get_poll_results(poll_id=1)
if results_result["success"]:
    results = results_result["data"]
    print(f"Poll: {results['question']}")
    for result in results["results"]:
        print(f"{result['text']}: {result['vote_count']} votes")
```

#### 6. Delete a Poll

```python
# Delete a poll (requires authentication)
delete_result = delete_poll(poll_id=1, token=token)
if delete_result["success"]:
    print("Poll deleted successfully!")
```

### Error Handling

All client functions return a consistent response structure:

```python
{
    "success": bool,
    "status_code": int or None,
    "data": dict or None,
    "message": str,
    "error": str or None  # Only present if success is False
}
```

Example error handling:

```python
result = create_poll("Question", ["Option1"], token)
if not result["success"]:
    if result["status_code"] == 401:
        print("Authentication failed - please login again")
    elif result["status_code"] == 422:
        print("Validation error:", result["message"])
    else:
        print("Error:", result["message"])
```

### Advanced Client Usage

```python
# Custom base URL
result = register_user("user", "pass", base_url="https://your-api.com")

# Handle pagination programmatically
all_polls = []
skip = 0
limit = 20

while True:
    result = get_polls(skip=skip, limit=limit)
    if not result["success"]:
        break

    all_polls.extend(result["data"])
    if not result["pagination"]["has_more"]:
        break

    skip = result["pagination"]["next_skip"]
```

## Testing the Client Library

You can test the client library by running the built-in test examples:

```bash
# Make sure the server is running
uvicorn main:app --reload

# In another terminal, run the client tests
python client.py
```

This will execute a series of tests demonstrating:
- User registration and login
- Poll creation with authentication
- Poll retrieval with pagination
- Error handling for various scenarios

The test output will show structured JSON responses with success/error information and detailed logging.

## Development and Contributing

### Code Quality
- Follow PEP 8 style guidelines
- Use type hints for better IDE support
- Include comprehensive docstrings
- Handle errors gracefully with meaningful messages

### Testing
- Test both server and client functionality
- Verify authentication flows
- Test pagination and error scenarios
- Use the built-in client tests as examples

## Interactive API Docs

Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for the interactive Swagger UI.

## License

MIT License
