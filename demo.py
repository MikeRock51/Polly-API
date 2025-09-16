#!/usr/bin/env python3
"""
Complete Polly-API Client Usage Example
This demonstrates a full workflow from user registration to poll management.
"""

import json
from client import (
    register_user, login_user, create_poll, get_polls,
    vote_on_poll, get_poll_results, delete_poll
)

def main():
    print("🚀 Polly-API Client Demo")
    print("=" * 50)

    # Step 1: Register a new user
    print("\n📝 Step 1: Registering new user...")
    register_result = register_user("demo_user", "secure_password")

    if not register_result["success"]:
        print(f"❌ Registration failed: {register_result['message']}")
        return

    print(f"✅ {register_result['message']}")
    print(f"   User ID: {register_result['data']['id']}")

    # Step 2: Login to get authentication token
    print("\n🔐 Step 2: Logging in...")
    login_result = login_user("demo_user", "secure_password")

    if not login_result["success"]:
        print(f"❌ Login failed: {login_result['message']}")
        return

    token = login_result["data"]["access_token"]
    print(f"✅ Login successful!")
    print(f"   Token: {token[:20]}...")

    # Step 3: Create a new poll
    print("\n📊 Step 3: Creating a poll...")
    poll_result = create_poll(
        question="What's your favorite season?",
        options=["Spring", "Summer", "Autumn", "Winter"],
        token=token
    )

    if not poll_result["success"]:
        print(f"❌ Poll creation failed: {poll_result['message']}")
        return

    poll_id = poll_result["data"]["id"]
    print(f"✅ Poll created successfully!")
    print(f"   Poll ID: {poll_id}")
    print(f"   Question: {poll_result['data']['question']}")

    # Step 4: Get all polls (including the new one)
    print("\n📋 Step 4: Fetching all polls...")
    polls_result = get_polls(limit=5)

    if polls_result["success"]:
        print(f"✅ Retrieved {polls_result['count']} polls")
        for poll in polls_result["data"]:
            print(f"   • Poll {poll['id']}: {poll['question']}")

    # Step 5: Vote on the poll
    print(f"\n🗳️  Step 5: Voting on poll {poll_id}...")
    vote_result = vote_on_poll(
        poll_id=poll_id,
        option_id=poll_result["data"]["options"][0]["id"],  # Vote for first option
        token=token
    )

    if vote_result["success"]:
        print("✅ Vote recorded successfully!")
    else:
        print(f"❌ Voting failed: {vote_result['message']}")

    # Step 6: Get poll results
    print(f"\n📈 Step 6: Getting results for poll {poll_id}...")
    results_result = get_poll_results(poll_id)

    if results_result["success"]:
        results = results_result["data"]
        print(f"✅ Results for: {results['question']}")
        print("   Current standings:")
        for result in results["results"]:
            print(f"   • {result['text']}: {result['vote_count']} votes")
    else:
        print(f"❌ Failed to get results: {results_result['message']}")

    # Step 7: Clean up - delete the poll
    print(f"\n🗑️  Step 7: Deleting poll {poll_id}...")
    delete_result = delete_poll(poll_id, token)

    if delete_result["success"]:
        print("✅ Poll deleted successfully!")
    else:
        print(f"❌ Deletion failed: {delete_result['message']}")

    print("\n🎉 Demo completed successfully!")

if __name__ == "__main__":
    main()
