"""Quick script to check if an Instagram account exists and is accessible"""
from instagram_scraper import InstagramIDScraper
from config_loader import load_accounts_from_json
import requests

username = "fincacieloazul"

# Load accounts
accounts = load_accounts_from_json("accounts.json")
scraper = InstagramIDScraper(accounts=accounts)
account = accounts[0]
session = scraper._create_session(account)

# Test 1: Check if account exists
print(f"Checking @{username}...")
print("\n1. Testing session validity...")
test_id = scraper.get_user_id("instagram")
if test_id:
    print(f"   ✓ Session is valid (tested with @instagram: {test_id})")
else:
    print("   ✗ Session may be expired - cookies need refreshing")

# Test 2: Try accessing the account
print(f"\n2. Attempting to access @{username}...")
url = f"https://www.instagram.com/{username}/"
response = session.get(url, allow_redirects=False, timeout=30)

print(f"   Status Code: {response.status_code}")
print(f"   Location Header: {response.headers.get('Location', 'None')}")

if response.status_code == 302:
    location = response.headers.get('Location', '')
    if '/accounts/login' in location:
        print("   ⚠ Redirected to login - account may be private or cookies expired")
    elif location == 'https://www.instagram.com/' or location == '/':
        print("   ⚠ Redirected to homepage - account may not exist or is private")
    else:
        print(f"   Redirected to: {location}")
elif response.status_code == 200:
    print("   ✓ Account page accessible!")
    # Try to get user ID
    user_id = scraper.get_user_id(username)
    if user_id:
        print(f"   ✓ User ID found: {user_id}")
    else:
        print("   ⚠ Page accessible but couldn't extract user ID")
elif response.status_code == 404:
    print("   ✗ Account not found (404)")
else:
    print(f"   ⚠ Unexpected status: {response.status_code}")

print("\n3. Recommendations:")
print("   - If session is invalid: Extract fresh cookies")
print("   - If account is private: Make sure you're logged in with an account that follows @fincacieloazul")
print("   - If account doesn't exist: Verify the username is correct")



