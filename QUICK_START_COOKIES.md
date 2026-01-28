# Quick Start: Extract Cookies for Your 2 Accounts

## 🚀 Fastest Method (5 minutes)

### Account 1: ffddnn87

1. **Open Chrome/Firefox/Safari**
2. **Go to:** [instagram.com](https://www.instagram.com)
3. **Log in:**
   - Username: `ffddnn87`
   - Password: `Aged#123`
4. **Press F12** (or right-click → Inspect)
5. **Click "Console" tab**
6. **Open** `extract_single_account.js` file
7. **Copy ALL the code** (Ctrl+A, Ctrl+C / Cmd+A, Cmd+C)
8. **Paste into console** (Ctrl+V / Cmd+V)
9. **Press Enter**
10. **When prompted**, type: `1` and press Enter
11. **Copy the JSON** that appears (it's automatically copied to clipboard!)
12. **Create file:** `account1.json` in your project folder
13. **Paste JSON** into the file and save

### Account 2: Email Account

1. **Open NEW incognito/private window** (or different browser)
2. **Go to:** [instagram.com](https://www.instagram.com)
3. **Log in:**
   - Email: `ffddnn87@gmail.com`
   - Password: `Aged#8181`
4. **Press F12** → **Console** tab
5. **Paste** `extract_single_account.js` → Press Enter
6. **Enter:** `2` when prompted
7. **Copy JSON** output
8. **Save to:** `account2.json`

### Merge Accounts

```bash
cd "/Users/growthgod/Documents/Repos/Instagram ID Scraper _Suggestuser_scraper"
python merge_accounts.py
```

### Test It

```bash
source venv/bin/activate
python scraper_cli.py instagram --stats
```

Should show: `"total_accounts": 2` ✅

---

## 📍 Where to Save Files

Save `account1.json` and `account2.json` in:

```
/Users/growthgod/Documents/Repos/Instagram ID Scraper _Suggestuser_scraper/
```

---

## 🎯 What You're Looking For

After running the script, you should see:

```
=== COPY THIS JSON ===

{
  "name": "account1",
  "cookies": {
    "sessionid": "47119281269%3AN6F7fhYlim3f0J...",
    "csrftoken": "Te8ontIDTj1cNHyVTzZg1OoL3DNfZxby",
    "ds_user_id": "47119281269",
    "rur": "EAG\\05447119281269..."
  },
  "session_id": "47119281269%3AN6F7fhYlim3f0J...",
  "user_agent": "Mozilla/5.0..."
}

=== END ===
```

**Copy everything between the `{` and `}`** (including the braces!)

---

## ⚠️ Important Notes

- **Must be logged in** - Extract cookies while actively logged into Instagram
- **Don't log out** - Keep the browser tab open while extracting
- **Use incognito** - For second account, use private/incognito window to avoid conflicts
- **Save immediately** - Cookies can expire, save them right away

---

## 🔍 Troubleshooting

**Q: Script doesn't run?**
- Make sure you're in the **Console** tab, not Elements or Network
- Refresh the Instagram page and try again

**Q: No JSON output?**
- Check that you're logged into Instagram
- Make sure JavaScript is enabled
- Try refreshing the page

**Q: Cookies missing?**
- Log out and log back in
- Clear browser cache
- Try a different browser

**Q: Where do I paste the JSON?**
- Create a new file: `account1.json`
- Paste the JSON into it
- Save in your project folder

---

## ✅ Verification

After merging, check `accounts.json`:

```bash
cat accounts.json | python3 -m json.tool
```

Should show 2 accounts with proper cookies!



