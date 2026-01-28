# Setting Up Multiple Instagram Accounts

This guide will help you add 10 Instagram accounts to your scraper for better rotation and rate limit avoidance.

## Step-by-Step Process

### Step 1: Extract Cookies from Each Account

For each of your 10 Instagram accounts, follow these steps:

#### Method A: Using the Browser Console Script (Easiest)

1. **Log into Instagram Account #1** in your browser
2. Open Developer Tools (F12) → **Console** tab
3. Copy and paste the contents of `extract_cookies.js` into the console
4. Press Enter
5. Copy the JSON output that appears
6. **Save it somewhere** (text file, notes app, etc.) - label it as "Account 1"
7. **Log out** of Instagram

8. **Repeat steps 1-7** for each of your 10 accounts:
   - Account 2: Log in → Extract → Save → Log out
   - Account 3: Log in → Extract → Save → Log out
   - ... continue for all 10 accounts

#### Method B: Manual Extraction

1. **Log into Instagram Account #1**
2. Open Developer Tools (F12) → **Application** tab → **Cookies** → `https://www.instagram.com`
3. Copy these cookie values:
   - `sessionid`
   - `csrftoken`
   - `ds_user_id`
   - `rur` (optional)
4. Note your browser's User-Agent (Console tab → type `navigator.userAgent`)
5. **Log out**

6. **Repeat for all 10 accounts**

### Step 2: Combine All Accounts into accounts.json

Once you have cookies from all 10 accounts, create your `accounts.json` file:

```json
{
  "accounts": [
    {
      "name": "account1",
      "cookies": {
        "sessionid": "PASTE_ACCOUNT_1_SESSIONID_HERE",
        "csrftoken": "PASTE_ACCOUNT_1_CSRFTOKEN_HERE",
        "ds_user_id": "PASTE_ACCOUNT_1_DS_USER_ID_HERE",
        "rur": "PASTE_ACCOUNT_1_RUR_HERE"
      },
      "session_id": "PASTE_ACCOUNT_1_SESSIONID_HERE",
      "user_agent": "PASTE_ACCOUNT_1_USER_AGENT_HERE"
    },
    {
      "name": "account2",
      "cookies": {
        "sessionid": "PASTE_ACCOUNT_2_SESSIONID_HERE",
        "csrftoken": "PASTE_ACCOUNT_2_CSRFTOKEN_HERE",
        "ds_user_id": "PASTE_ACCOUNT_2_DS_USER_ID_HERE",
        "rur": "PASTE_ACCOUNT_2_RUR_HERE"
      },
      "session_id": "PASTE_ACCOUNT_2_SESSIONID_HERE",
      "user_agent": "PASTE_ACCOUNT_2_USER_AGENT_HERE"
    }
    // ... add accounts 3-10 following the same pattern
  ]
}
```

### Step 3: Use the Helper Script (Recommended)

I've created a helper script `merge_accounts.py` that makes this easier:

1. Extract cookies from each account using `extract_cookies.js`
2. Save each JSON output to separate files: `account1.json`, `account2.json`, etc.
3. Run the merge script to combine them all

See the script for details.

## Quick Tips

### ⚠️ Important Notes:

1. **Extract cookies while logged in** - Cookies are only valid when you're actively logged into Instagram
2. **Use different browsers or incognito windows** - This makes it easier to switch between accounts
3. **Label everything clearly** - Keep track of which cookies belong to which account
4. **Extract cookies fresh** - Don't use old cookies, they expire quickly
5. **Keep cookies secure** - Never share or commit `accounts.json` to public repositories

### 🔄 Account Rotation Benefits:

With 10 accounts, the scraper will:
- Automatically rotate between accounts
- Reduce rate limiting (each account makes fewer requests)
- Continue working if one account gets temporarily blocked
- Process requests much faster (can reduce delays)

### 📝 Example Workflow:

```
Account 1: Extract → Save to account1.json
Account 2: Extract → Save to account2.json
Account 3: Extract → Save to account3.json
...
Account 10: Extract → Save to account10.json

Then run: python merge_accounts.py
```

## Testing Your Setup

After adding all accounts, test with:

```bash
source venv/bin/activate
python scraper_cli.py instagram --stats
```

Check the statistics to see all 10 accounts are active!



