"""
Instagram Followers Scraper
Fetches the list of followers for a given Instagram account
"""

import requests
import json
import time
import random
import re
import logging
from typing import List, Dict, Optional
from instagram_scraper import InstagramIDScraper, InstagramAccount
from config_loader import load_accounts_from_json

logger = logging.getLogger(__name__)


class InstagramFollowersScraper(InstagramIDScraper):
    """
    Extended scraper that can fetch followers lists
    """
    
    def get_followers(self, username: str, max_followers: Optional[int] = None) -> List[Dict]:
        """
        Get list of followers for a username
        
        Args:
            username: Instagram username (without @)
            max_followers: Maximum number of followers to fetch (None = all)
            
        Returns:
            List of follower dictionaries with 'username' and 'user_id'
        """
        username = username.lstrip('@').strip()
        
        # First, get the user ID
        user_id = self.get_user_id(username)
        if not user_id:
            logger.error(f"Could not get user ID for @{username}")
            return []
        
        logger.info(f"Found user ID for @{username}: {user_id}")
        
        # Get followers using GraphQL API
        return self._fetch_followers_graphql(user_id, username, max_followers)
    
    def _fetch_followers_graphql(self, user_id: str, username: str, max_followers: Optional[int] = None) -> List[Dict]:
        """
        Fetch followers using Instagram's GraphQL API
        """
        account = self._get_next_account()
        session = self._create_session(account)
        
        followers = []
        end_cursor = None
        has_next_page = True
        page_count = 0
        max_pages = 50  # Safety limit
        
        while has_next_page and (max_followers is None or len(followers) < max_followers):
            page_count += 1
            if page_count > max_pages:
                logger.warning(f"Reached maximum page limit ({max_pages})")
                break
            
            # GraphQL query for followers
            variables = {
                "id": user_id,
                "include_reel": False,
                "fetch_mutual": False,
                "first": 50  # Instagram typically returns 50 per page
            }
            
            if end_cursor:
                variables["after"] = end_cursor
            
            query_hash = "c76146de99bb02f6415203be841dd25a"  # Followers query hash
            
            url = f"https://www.instagram.com/graphql/query/?query_hash={query_hash}&variables={json.dumps(variables)}"
            
            try:
                headers = {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-IG-App-ID': '936619743392459',
                    'X-IG-WWW-Claim': '0',
                    'Referer': f'https://www.instagram.com/{username}/followers/',
                }
                session.headers.update(headers)
                
                response = session.get(url, timeout=30)
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        
                        # Parse followers from response
                        edges = data.get('data', {}).get('user', {}).get('edge_followed_by', {}).get('edges', [])
                        
                        for edge in edges:
                            node = edge.get('node', {})
                            follower_username = node.get('username', '')
                            follower_id = node.get('id', '')
                            
                            if follower_username:
                                followers.append({
                                    'username': follower_username,
                                    'user_id': follower_id,
                                    'full_name': node.get('full_name', ''),
                                    'is_verified': node.get('is_verified', False),
                                    'profile_pic_url': node.get('profile_pic_url', '')
                                })
                        
                        # Check for next page
                        page_info = data.get('data', {}).get('user', {}).get('edge_followed_by', {}).get('page_info', {})
                        has_next_page = page_info.get('has_next_page', False)
                        end_cursor = page_info.get('end_cursor')
                        
                        logger.info(f"Fetched page {page_count}: {len(edges)} followers (Total: {len(followers)})")
                        
                        # Stop if we have enough followers
                        if max_followers and len(followers) >= max_followers:
                            followers = followers[:max_followers]
                            break
                        
                        # Rate limiting delay
                        if has_next_page:
                            delay = random.uniform(3, 6)
                            time.sleep(delay)
                            
                    except (json.JSONDecodeError, KeyError) as e:
                        logger.error(f"Error parsing followers response: {e}")
                        break
                        
                elif response.status_code == 429:
                    logger.warning("Rate limited. Waiting longer...")
                    time.sleep(30)
                    continue
                else:
                    logger.warning(f"Failed to fetch followers: Status {response.status_code}")
                    # Try HTML fallback
                    return self._fetch_followers_html(username, max_followers)
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"Request error fetching followers: {e}")
                break
        
        logger.info(f"Total followers fetched: {len(followers)}")
        return followers
    
    def _fetch_followers_html(self, username: str, max_followers: Optional[int] = None) -> List[Dict]:
        """
        Fallback method: Try to extract followers from HTML page
        Note: This is less reliable as Instagram loads followers dynamically
        """
        account = self._get_next_account()
        session = self._create_session(account)
        
        url = f"https://www.instagram.com/{username}/followers/"
        
        try:
            response = session.get(url, timeout=30)
            
            if response.status_code == 200:
                # Handle Brotli compression
                content_encoding = response.headers.get('Content-Encoding', '').lower()
                if 'br' in content_encoding:
                    import brotli
                    content = brotli.decompress(response.content).decode('utf-8', errors='ignore')
                else:
                    content = response.text
                
                # Try to find followers in script tags
                followers = []
                
                # Look for JSON data in script tags
                script_pattern = r'<script[^>]*type=["\']application/json["\'][^>]*>(.*?)</script>'
                script_matches = re.findall(script_pattern, content, re.IGNORECASE | re.DOTALL)
                
                for script_content in script_matches:
                    try:
                        script_data = json.loads(script_content)
                        # Recursively search for followers data
                        followers_data = self._find_followers_in_json(script_data)
                        if followers_data:
                            followers.extend(followers_data)
                            if max_followers and len(followers) >= max_followers:
                                followers = followers[:max_followers]
                                break
                    except (json.JSONDecodeError, TypeError):
                        continue
                
                if followers:
                    logger.info(f"Found {len(followers)} followers via HTML parsing")
                    return followers
                    
        except Exception as e:
            logger.error(f"Error fetching followers from HTML: {e}")
        
        return []
    
    def _find_followers_in_json(self, data: any) -> List[Dict]:
        """Recursively search for followers data in JSON structure"""
        followers = []
        
        if isinstance(data, dict):
            # Look for followers/edges structure
            if 'edges' in data and isinstance(data['edges'], list):
                for edge in data['edges']:
                    if isinstance(edge, dict) and 'node' in edge:
                        node = edge['node']
                        if 'username' in node:
                            followers.append({
                                'username': node.get('username', ''),
                                'user_id': node.get('id', ''),
                                'full_name': node.get('full_name', ''),
                                'is_verified': node.get('is_verified', False)
                            })
            
            # Recursively search in values
            for value in data.values():
                result = self._find_followers_in_json(value)
                if result:
                    followers.extend(result)
                    
        elif isinstance(data, list):
            for item in data:
                result = self._find_followers_in_json(item)
                if result:
                    followers.extend(result)
        
        return followers


def main():
    """CLI for fetching followers"""
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description="Fetch Instagram followers")
    parser.add_argument("username", help="Instagram username")
    parser.add_argument("--max", type=int, help="Maximum number of followers to fetch")
    parser.add_argument("--output", "-o", help="Output file (JSON)")
    parser.add_argument("--accounts-file", default="accounts.json", help="Accounts JSON file")
    
    args = parser.parse_args()
    
    # Load accounts
    try:
        accounts = load_accounts_from_json(args.accounts_file)
        if not accounts:
            print("Error: No accounts found", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"Error loading accounts: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Create scraper
    scraper = InstagramFollowersScraper(accounts=accounts)
    
    print(f"Fetching followers for @{args.username}...")
    if args.max:
        print(f"Limit: {args.max} followers")
    
    followers = scraper.get_followers(args.username, max_followers=args.max)
    
    if not followers:
        print("No followers found or account not accessible", file=sys.stderr)
        sys.exit(1)
    
    # Output results
    output_data = {
        "username": args.username,
        "total_followers": len(followers),
        "followers": followers
    }
    
    output_json = json.dumps(output_data, indent=2)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output_json)
        print(f"\n✓ Saved {len(followers)} followers to {args.output}")
    else:
        print(f"\nFound {len(followers)} followers:")
        print(output_json)
    
    # Also save as CSV-friendly format
    if args.output:
        csv_file = args.output.replace('.json', '.csv')
        with open(csv_file, 'w') as f:
            f.write("username,user_id,full_name,is_verified\n")
            for follower in followers:
                f.write(f"{follower['username']},{follower.get('user_id', '')},{follower.get('full_name', '').replace(',', ' ')},{follower.get('is_verified', False)}\n")
        print(f"✓ Also saved CSV format to {csv_file}")


if __name__ == "__main__":
    main()

