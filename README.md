# Instagram User ID Scraper

A Python scraper that fetches Instagram user IDs from usernames using authenticated Instagram accounts and proxy rotation to avoid rate limits.

## Features

- ✅ **Account Rotation**: Automatically rotates between multiple Instagram accounts
- ✅ **Proxy Rotation**: Supports rotating through multiple proxies
- ✅ **Rate Limit Handling**: Built-in delays and error handling
- ✅ **Session Management**: Uses cookies and session IDs from authenticated accounts
- ✅ **Automatic Retries**: Retries failed requests with different accounts/proxies
- ✅ **Statistics Tracking**: Monitors success rates and account health

## Installation

1. Clone or download this repository

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Setup

### 1. Get Instagram Session Cookies

To use this scraper, you need to extract cookies from an authenticated Instagram session.

**📖 Detailed Guide:** See [COOKIE_EXTRACTION_GUIDE.md](COOKIE_EXTRACTION_GUIDE.md) for step-by-step instructions with screenshots.

**Quick Method:**
1. Log into Instagram in your browser
2. Open Developer Tools (F12) → Console tab
3. Copy and paste the contents of `extract_cookies.js` into the console
4. Press Enter - the JSON will be copied to your clipboard!
5. Paste it into `accounts.json`

**Manual Method:**
1. Log into Instagram in your browser
2. Open Developer Tools (F12)
3. Go to the Application/Storage tab
4. Navigate to Cookies → `https://www.instagram.com`
5. Copy the following cookies:
   - `sessionid` (most important)
   - `csrftoken`
   - `ds_user_id`
   - `rur` (optional but recommended)

### 2. Configure Accounts

Create an `accounts.json` file (use `accounts.json.example` as a template):

```json
{
  "accounts": [
    {
      "name": "account1",
      "cookies": {
        "sessionid": "your_session_id_here",
        "csrftoken": "your_csrf_token_here",
        "ds_user_id": "your_user_id_here"
      },
      "session_id": "your_session_id_here",
      "user_agent": "Mozilla/5.0..."
    }
  ]
}
```

**Important**: Add multiple accounts for better rotation and to avoid rate limits.

### 3. Configure Proxies (Optional)

Create a `proxies.json` file (use `proxies.json.example` as a template):

```json
{
  "proxies": [
    {
      "host": "proxy.example.com",
      "port": 8080,
      "username": "proxy_user",
      "password": "proxy_password",
      "protocol": "http"
    }
  ]
}
```

## Usage

### Basic Usage

```python
from instagram_scraper import InstagramIDScraper, InstagramAccount, Proxy

# Create accounts
accounts = [
    InstagramAccount(
        name="account1",
        cookies={"sessionid": "YOUR_SESSION_ID"},
        session_id="YOUR_SESSION_ID"
    )
]

# Create scraper
scraper = InstagramIDScraper(accounts=accounts)

# Get single user ID
user_id = scraper.get_user_id("instagram")
print(f"User ID: {user_id}")

# Get multiple user IDs
results = scraper.get_user_ids(["instagram", "cristiano", "leomessi"])
print(results)
```

### Using JSON Configuration

```python
from instagram_scraper import InstagramIDScraper
from config_loader import load_accounts_from_json, load_proxies_from_json

# Load configuration
accounts = load_accounts_from_json("accounts.json")
proxies = load_proxies_from_json("proxies.json")

# Create scraper
scraper = InstagramIDScraper(accounts=accounts, proxies=proxies)

# Scrape user IDs
results = scraper.get_user_ids(["username1", "username2", "username3"])

# Check statistics
stats = scraper.get_stats()
print(stats)
```

### Batch Processing

See `example_usage.py` for examples of batch processing large lists of usernames.

## How It Works

1. **Account Selection**: The scraper selects the least-used active account
2. **Proxy Selection**: If proxies are configured, rotates through them
3. **Request**: Makes authenticated request to Instagram's API
4. **Fallback**: If API fails, falls back to HTML scraping
5. **Error Handling**: Tracks errors and deactivates problematic accounts/proxies
6. **Retry Logic**: Automatically retries with different accounts/proxies on failure

## Rate Limiting

The scraper includes built-in rate limiting:
- Random delays between requests (2-5 seconds by default)
- Automatic account switching on errors
- Account deactivation after too many errors

You can adjust these settings:

```python
scraper.min_delay = 3  # Minimum delay in seconds
scraper.max_delay = 7  # Maximum delay in seconds
scraper.max_errors_per_account = 5  # Errors before deactivating account
```

## API Reference

### InstagramIDScraper

Main scraper class.

**Methods:**
- `get_user_id(username, retries=3)`: Get user ID for a single username
- `get_user_ids(usernames, delay_between=None)`: Get user IDs for multiple usernames
- `get_stats()`: Get scraper statistics

### InstagramAccount

Represents an Instagram account with session data.

**Attributes:**
- `name`: Account identifier
- `cookies`: Dictionary of cookies
- `session_id`: Instagram session ID
- `user_agent`: Optional custom user agent
- `is_active`: Whether account is currently active
- `request_count`: Number of requests made with this account
- `error_count`: Number of errors encountered

### Proxy

Represents a proxy server.

**Attributes:**
- `host`: Proxy hostname
- `port`: Proxy port
- `username`: Optional proxy username
- `password`: Optional proxy password
- `protocol`: Protocol (http, https, socks5)

## Troubleshooting

### "No active accounts available"
- Check that your session IDs are valid and not expired
- Verify cookies are correctly formatted in `accounts.json`
- Instagram sessions expire after some time - you may need to refresh them

### Rate Limiting (429 errors)
- Add more accounts for rotation
- Increase delays between requests
- Use proxies to distribute requests
- Reduce the number of requests per minute

### Invalid Session (401 errors)
- Your session ID may have expired
- Log out and log back into Instagram, then extract new cookies
- Check that all required cookies are included

### Proxy Errors
- Verify proxy credentials and addresses
- Test proxies independently
- Some proxies may not work with Instagram - try different ones

## Security Notes

⚠️ **Important Security Considerations:**

- Never commit `accounts.json` or `proxies.json` to version control
- Keep your session IDs and proxy credentials secure
- Use environment variables for sensitive data in production
- Instagram may detect automated scraping - use responsibly

## License

This tool is for educational purposes only. Use responsibly and in accordance with Instagram's Terms of Service.

## Contributing

Feel free to submit issues or pull requests for improvements!

