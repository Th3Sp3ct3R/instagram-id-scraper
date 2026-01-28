"""Debug script to inspect Instagram HTML structure"""
from instagram_scraper import InstagramIDScraper
from config_loader import load_accounts_from_json
import requests

accounts = load_accounts_from_json("accounts.json")
scraper = InstagramIDScraper(accounts=accounts)

# Get a session
account = accounts[0]
session = scraper._create_session(account)

# Fetch HTML
username = "instagram"
url = f"https://www.instagram.com/{username}/"
response = session.get(url, timeout=30)

if response.status_code == 200:
    content = response.text
    print(f"HTML Length: {len(content)}")
    print(f"\nFirst 2000 characters:")
    print(content[:2000])
    print(f"\n\nLooking for patterns...")
    
    # Check for various patterns
    patterns_to_check = [
        'window._sharedData',
        'profilePage_',
        '"id":"',
        '"user_id":"',
        '"pk":"',
        'application/json',
    ]
    
    for pattern in patterns_to_check:
        if pattern in content:
            print(f"✓ Found: {pattern}")
            # Show context around first occurrence
            idx = content.find(pattern)
            start = max(0, idx - 100)
            end = min(len(content), idx + 500)
            print(f"  Context: ...{content[start:end]}...\n")
        else:
            print(f"✗ Not found: {pattern}")
    
    # Save HTML to file for inspection
    with open("debug_html.html", "w", encoding="utf-8") as f:
        f.write(content)
    print(f"\nHTML saved to debug_html.html")
else:
    print(f"Failed to fetch: Status {response.status_code}")




