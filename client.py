import requests
from typing import Dict, Optional, List
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def register_user(username: str, password: str, base_url: str = "http://localhost:8000") -> Dict:
    """
    Register a new user via the /register endpoint.

    Args:
        username (str): The username for registration
        password (str): The password for the user
        base_url (str): Base URL of the API server (default: http://localhost:8000)

    Returns:
        Dict: Response containing either success data or error information

    Raises:
        requests.RequestException: If there's a network error
        ValueError: If username or password is empty
    """
    if not username or not password:
        raise ValueError("Username and password are required")

    url = f"{base_url}/register"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "username": username,
        "password": password
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise exception for HTTP error codes

        # Success case - return the user data
        return {
            "success": True,
            "status_code": response.status_code,
            "data": response.json(),
            "message": "User registered successfully"
        }

    except requests.HTTPError as e:
        if response.status_code == 400:
            # Username already registered
            return {
                "success": False,
                "status_code": response.status_code,
                "error": "Username already registered",
                "message": response.text if response.text else "Bad request"
            }
        else:
            # Other HTTP errors
            return {
                "success": False,
                "status_code": response.status_code,
                "error": f"HTTP {response.status_code}",
                "message": response.text if response.text else "HTTP error"
            }

    except requests.RequestException as e:
        # Network or other request errors
        return {
            "success": False,
            "status_code": None,
            "error": "Request failed",
            "message": str(e)
        }


def login_user(username: str, password: str, base_url: str = "http://localhost:8000") -> Dict:
    """
    Login and get JWT token via the /login endpoint.

    Args:
        username (str): The username for login
        password (str): The password for the user
        base_url (str): Base URL of the API server (default: http://localhost:8000)

    Returns:
        Dict: Response containing either token data or error information

    Raises:
        ValueError: If username or password is empty
    """
    if not username or not password:
        raise ValueError("Username and password are required")

    url = f"{base_url}/login"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "username": username,
        "password": password
    }

    try:
        response = requests.post(url, data=data, headers=headers)
        response.raise_for_status()  # Raise exception for HTTP error codes

        # Success case - return the token data
        token_data = response.json()
        logger.info(f"Successfully logged in user: {username}")
        return {
            "success": True,
            "status_code": response.status_code,
            "data": token_data,
            "message": "Login successful"
        }

    except requests.HTTPError as e:
        if response.status_code == 400:
            # Incorrect username or password
            logger.warning(f"Failed login attempt for user: {username}")
            return {
                "success": False,
                "status_code": response.status_code,
                "error": "Invalid credentials",
                "message": "Incorrect username or password"
            }
        else:
            # Other HTTP errors
            logger.error(f"HTTP error during login: {response.status_code} - {response.text}")
            return {
                "success": False,
                "status_code": response.status_code,
                "error": f"HTTP {response.status_code}",
                "message": response.text if response.text else "HTTP error"
            }

    except requests.RequestException as e:
        # Network or other request errors
        logger.error(f"Request error during login: {str(e)}")
        return {
            "success": False,
            "status_code": None,
            "error": "Request failed",
            "message": str(e)
        }


def create_poll(question: str, options: List[str], token: str, base_url: str = "http://localhost:8000") -> Dict:
    """
    Create a new poll via the POST /polls endpoint (requires authentication).

    Args:
        question (str): The poll question
        options (List[str]): List of poll options
        token (str): JWT access token for authentication
        base_url (str): Base URL of the API server (default: http://localhost:8000)

    Returns:
        Dict: Response containing either poll data or error information

    Raises:
        ValueError: If question or options are invalid
    """
    if not question or not question.strip():
        raise ValueError("Question is required")
    if not options or len(options) < 2:
        raise ValueError("At least 2 options are required")
    if not token:
        raise ValueError("Authentication token is required")

    url = f"{base_url}/polls"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "question": question,
        "options": options
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise exception for HTTP error codes

        # Success case - return the poll data
        poll_data = response.json()
        logger.info(f"Successfully created poll: {question[:50]}...")
        return {
            "success": True,
            "status_code": response.status_code,
            "data": poll_data,
            "message": "Poll created successfully"
        }

    except requests.HTTPError as e:
        if response.status_code == 401:
            logger.warning("Unauthorized: Invalid or expired token")
            return {
                "success": False,
                "status_code": response.status_code,
                "error": "Unauthorized",
                "message": "Invalid or expired authentication token"
            }
        elif response.status_code == 422:
            logger.warning(f"Validation error: {response.text}")
            return {
                "success": False,
                "status_code": response.status_code,
                "error": "Validation error",
                "message": response.text if response.text else "Invalid request data"
            }
        else:
            # Other HTTP errors
            logger.error(f"HTTP error during poll creation: {response.status_code} - {response.text}")
            return {
                "success": False,
                "status_code": response.status_code,
                "error": f"HTTP {response.status_code}",
                "message": response.text if response.text else "HTTP error"
            }

    except requests.RequestException as e:
        # Network or other request errors
        logger.error(f"Request error during poll creation: {str(e)}")
        return {
            "success": False,
            "status_code": None,
            "error": "Request failed",
            "message": str(e)
        }


def get_polls(skip: int = 0, limit: int = 10, base_url: str = "http://localhost:8000") -> Dict:
    """
    Fetch paginated poll data from the /polls endpoint.

    Args:
        skip (int): Number of polls to skip for pagination (default: 0)
        limit (int): Maximum number of polls to return (default: 10)
        base_url (str): Base URL of the API server (default: http://localhost:8000)

    Returns:
        Dict: Response containing either poll data or error information

    Raises:
        ValueError: If skip or limit are negative
    """
    if skip < 0:
        raise ValueError("Skip must be a non-negative integer")
    if limit < 1:
        raise ValueError("Limit must be a positive integer")

    url = f"{base_url}/polls"
    params = {
        "skip": skip,
        "limit": limit
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise exception for HTTP error codes

        # Success case - return the polls data
        polls_data = response.json()
        return {
            "success": True,
            "status_code": response.status_code,
            "data": polls_data,
            "count": len(polls_data),
            "pagination": {
                "skip": skip,
                "limit": limit,
                "has_more": len(polls_data) == limit,
                "next_skip": skip + limit if len(polls_data) == limit else None
            },
            "message": f"Retrieved {len(polls_data)} polls successfully"
        }

    except requests.HTTPError as e:
        # Handle HTTP errors
        return {
            "success": False,
            "status_code": response.status_code,
            "error": f"HTTP {response.status_code}",
            "message": response.text if response.text else "HTTP error"
        }

    except requests.RequestException as e:
        # Network or other request errors
        return {
            "success": False,
            "status_code": None,
            "error": "Request failed",
            "message": str(e)
        }


def delete_poll(poll_id: int, token: str, base_url: str = "http://localhost:8000") -> Dict:
    """
    Delete a poll via the DELETE /polls/{poll_id} endpoint (requires authentication).

    Args:
        poll_id (int): The ID of the poll to delete
        token (str): JWT access token for authentication
        base_url (str): Base URL of the API server (default: http://localhost:8000)

    Returns:
        Dict: Response containing success/error information

    Raises:
        ValueError: If poll_id or token is invalid
    """
    if not isinstance(poll_id, int) or poll_id <= 0:
        raise ValueError("Valid poll ID is required")
    if not token:
        raise ValueError("Authentication token is required")

    url = f"{base_url}/polls/{poll_id}"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()  # Raise exception for HTTP error codes

        # Success case - poll deleted (204 No Content)
        logger.info(f"Successfully deleted poll ID: {poll_id}")
        return {
            "success": True,
            "status_code": response.status_code,
            "data": None,
            "message": "Poll deleted successfully"
        }

    except requests.HTTPError as e:
        if response.status_code == 401:
            logger.warning("Unauthorized: Invalid or expired token")
            return {
                "success": False,
                "status_code": response.status_code,
                "error": "Unauthorized",
                "message": "Invalid or expired authentication token"
            }
        elif response.status_code == 404:
            logger.warning(f"Poll not found: {poll_id}")
            return {
                "success": False,
                "status_code": response.status_code,
                "error": "Not found",
                "message": "Poll not found or not authorized"
            }
        else:
            # Other HTTP errors
            logger.error(f"HTTP error during poll deletion: {response.status_code} - {response.text}")
            return {
                "success": False,
                "status_code": response.status_code,
                "error": f"HTTP {response.status_code}",
                "message": response.text if response.text else "HTTP error"
            }

    except requests.RequestException as e:
        # Network or other request errors
        logger.error(f"Request error during poll deletion: {str(e)}")
        return {
            "success": False,
            "status_code": None,
            "error": "Request failed",
            "message": str(e)
        }


def vote_on_poll(poll_id: int, option_id: int, token: str, base_url: str = "http://localhost:8000") -> Dict:
    """
    Vote on a poll via the POST /polls/{poll_id}/vote endpoint (requires authentication).

    Args:
        poll_id (int): The ID of the poll to vote on
        option_id (int): The ID of the option to vote for
        token (str): JWT access token for authentication
        base_url (str): Base URL of the API server (default: http://localhost:8000)

    Returns:
        Dict: Response containing either vote data or error information

    Raises:
        ValueError: If poll_id, option_id, or token is invalid
    """
    if not isinstance(poll_id, int) or poll_id <= 0:
        raise ValueError("Valid poll ID is required")
    if not isinstance(option_id, int) or option_id <= 0:
        raise ValueError("Valid option ID is required")
    if not token:
        raise ValueError("Authentication token is required")

    url = f"{base_url}/polls/{poll_id}/vote"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "option_id": option_id
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise exception for HTTP error codes

        # Success case - return the vote data
        vote_data = response.json()
        logger.info(f"Successfully voted on poll {poll_id}, option {option_id}")
        return {
            "success": True,
            "status_code": response.status_code,
            "data": vote_data,
            "message": "Vote recorded successfully"
        }

    except requests.HTTPError as e:
        if response.status_code == 401:
            logger.warning("Unauthorized: Invalid or expired token")
            return {
                "success": False,
                "status_code": response.status_code,
                "error": "Unauthorized",
                "message": "Invalid or expired authentication token"
            }
        elif response.status_code == 404:
            logger.warning(f"Poll or option not found: poll_id={poll_id}, option_id={option_id}")
            return {
                "success": False,
                "status_code": response.status_code,
                "error": "Not found",
                "message": "Poll or option not found"
            }
        else:
            # Other HTTP errors
            logger.error(f"HTTP error during voting: {response.status_code} - {response.text}")
            return {
                "success": False,
                "status_code": response.status_code,
                "error": f"HTTP {response.status_code}",
                "message": response.text if response.text else "HTTP error"
            }

    except requests.RequestException as e:
        # Network or other request errors
        logger.error(f"Request error during voting: {str(e)}")
        return {
            "success": False,
            "status_code": None,
            "error": "Request failed",
            "message": str(e)
        }


def get_poll_results(poll_id: int, base_url: str = "http://localhost:8000") -> Dict:
    """
    Get poll results via the GET /polls/{poll_id}/results endpoint.

    Args:
        poll_id (int): The ID of the poll to get results for
        base_url (str): Base URL of the API server (default: http://localhost:8000)

    Returns:
        Dict: Response containing either poll results or error information

    Raises:
        ValueError: If poll_id is invalid
    """
    if not isinstance(poll_id, int) or poll_id <= 0:
        raise ValueError("Valid poll ID is required")

    url = f"{base_url}/polls/{poll_id}/results"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP error codes

        # Success case - return the poll results
        results_data = response.json()
        logger.info(f"Successfully retrieved results for poll ID: {poll_id}")
        return {
            "success": True,
            "status_code": response.status_code,
            "data": results_data,
            "message": f"Retrieved results for poll {poll_id}"
        }

    except requests.HTTPError as e:
        if response.status_code == 404:
            logger.warning(f"Poll not found: {poll_id}")
            return {
                "success": False,
                "status_code": response.status_code,
                "error": "Not found",
                "message": "Poll not found"
            }
        else:
            # Other HTTP errors
            logger.error(f"HTTP error during results retrieval: {response.status_code} - {response.text}")
            return {
                "success": False,
                "status_code": response.status_code,
                "error": f"HTTP {response.status_code}",
                "message": response.text if response.text else "HTTP error"
            }

    except requests.RequestException as e:
        # Network or other request errors
        logger.error(f"Request error during results retrieval: {str(e)}")
        return {
            "success": False,
            "status_code": None,
            "error": "Request failed",
            "message": str(e)
        }


# Example usage:
if __name__ == "__main__":
    # Test the register function
    print("=== Testing User Registration ===")
    register_result = register_user("testuser", "testpass")
    print(json.dumps(register_result, indent=2))

    print("\n=== Testing User Login ===")
    login_result = login_user("testuser", "testpass")
    print(json.dumps(login_result, indent=2))

    # Extract token for authenticated requests
    token = None
    if login_result["success"]:
        token = login_result["data"]["access_token"]
        print(f"\nToken obtained: {token[:20]}...")

        print("\n=== Testing Poll Creation ===")
        poll_result = create_poll(
            "What's your favorite programming language?",
            ["Python", "JavaScript", "Java", "Go"],
            token
        )
        print(json.dumps(poll_result, indent=2))

    print("\n=== Testing Get Polls ===")
    # Test the get polls function
    polls_result = get_polls(skip=0, limit=10)
    print(json.dumps(polls_result, indent=2))
