# Step-by-Step: Adding 10 Instagram Accounts

## 🎯 Goal
Extract cookies from 10 Instagram accounts and add them all to `accounts.json` for automatic rotation.

---

## Method 1: Using Helper Scripts (Recommended - Easiest)

### Step 1: Extract Cookies from Each Account

**For EACH of your 10 accounts:**

1. **Log into Instagram** (Account #1, then #2, etc.)
2. **Open Developer Tools**: Press `F12` (or `Cmd+Option+I` on Mac)
3. **Go to Console tab**
4. **Copy the entire contents** of `extract_single_account.js`
5. **Paste into the console** and press Enter
6. **When prompted**, enter the account number (1, 2, 3, etc.)
7. **Copy the JSON output** that appears
8. **Save it to a file**:
   - Account 1 → `account1.json`
   - Account 2 → `account2.json`
   - Account 3 → `account3.json`
   - ... continue for all 10 accounts

**Repeat steps 1-8 for all 10 accounts.**

💡 **Tip**: Use incognito/private windows or different browsers to keep multiple accounts logged in simultaneously.

### Step 2: Merge All Accounts

Once you have `account1.json` through `account10.json`:

```bash
python merge_accounts.py
```

This will automatically:
- Read all `account*.json` files
- Combine them into one `accounts.json`
- Verify all accounts are properly formatted

### Step 3: Verify Setup

Test that all 10 accounts are loaded:

```bash
source venv/bin/activate
python scraper_cli.py instagram --stats
```

You should see:
- `"total_accounts": 10`
- `"active_accounts": 10`

---

## Method 2: Manual Setup

### Step 1: Extract Cookies Manually

For each account, extract cookies using Developer Tools:

1. Log into Instagram
2. F12 → Application tab → Cookies → `https://www.instagram.com`
3. Copy these values:
   - `sessionid`
   - `csrftoken`
   - `ds_user_id`
   - `rur` (optional)
4. Get User-Agent: Console tab → type `navigator.userAgent` → copy result
5. Log out and repeat for next account

### Step 2: Create accounts.json

Open `accounts.json` and add all 10 accounts:

```json
{
  "accounts": [
    {
      "name": "account1",
      "cookies": {
        "sessionid": "PASTE_ACCOUNT_1_SESSIONID",
        "csrftoken": "PASTE_ACCOUNT_1_CSRFTOKEN",
        "ds_user_id": "PASTE_ACCOUNT_1_DS_USER_ID",
        "rur": "PASTE_ACCOUNT_1_RUR"
      },
      "session_id": "PASTE_ACCOUNT_1_SESSIONID",
      "user_agent": "PASTE_ACCOUNT_1_USER_AGENT"
    },
    {
      "name": "account2",
      "cookies": {
        "sessionid": "PASTE_ACCOUNT_2_SESSIONID",
        "csrftoken": "PASTE_ACCOUNT_2_CSRFTOKEN",
        "ds_user_id": "PASTE_ACCOUNT_2_DS_USER_ID",
        "rur": "PASTE_ACCOUNT_2_RUR"
      },
      "session_id": "PASTE_ACCOUNT_2_SESSIONID",
      "user_agent": "PASTE_ACCOUNT_2_USER_AGENT"
    }
    // ... add accounts 3-10 following the same pattern
  ]
}
```

---

## ⚡ Quick Workflow (Fastest)

### Using Multiple Browser Windows:

1. **Open 10 incognito/private browser windows**
2. **Log into a different Instagram account in each window**
3. **In each window:**
   - F12 → Console
   - Paste `extract_single_account.js`
   - Enter account number (1-10)
   - Copy JSON output
   - Save to `account1.json`, `account2.json`, etc.
4. **Run merge script:**
   ```bash
   python merge_accounts.py
   ```
5. **Done!** All 10 accounts are now in `accounts.json`

---

## ✅ Verification Checklist

After setup, verify:

- [ ] All 10 account files exist (`account1.json` through `account10.json`)
- [ ] `accounts.json` contains 10 accounts
- [ ] Each account has `sessionid`, `csrftoken`, `ds_user_id`
- [ ] `session_id` matches `sessionid` cookie value
- [ ] Test shows 10 active accounts: `python scraper_cli.py instagram --stats`

---

## 🚨 Common Issues

### Issue: "No active accounts available"
- **Solution**: Cookies may have expired. Extract fresh cookies.

### Issue: "Invalid JSON" error
- **Solution**: Check that all JSON files are valid. Use a JSON validator.

### Issue: Account not working
- **Solution**: 
  1. Verify cookies are correct
  2. Make sure you extracted cookies while logged in
  3. Try extracting fresh cookies

### Issue: Can't extract from multiple accounts
- **Solution**: Use incognito windows or different browsers for each account

---

## 📊 Expected Results

With 10 accounts configured, you'll see:

- **Faster scraping**: Can reduce delays between requests
- **Better reliability**: If one account gets rate-limited, others continue
- **Higher success rate**: More accounts = more requests before hitting limits
- **Automatic rotation**: Scraper automatically uses the least-used account

---

## 🎉 Next Steps

Once all 10 accounts are set up:

1. **Test the scraper:**
   ```bash
   python scraper_cli.py instagram cristiano leomessi --stats
   ```

2. **Run your full list:**
   ```bash
   python scraper_cli.py [all your usernames] --output results.json --stats
   ```

3. **Monitor performance:**
   - Check `--stats` output to see account rotation
   - Watch for any accounts getting deactivated
   - If accounts get deactivated, extract fresh cookies

---

## 📝 File Structure

After setup, you should have:

```
Instagram ID Scraper/
├── accounts.json          ← Final file with all 10 accounts
├── account1.json         ← Individual account (can delete after merge)
├── account2.json         ← Individual account (can delete after merge)
├── ...
├── account10.json        ← Individual account (can delete after merge)
├── merge_accounts.py     ← Helper script
└── extract_single_account.js ← Extraction script
```

You can delete the individual `account*.json` files after merging if you want to keep things clean.



