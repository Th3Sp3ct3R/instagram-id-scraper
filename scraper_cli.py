#!/usr/bin/env python3
"""
Command-line interface for Instagram User ID Scraper
"""

import argparse
import json
import sys
from pathlib import Path
from instagram_scraper import InstagramIDScraper
from config_loader import load_accounts_from_json, load_proxies_from_json


def main():
    parser = argparse.ArgumentParser(
        description="Instagram User ID Scraper with Account and Proxy Rotation"
    )
    
    parser.add_argument(
        "usernames",
        nargs="+",
        help="Instagram usernames to scrape (without @)"
    )
    
    parser.add_argument(
        "--accounts-file",
        default="accounts.json",
        help="Path to accounts JSON file (default: accounts.json)"
    )
    
    parser.add_argument(
        "--proxies-file",
        help="Path to proxies JSON file (optional)"
    )
    
    parser.add_argument(
        "--output",
        "-o",
        help="Output file path (JSON format). If not specified, prints to stdout"
    )
    
    parser.add_argument(
        "--delay",
        type=float,
        help="Fixed delay between requests in seconds (default: random 2-5s)"
    )
    
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Print scraper statistics after completion"
    )
    
    args = parser.parse_args()
    
    # Load accounts
    if not Path(args.accounts_file).exists():
        print(f"Error: Accounts file not found: {args.accounts_file}", file=sys.stderr)
        print("Please create accounts.json (see accounts.json.example)", file=sys.stderr)
        sys.exit(1)
    
    try:
        accounts = load_accounts_from_json(args.accounts_file)
        if not accounts:
            print("Error: No accounts found in configuration file", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"Error loading accounts: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Load proxies (optional)
    proxies = None
    if args.proxies_file:
        if not Path(args.proxies_file).exists():
            print(f"Warning: Proxies file not found: {args.proxies_file}", file=sys.stderr)
        else:
            try:
                proxies = load_proxies_from_json(args.proxies_file)
            except Exception as e:
                print(f"Warning: Error loading proxies: {e}", file=sys.stderr)
    
    # Initialize scraper
    scraper = InstagramIDScraper(accounts=accounts, proxies=proxies)
    
    # Clean usernames (remove @ if present)
    usernames = [u.lstrip('@').strip() for u in args.usernames]
    
    print(f"Scraping {len(usernames)} username(s) using {len(accounts)} account(s)...")
    if proxies:
        print(f"Using {len(proxies)} proxy/proxies")
    
    # Scrape user IDs
    results = scraper.get_user_ids(usernames, delay_between=args.delay)
    
    # Prepare output
    output_data = {
        "results": results,
        "summary": {
            "total": len(results),
            "successful": sum(1 for v in results.values() if v is not None),
            "failed": sum(1 for v in results.values() if v is None)
        }
    }
    
    if args.stats:
        output_data["statistics"] = scraper.get_stats()
    
    # Output results
    output_json = json.dumps(output_data, indent=2)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output_json)
        print(f"\nResults saved to {args.output}")
    else:
        print("\nResults:")
        print(output_json)
    
    # Print summary
    print(f"\nSummary: {output_data['summary']['successful']}/{output_data['summary']['total']} successful")


if __name__ == "__main__":
    main()





