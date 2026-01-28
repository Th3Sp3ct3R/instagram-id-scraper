#!/usr/bin/env python3
"""
Helper script to merge multiple account JSON files into one accounts.json
Usage:
  1. Extract cookies from each account using extract_cookies.js
  2. Save each output to account1.json, account2.json, etc.
  3. Run: python merge_accounts.py
"""

import json
import os
import glob
from pathlib import Path

def load_account_file(file_path):
    """Load a single account JSON file"""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            # Handle both formats: direct account object or wrapped in accounts array
            if 'accounts' in data:
                return data['accounts'][0]
            elif 'name' in data or 'sessionid' in data.get('cookies', {}):
                return data
            else:
                print(f"Warning: Unknown format in {file_path}")
                return None
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

def merge_accounts():
    """Merge all account JSON files into accounts.json"""
    
    # Find all account JSON files
    account_files = sorted(glob.glob("account*.json"))
    
    if not account_files:
        print("No account*.json files found!")
        print("\nTo use this script:")
        print("1. Extract cookies from each Instagram account using extract_cookies.js")
        print("2. Save each output to account1.json, account2.json, etc.")
        print("3. Run this script again")
        return
    
    print(f"Found {len(account_files)} account file(s):")
    for f in account_files:
        print(f"  - {f}")
    
    accounts = []
    
    for i, file_path in enumerate(account_files, 1):
        account_data = load_account_file(file_path)
        if account_data:
            # Ensure account has a name
            if 'name' not in account_data:
                account_data['name'] = f"account{i}"
            
            # Ensure session_id matches sessionid cookie
            if 'session_id' not in account_data and 'cookies' in account_data:
                account_data['session_id'] = account_data['cookies'].get('sessionid', '')
            
            accounts.append(account_data)
            print(f"✓ Loaded {account_data.get('name', f'account{i}')}")
        else:
            print(f"✗ Failed to load {file_path}")
    
    if not accounts:
        print("\nNo valid accounts found. Please check your account files.")
        return
    
    # Create the final accounts.json structure
    output = {
        "accounts": accounts
    }
    
    # Save to accounts.json
    output_path = "accounts.json"
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n✓ Successfully merged {len(accounts)} account(s) into {output_path}")
    print(f"\nYou can now use the scraper with all {len(accounts)} accounts!")
    print("\nTest it with:")
    print("  python scraper_cli.py instagram --stats")

if __name__ == "__main__":
    merge_accounts()



