# Integration Guide: Using Instagram Scraper in Another Codebase

## Minimal Files Required

To use the Instagram scraper in another codebase, you only need:

### **Required Files:**
1. **`instagram_scraper.py`** - The main scraper module (standalone)
2. **`requirements.txt`** - Python dependencies

### **Optional Files:**
- **`config_loader.py`** - Only needed if you want to load accounts/proxies from JSON files. You can create `InstagramAccount` and `Proxy` objects manually instead.

## Dependencies

The scraper requires:
- **`requests`** (required) - For HTTP requests
- **`brotli`** (optional but recommended) - Helps decompress Instagram's Brotli-compressed responses

All other imports are from Python's standard library.

## How to Pull Specific Files from GitHub

### Method 1: Using GitHub's Raw URLs (Recommended)

Download only the files you need:

```bash
# In your target codebase directory
curl -O https://raw.githubusercontent.com/Th3Sp3ct3R/instagram-id-scraper/main/instagram_scraper.py
curl -O https://raw.githubusercontent.com/Th3Sp3ct3R/instagram-id-scraper/main/requirements.txt

# Optional: If you want config_loader for JSON file support
curl -O https://raw.githubusercontent.com/Th3Sp3ct3R/instagram-id-scraper/main/config_loader.py
```

### Method 2: Using Git Sparse Checkout

```bash
# In your target codebase directory
mkdir instagram-scraper
cd instagram-scraper
git init
git remote add origin https://github.com/Th3Sp3ct3R/instagram-id-scraper.git
git config core.sparseCheckout true

# Specify which files/folders to checkout
echo "instagram_scraper.py" >> .git/info/sparse-checkout
echo "requirements.txt" >> .git/info/sparse-checkout
echo "config_loader.py" >> .git/info/sparse-checkout  # Optional

# Pull the files
git pull origin main
```

### Method 3: Using GitHub CLI

```bash
# Download specific files
gh repo download Th3Sp3ct3R/instagram-id-scraper --dir temp --include instagram_scraper.py,requirements.txt,config_loader.py
# Then copy the files to your project
```

### Method 4: Manual Copy

1. Go to: https://github.com/Th3Sp3ct3R/instagram-id-scraper
2. Click on each file (`instagram_scraper.py`, `requirements.txt`)
3. Click "Raw" button
4. Copy the content and save to your project

## Usage Examples

### Minimal Usage (Without config_loader)

```python
from instagram_scraper import InstagramIDScraper, InstagramAccount

# Create account manually
accounts = [
    InstagramAccount(
        name="account1",
        cookies={
            "sessionid": "YOUR_SESSION_ID",
            "csrftoken": "YOUR_CSRF_TOKEN",
            "ds_user_id": "YOUR_USER_ID"
        },
        session_id="YOUR_SESSION_ID"
    )
]

# Initialize scraper
scraper = InstagramIDScraper(accounts=accounts)

# Get user ID
user_id = scraper.get_user_id("instagram")
print(f"User ID: {user_id}")

# Get multiple user IDs
results = scraper.get_user_ids(["username1", "username2"])
```

### With config_loader (If you downloaded it)

```python
from instagram_scraper import InstagramIDScraper
from config_loader import load_accounts_from_json

# Load accounts from JSON
accounts = load_accounts_from_json("accounts.json")

# Initialize scraper
scraper = InstagramIDScraper(accounts=accounts)

# Use the scraper
user_id = scraper.get_user_id("instagram")
```

## Installation

After copying the files, install dependencies:

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install requests brotli
```

## File Dependencies

- **`instagram_scraper.py`** - ✅ Standalone, no internal file dependencies
- **`config_loader.py`** - ⚠️ Depends on `instagram_scraper.py` (imports `InstagramAccount` and `Proxy`)

## What You DON'T Need

You can safely ignore these files (they're just helpers/documentation):
- `scraper_cli.py` - CLI wrapper (optional)
- `example_usage.py` - Examples (optional)
- `check_account.py` - Testing utility (optional)
- All `.md` files - Documentation (optional)
- `extract_*.js` files - Cookie extraction helpers (optional)

## Summary

**Minimum to make it work:**
1. Copy `instagram_scraper.py` to your project
2. Install `requests` (and optionally `brotli`)
3. Create `InstagramAccount` objects with your Instagram session cookies
4. Use `InstagramIDScraper.get_user_id(username)` or `get_user_ids(usernames)`

That's it! The scraper is self-contained and doesn't need any other files from the repo.
