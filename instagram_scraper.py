"""
Instagram User ID Scraper with Account and Proxy Rotation
Fetches user IDs from Instagram usernames using authenticated sessions
"""

import requests
import json
import time
import random
import re
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class InstagramAccount:
    """Represents an Instagram account with its session data"""
    name: str
    cookies: Dict[str, str]
    session_id: str
    user_agent: Optional[str] = None
    is_active: bool = True
    last_used: Optional[datetime] = None
    request_count: int = 0
    error_count: int = 0


@dataclass
class Proxy:
    """Represents a proxy server"""
    host: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None
    protocol: str = "http"
    is_active: bool = True
    error_count: int = 0
    
    def to_dict(self) -> Dict[str, str]:
        """Convert proxy to dictionary format for requests"""
        if self.username and self.password:
            proxy_url = f"{self.protocol}://{self.username}:{self.password}@{self.host}:{self.port}"
        else:
            proxy_url = f"{self.protocol}://{self.host}:{self.port}"
        return {
            "http": proxy_url,
            "https": proxy_url
        }


class InstagramIDScraper:
    """
    Instagram User ID Scraper with account and proxy rotation
    """
    
    def __init__(self, accounts: List[InstagramAccount], proxies: Optional[List[Proxy]] = None):
        """
        Initialize the scraper with accounts and optional proxies
        
        Args:
            accounts: List of InstagramAccount objects with cookies/session IDs
            proxies: Optional list of Proxy objects for rotation
        """
        self.accounts = accounts
        self.proxies = proxies or []
        self.current_account_index = 0
        self.current_proxy_index = 0
        
        # Rate limiting settings
        self.min_delay = 2  # Minimum seconds between requests
        self.max_delay = 5  # Maximum seconds between requests
        self.max_errors_per_account = 10  # Switch account after this many errors
        
        # Statistics
        self.stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "account_switches": 0,
            "proxy_switches": 0
        }
    
    def _get_next_account(self) -> InstagramAccount:
        """Get the next available account in rotation"""
        active_accounts = [acc for acc in self.accounts if acc.is_active]
        
        if not active_accounts:
            raise Exception("No active accounts available")
        
        # Find account with least recent usage
        account = min(active_accounts, key=lambda a: a.request_count)
        self.current_account_index = self.accounts.index(account)
        
        return account
    
    def _get_next_proxy(self) -> Optional[Proxy]:
        """Get the next available proxy in rotation"""
        if not self.proxies:
            return None
        
        active_proxies = [p for p in self.proxies if p.is_active]
        
        if not active_proxies:
            logger.warning("No active proxies available, continuing without proxy")
            return None
        
        proxy = active_proxies[self.current_proxy_index % len(active_proxies)]
        self.current_proxy_index = (self.current_proxy_index + 1) % len(active_proxies)
        
        return proxy
    
    def _create_session(self, account: InstagramAccount, proxy: Optional[Proxy] = None) -> requests.Session:
        """Create a requests session with account cookies and optional proxy"""
        session = requests.Session()
        
        # Set cookies
        session.cookies.update(account.cookies)
        
        # Set headers
        headers = {
            'User-Agent': account.user_agent or 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'Referer': 'https://www.instagram.com/',
        }
        session.headers.update(headers)
        
        # Set proxy if provided
        if proxy:
            session.proxies.update(proxy.to_dict())
        
        return session
    
    def _find_user_id_in_json(self, data: any, username: str) -> Optional[str]:
        """Recursively search for user ID in JSON structure"""
        if isinstance(data, dict):
            # Check if this dict has both id and username matching
            if 'id' in data and 'username' in data:
                if str(data.get('username', '')).lower() == username.lower():
                    user_id = str(data.get('id', ''))
                    if user_id.isdigit() and len(user_id) >= 8:
                        return user_id
            # Recursively search in values
            for value in data.values():
                result = self._find_user_id_in_json(value, username)
                if result:
                    return result
        elif isinstance(data, list):
            for item in data:
                result = self._find_user_id_in_json(item, username)
                if result:
                    return result
        return None
    
    def _fetch_user_id(self, username: str, account: InstagramAccount, proxy: Optional[Proxy] = None) -> Optional[str]:
        """
        Fetch user ID for a given username using the provided account and proxy
        
        Args:
            username: Instagram username (without @)
            account: InstagramAccount to use for the request
            proxy: Optional Proxy to use
            
        Returns:
            User ID as string, or None if failed
        """
        session = self._create_session(account, proxy)
        
        # Method 1: Try scraping HTML page first (more reliable)
        url = f"https://www.instagram.com/{username}/"
        
        try:
            # Handle redirects manually to avoid infinite loops
            max_redirects = 5
            redirect_count = 0
            final_url = url
            
            while redirect_count < max_redirects:
                response = session.get(final_url, timeout=30, allow_redirects=False)
                
                # Handle redirects
                if response.status_code in [301, 302, 303, 307, 308]:
                    redirect_count += 1
                    location = response.headers.get('Location', '')
                    if location:
                        final_url = location
                        # Handle relative URLs
                        if final_url.startswith('/'):
                            final_url = f"https://www.instagram.com{final_url}"
                        # Check if redirecting to login (account might be private/invalid)
                        if '/accounts/login' in final_url.lower():
                            logger.warning(f"Redirected to login page - account @{username} may be private or invalid")
                            return None
                        continue
                    else:
                        break
                elif response.status_code == 200:
                    break
                else:
                    # Not a redirect, break and handle normally
                    break
            
            if response.status_code == 200:
                # Try to extract user ID from page source
                # Handle Brotli compression (Instagram uses 'br' encoding)
                content_encoding = response.headers.get('Content-Encoding', '').lower()
                content = None
                
                if 'br' in content_encoding or 'brotli' in content_encoding:
                    # Instagram uses Brotli compression
                    try:
                        import brotli
                        content = brotli.decompress(response.content).decode('utf-8', errors='ignore')
                    except ImportError:
                        logger.warning("brotli module not installed. Install with: pip install brotli")
                        # Try to use response.text (may fail)
                        content = response.text
                    except Exception as e:
                        logger.debug(f"Brotli decompression failed: {e}")
                        content = response.text
                elif 'gzip' in content_encoding:
                    import gzip
                    try:
                        content = gzip.decompress(response.content).decode('utf-8', errors='ignore')
                    except Exception as e:
                        logger.debug(f"Gzip decompression failed: {e}")
                        content = response.text
                else:
                    # No compression or already decompressed by requests
                    content = response.text
                
                # Fallback: if content still looks binary, try manual decompression
                if content and len(content) > 0 and (ord(content[0]) < 32 or not content[:200].isprintable()):
                    try:
                        import brotli
                        content = brotli.decompress(response.content).decode('utf-8', errors='ignore')
                    except:
                        try:
                            import gzip
                            content = gzip.decompress(response.content).decode('utf-8', errors='ignore')
                        except:
                            content = response.content.decode('utf-8', errors='ignore')
                
                # Method 1: Look for window._sharedData pattern (older Instagram)
                if 'window._sharedData' in content:
                    start = content.find('window._sharedData = ') + len('window._sharedData = ')
                    end = content.find(';</script>', start)
                    if end > start:
                        try:
                            data_str = content[start:end]
                            data = json.loads(data_str)
                            user_id = data.get('entry_data', {}).get('ProfilePage', [{}])[0].get('graphql', {}).get('user', {}).get('id')
                            if user_id:
                                logger.info(f"Successfully fetched ID for @{username} via _sharedData: {user_id}")
                                return str(user_id)
                        except (json.JSONDecodeError, KeyError, IndexError) as e:
                            logger.debug(f"Failed to parse _sharedData: {e}")
                
                # Method 2: Look for profilePage pattern
                if '"profilePage_' in content:
                    start = content.find('"profilePage_') + len('"profilePage_')
                    end = content.find('"', start)
                    if end > start:
                        user_id = content[start:end]
                        logger.info(f"Successfully fetched ID for @{username} via profilePage pattern: {user_id}")
                        return user_id
                
                # Method 3: Look for various JSON patterns in script tags
                # Try to find JSON data structures containing user info
                json_patterns = [
                    # Pattern: "id":"123456789" near username
                    r'"id":"(\d+)"[^}]{0,500}?"username":"' + re.escape(username) + '"',
                    r'"username":"' + re.escape(username) + r'"[^}]{0,500}?"id":"(\d+)"',
                    # Pattern: profilePage_123456789
                    r'"profilePage_(\d+)"',
                    # Pattern: "user_id":"123456789"
                    r'"user_id":"(\d+)"',
                    # Pattern: "owner":{"id":"123456789"}
                    r'"owner":\s*\{\s*"id":"(\d+)"',
                    # Pattern: "profile_id":"123456789"
                    r'"profile_id":"(\d+)"',
                    # Pattern: "pk":"123456789" (primary key)
                    r'"pk":"(\d+)"[^}]{0,500}?"username":"' + re.escape(username) + '"',
                    r'"username":"' + re.escape(username) + r'"[^}]{0,500}?"pk":"(\d+)"',
                ]
                
                for pattern in json_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
                    if matches:
                        # Filter matches - user IDs are typically 8-15 digits
                        for match in matches:
                            if match.isdigit() and len(match) >= 8:
                                user_id = match
                                logger.info(f"Successfully fetched ID for @{username} via JSON pattern: {user_id}")
                                return user_id
                
                # Method 4: Look for script tags with JSON data
                script_tag_pattern = r'<script[^>]*type=["\']application/json["\'][^>]*>(.*?)</script>'
                script_matches = re.findall(script_tag_pattern, content, re.IGNORECASE | re.DOTALL)
                for script_content in script_matches:
                    try:
                        script_data = json.loads(script_content)
                        # Recursively search for user ID in JSON structure
                        user_id = self._find_user_id_in_json(script_data, username)
                        if user_id:
                            logger.info(f"Successfully fetched ID for @{username} via script JSON: {user_id}")
                            return str(user_id)
                    except (json.JSONDecodeError, TypeError):
                        continue
                
                # Method 5: Look for data attributes or meta tags
                meta_patterns = [
                    r'<meta[^>]*property=["\']al:ios:url["\'][^>]*content=["\'].*?/user/(\d+)/',
                    r'data-user-id=["\'](\d+)["\']',
                ]
                for pattern in meta_patterns:
                    match = re.search(pattern, content, re.IGNORECASE)
                    if match:
                        user_id = match.group(1)
                        if user_id.isdigit() and len(user_id) >= 8:
                            logger.info(f"Successfully fetched ID for @{username} via meta/data pattern: {user_id}")
                            return user_id
                
                logger.debug(f"Could not find user ID in HTML for @{username}. HTML length: {len(content)}")
            
            # If we get here, the request didn't succeed
            if response.status_code == 429:
                logger.warning(f"Rate limited (429) for account {account.name}")
                account.error_count += 1
            elif response.status_code == 401:
                logger.warning(f"Unauthorized (401) for account {account.name} - session may be invalid")
                account.error_count += 1
            elif response.status_code == 404:
                logger.warning(f"User @{username} not found (404)")
                # Don't count 404 as an account error - user just doesn't exist
            else:
                logger.warning(f"Failed to fetch ID for @{username}: Status {response.status_code}")
                account.error_count += 1
            
            return None
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error for @{username}: {e}")
            account.error_count += 1
            if proxy:
                proxy.error_count += 1
            return None
    
    def get_user_id(self, username: str, retries: int = 3) -> Optional[str]:
        """
        Get user ID for a username with automatic account/proxy rotation
        
        Args:
            username: Instagram username (without @)
            retries: Number of retries with different accounts/proxies
            
        Returns:
            User ID as string, or None if all retries failed
        """
        username = username.lstrip('@').strip()
        
        for attempt in range(retries):
            try:
                # Get account and proxy
                account = self._get_next_account()
                proxy = self._get_next_proxy()
                
                logger.info(f"Attempt {attempt + 1}/{retries} for @{username} using account {account.name}")
                
                # Fetch user ID
                user_id = self._fetch_user_id(username, account, proxy)
                
                # Update statistics
                self.stats["total_requests"] += 1
                account.request_count += 1
                account.last_used = datetime.now()
                
                if user_id:
                    self.stats["successful_requests"] += 1
                    return user_id
                else:
                    self.stats["failed_requests"] += 1
                    
                    # Check if account should be deactivated
                    if account.error_count >= self.max_errors_per_account:
                        logger.warning(f"Deactivating account {account.name} due to too many errors")
                        account.is_active = False
                    
                    # Check if proxy should be deactivated
                    if proxy and proxy.error_count >= self.max_errors_per_account:
                        logger.warning(f"Deactivating proxy {proxy.host}:{proxy.port} due to too many errors")
                        proxy.is_active = False
                
                # Random delay before retry
                if attempt < retries - 1:
                    delay = random.uniform(self.min_delay, self.max_delay)
                    logger.info(f"Waiting {delay:.2f}s before retry...")
                    time.sleep(delay)
                    
            except Exception as e:
                logger.error(f"Unexpected error for @{username}: {e}")
                self.stats["failed_requests"] += 1
        
        logger.error(f"Failed to fetch ID for @{username} after {retries} attempts")
        return None
    
    def get_user_ids(self, usernames: List[str], delay_between: Optional[float] = None) -> Dict[str, Optional[str]]:
        """
        Get user IDs for multiple usernames
        
        Args:
            usernames: List of Instagram usernames
            delay_between: Optional delay between requests (uses random delay if None)
            
        Returns:
            Dictionary mapping usernames to their IDs (or None if failed)
        """
        results = {}
        
        for i, username in enumerate(usernames):
            user_id = self.get_user_id(username)
            results[username] = user_id
            
            # Delay between requests (except for the last one)
            if i < len(usernames) - 1:
                if delay_between is None:
                    delay = random.uniform(self.min_delay, self.max_delay)
                else:
                    delay = delay_between
                time.sleep(delay)
        
        return results
    
    def get_stats(self) -> Dict:
        """Get scraper statistics"""
        return {
            **self.stats,
            "active_accounts": sum(1 for acc in self.accounts if acc.is_active),
            "total_accounts": len(self.accounts),
            "active_proxies": sum(1 for p in self.proxies if p.is_active) if self.proxies else 0,
            "total_proxies": len(self.proxies) if self.proxies else 0,
        }


