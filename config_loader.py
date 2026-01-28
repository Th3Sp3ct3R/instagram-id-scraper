"""
Configuration loader for Instagram accounts and proxies
Supports loading from JSON files or environment variables
"""

import json
import os
from typing import List, Dict
from instagram_scraper import InstagramAccount, Proxy


def load_accounts_from_json(file_path: str) -> List[InstagramAccount]:
    """
    Load Instagram accounts from a JSON file
    
    Expected JSON format:
    {
        "accounts": [
            {
                "name": "account1",
                "cookies": {
                    "sessionid": "your_session_id_here",
                    "csrftoken": "your_csrf_token_here",
                    ...
                },
                "session_id": "your_session_id_here",
                "user_agent": "optional_user_agent"
            },
            ...
        ]
    }
    """
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    accounts = []
    for acc_data in data.get('accounts', []):
        account = InstagramAccount(
            name=acc_data['name'],
            cookies=acc_data.get('cookies', {}),
            session_id=acc_data.get('session_id', acc_data.get('cookies', {}).get('sessionid', '')),
            user_agent=acc_data.get('user_agent')
        )
        accounts.append(account)
    
    return accounts


def load_proxies_from_json(file_path: str) -> List[Proxy]:
    """
    Load proxies from a JSON file
    
    Expected JSON format:
    {
        "proxies": [
            {
                "host": "proxy.example.com",
                "port": 8080,
                "username": "optional_username",
                "password": "optional_password",
                "protocol": "http"
            },
            ...
        ]
    }
    """
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    proxies = []
    for proxy_data in data.get('proxies', []):
        proxy = Proxy(
            host=proxy_data['host'],
            port=proxy_data['port'],
            username=proxy_data.get('username'),
            password=proxy_data.get('password'),
            protocol=proxy_data.get('protocol', 'http')
        )
        proxies.append(proxy)
    
    return proxies


def load_accounts_from_env() -> List[InstagramAccount]:
    """
    Load Instagram accounts from environment variables
    
    Expected format:
    INSTAGRAM_ACCOUNTS='[{"name": "acc1", "cookies": {...}, "session_id": "..."}, ...]'
    """
    accounts_json = os.getenv('INSTAGRAM_ACCOUNTS')
    if not accounts_json:
        return []
    
    data = json.loads(accounts_json)
    accounts = []
    for acc_data in data:
        account = InstagramAccount(
            name=acc_data['name'],
            cookies=acc_data.get('cookies', {}),
            session_id=acc_data.get('session_id', acc_data.get('cookies', {}).get('sessionid', '')),
            user_agent=acc_data.get('user_agent')
        )
        accounts.append(account)
    
    return accounts


def load_proxies_from_env() -> List[Proxy]:
    """
    Load proxies from environment variables
    
    Expected format:
    INSTAGRAM_PROXIES='[{"host": "proxy.com", "port": 8080, ...}, ...]'
    """
    proxies_json = os.getenv('INSTAGRAM_PROXIES')
    if not proxies_json:
        return []
    
    data = json.loads(proxies_json)
    proxies = []
    for proxy_data in data:
        proxy = Proxy(
            host=proxy_data['host'],
            port=proxy_data['port'],
            username=proxy_data.get('username'),
            password=proxy_data.get('password'),
            protocol=proxy_data.get('protocol', 'http')
        )
        proxies.append(proxy)
    
    return proxies





