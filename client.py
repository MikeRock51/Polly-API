import requests
from typing import Dict, Optional
import json


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


# Example usage:
if __name__ == "__main__":
    # Test the function
    result = register_user("testuser", "testpass")
    print(json.dumps(result, indent=2))
