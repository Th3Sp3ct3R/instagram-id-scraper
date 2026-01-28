# Quick Guide: Extracting Cookies from 10 Instagram Accounts

## Fastest Method (Using Browser Console)

### Setup: Use Incognito/Private Windows

**Option 1: Multiple Incognito Windows (Easiest)**
- Open 10 separate incognito/private browser windows
- Log into a different Instagram account in each window
- Extract cookies from each window without logging out

**Option 2: Single Browser (More Manual)**
- Log into Account 1 → Extract → Log out
- Log into Account 2 → Extract → Log out
- Repeat for all 10 accounts

### Steps for Each Account:

1. **Open Instagram** in the browser (logged into the account)
2. **Press F12** to open Developer Tools
3. **Click the Console tab**
4. **Copy and paste this code:**

```javascript
// Quick extractor - copy this entire block
(function() {
  const cookies = document.cookie.split(';').reduce((acc, cookie) => {
    const [name, value] = cookie.trim().split('=');
    acc[name] = decodeURIComponent(value);
    return acc;
  }, {});
  
  const account = {
    name: `account${prompt('Account number? (1-10)', '1')}`,
    cookies: {
      sessionid: cookies.sessionid || '',
      csrftoken: cookies.csrftoken || '',
      ds_user_id: cookies.ds_user_id || '',
      rur: cookies.rur || ''
    },
    session_id: cookies.sessionid || '',
    user_agent: navigator.userAgent
  };
  
  console.log('\n=== COPY THIS JSON ===\n');
  console.log(JSON.stringify(account, null, 2));
  console.log('\n=== END ===\n');
  
  navigator.clipboard.writeText(JSON.stringify(account, null, 2))
    .then(() => console.log('✓ Copied to clipboard!'))
    .catch(() => console.log('⚠ Please copy manually'));
  
  return account;
})();
```

5. **Press Enter**
6. **When prompted, enter the account number** (1, 2, 3, etc.)
7. **Copy the JSON output** that appears
8. **Save it to a file**: `account1.json`, `account2.json`, etc.

### After Extracting All 10 Accounts:

Run the merge script:

```bash
python merge_accounts.py
```

This will automatically combine all `account*.json` files into `accounts.json`!

## Alternative: Manual Method

If you prefer to manually create the file:

1. Extract cookies from each account (see COOKIE_EXTRACTION_GUIDE.md)
2. Open `accounts.json.example` as a template
3. Copy the account object structure 10 times
4. Fill in each account's cookies

## Pro Tips:

- **Use different browsers**: Chrome, Firefox, Edge, Safari - one account per browser
- **Use browser profiles**: Create separate browser profiles for each account
- **Extract all at once**: If using incognito windows, extract from all 10 before closing
- **Label clearly**: Name your account files clearly (account1.json, account2.json, etc.)
- **Test each account**: After merging, test that all accounts work

## Verification:

After setting up all accounts, verify:

```bash
python scraper_cli.py instagram --stats
```

You should see:
- `"total_accounts": 10`
- `"active_accounts": 10`

If any accounts show as inactive, their cookies may have expired - extract fresh ones!



