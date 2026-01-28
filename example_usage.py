"""
Example usage of the Instagram ID Scraper
"""

from instagram_scraper import InstagramIDScraper, InstagramAccount, Proxy
from config_loader import load_accounts_from_json, load_proxies_from_json
import json


def example_basic_usage():
    """Basic usage example with manual account/proxy setup"""
    
    # Create Instagram accounts with cookies/session IDs
    accounts = [
        InstagramAccount(
            name="account1",
            cookies={
                "sessionid": "YOUR_SESSION_ID_HERE",
                "csrftoken": "YOUR_CSRF_TOKEN_HERE",
                # Add other cookies from your browser session
            },
            session_id="YOUR_SESSION_ID_HERE",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        ),
        # Add more accounts for rotation
    ]
    
    # Optional: Create proxies for rotation
    proxies = [
        Proxy(
            host="proxy.example.com",
            port=8080,
            username="proxy_user",  # Optional
            password="proxy_pass",  # Optional
            protocol="http"
        ),
        # Add more proxies for rotation
    ]
    
    # Initialize scraper
    scraper = InstagramIDScraper(accounts=accounts, proxies=proxies)
    
    # Get single user ID
    user_id = scraper.get_user_id("instagram")
    print(f"User ID: {user_id}")
    
    # Get multiple user IDs
    usernames = ["instagram", "cristiano", "leomessi"]
    results = scraper.get_user_ids(usernames)
    
    print("\nResults:")
    for username, user_id in results.items():
        print(f"@{username}: {user_id}")
    
    # Print statistics
    print("\nScraper Statistics:")
    print(json.dumps(scraper.get_stats(), indent=2))


def example_json_config():
    """Example using JSON configuration files"""
    
    # Load accounts and proxies from JSON files
    try:
        accounts = load_accounts_from_json("accounts.json")
        proxies = load_proxies_from_json("proxies.json")
    except FileNotFoundError as e:
        print(f"Configuration file not found: {e}")
        print("Please create accounts.json and/or proxies.json")
        return
    
    # Initialize scraper
    scraper = InstagramIDScraper(accounts=accounts, proxies=proxies)
    
    # Scrape user IDs
    usernames = ["instagram", "cristiano", "leomessi"]
    results = scraper.get_user_ids(usernames)
    
    # Save results to file
    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("Results saved to results.json")
    print("\nScraper Statistics:")
    print(json.dumps(scraper.get_stats(), indent=2))


def example_batch_processing():
    """Example for processing a large list of usernames"""
    import os
    
    # Load configuration
    accounts = load_accounts_from_json("accounts.json")
    proxies = load_proxies_from_json("proxies.json") if os.path.exists("proxies.json") else None
    
    scraper = InstagramIDScraper(accounts=accounts, proxies=proxies)
    
    # Read usernames from file (one per line)
    with open("usernames.txt", "r") as f:
        usernames = [line.strip() for line in f if line.strip()]
    
    # Process in batches
    batch_size = 10
    all_results = {}
    
    for i in range(0, len(usernames), batch_size):
        batch = usernames[i:i + batch_size]
        print(f"\nProcessing batch {i // batch_size + 1} ({len(batch)} usernames)...")
        
        batch_results = scraper.get_user_ids(batch)
        all_results.update(batch_results)
        
        # Save progress after each batch
        with open("results.json", "w") as f:
            json.dump(all_results, f, indent=2)
        
        print(f"Progress: {len(all_results)}/{len(usernames)} completed")
        print(f"Stats: {scraper.get_stats()}")


if __name__ == "__main__":
    import os
    
    # Choose which example to run
    if os.path.exists("accounts.json"):
        example_json_config()
    else:
        print("Running basic usage example...")
        print("Note: Update the session IDs and cookies before running!")
        # example_basic_usage()  # Uncomment and update with real credentials

