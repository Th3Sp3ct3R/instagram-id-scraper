# How to Copy JSON Output - Visual Guide

## Step-by-Step: Where to Copy the JSON

### Step 1: Extract Cookies

1. **Log into Instagram** (Account 1)
2. **Press F12** to open Developer Tools
3. **Click the "Console" tab**
4. **Copy the entire contents** of `extract_single_account.js`
5. **Paste it into the console** and press **Enter**
6. **When prompted**, type `1` and press Enter

### Step 2: Find the JSON Output

After running the script, you'll see output in the console that looks like this:

```
=== INSTAGRAM ACCOUNT 1 ===

Cookies Found:
  sessionid: ✓
  csrftoken: ✓
  ds_user_id: ✓
  rur: ✓

=== COPY THIS JSON ===

{
  "name": "account1",
  "cookies": {
    "sessionid": "47119281269%3AN6F7fhYlim3f0J%3A25%3AAYg-K0Z0bXzz90Z5IOYIQAJwz5cSh_muYUItpEEjBjch",
    "csrftoken": "Te8ontIDTj1cNHyVTzZg1OoL3DNfZxby",
    "ds_user_id": "47119281269",
    "rur": "EAG\\05447119281269\\0541794676775:01fe0c8e46751826977baf5faf1671d7de0affeeee7e7c69ac38cf20022ca82ff5a1a6a3"
  },
  "session_id": "47119281269%3AN6F7fhYlim3f0J%3A25%3AAYg-K0Z0bXzz90Z5IOYIQAJwz5cSh_muYUItpEEjBjch",
  "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36..."
}

=== END ===

💾 Save this to: account1.json

✓ Copied to clipboard!
```

### Step 3: Copy the JSON

**Method A: From Console (Manual Copy)**
1. **Select the JSON text** (the part between `=== COPY THIS JSON ===` and `=== END ===`)
2. **Right-click → Copy** (or Ctrl+C / Cmd+C)
3. The JSON starts with `{` and ends with `}`

**Method B: Already Copied (Automatic)**
- If you see "✓ Copied to clipboard!", the JSON is already copied!
- Just paste it into a file

### Step 4: Save to File

**Option 1: Using VS Code / Text Editor**

1. **Open VS Code** (or any text editor)
2. **Create a new file**: `account1.json`
3. **Paste the JSON** (Ctrl+V / Cmd+V)
4. **Save the file** in your project folder:
   ```
   /Users/growthgod/Documents/Repos/Instagram ID Scraper _Suggestuser_scraper/account1.json
   ```

**Option 2: Using Terminal (Mac/Linux)**

```bash
# Navigate to project folder
cd "/Users/growthgod/Documents/Repos/Instagram ID Scraper _Suggestuser_scraper"

# Create file and paste (if copied to clipboard)
pbpaste > account1.json

# OR create file manually
nano account1.json
# Paste JSON, then: Ctrl+X, Y, Enter to save
```

**Option 3: Using Terminal (Windows)**

```bash
# Navigate to project folder
cd "C:\Users\...\Instagram ID Scraper _Suggestuser_scraper"

# Create file
notepad account1.json
# Paste JSON and save
```

### Step 5: Verify the File

Make sure `account1.json` contains valid JSON:

```json
{
  "name": "account1",
  "cookies": {
    "sessionid": "...",
    "csrftoken": "...",
    "ds_user_id": "...",
    "rur": "..."
  },
  "session_id": "...",
  "user_agent": "..."
}
```

### Step 6: Repeat for All Accounts

- Account 1 → `account1.json`
- Account 2 → `account2.json`
- Account 3 → `account3.json`
- ... (continue for all 10 accounts)

**Important**: When extracting Account 2, enter `2` when prompted, and save to `account2.json`. Repeat for all accounts.

### Step 7: Merge All Accounts

Once you have `account1.json` through `account10.json`:

```bash
cd "/Users/growthgod/Documents/Repos/Instagram ID Scraper _Suggestuser_scraper"
python merge_accounts.py
```

This will create `accounts.json` with all 10 accounts!

---

## Visual Example

```
Browser Console Output:
─────────────────────────────────────────────
=== COPY THIS JSON ===          ← START HERE

{                               ← COPY FROM HERE
  "name": "account1",
  "cookies": {
    "sessionid": "...",
    ...
  }
}                               ← TO HERE

=== END ===                     ← END HERE
─────────────────────────────────────────────
```

**Copy ONLY the JSON object** (the `{ ... }` part), not the `===` markers.

---

## Quick Checklist

- [ ] Logged into Instagram Account 1
- [ ] Opened F12 → Console tab
- [ ] Pasted `extract_single_account.js`
- [ ] Entered account number: 1
- [ ] Copied the JSON output
- [ ] Created `account1.json` file
- [ ] Pasted JSON into the file
- [ ] Saved the file in project folder
- [ ] Repeated for Accounts 2-10
- [ ] Ran `python merge_accounts.py`

---

## Troubleshooting

**Q: Where do I see the JSON output?**
A: In the browser console (F12 → Console tab), after running the script.

**Q: The JSON wasn't copied automatically**
A: Manually select the JSON text (between `{` and `}`) and copy it.

**Q: Where do I save the file?**
A: In the project folder: `/Users/growthgod/Documents/Repos/Instagram ID Scraper _Suggestuser_scraper/`

**Q: What should the file be named?**
A: `account1.json`, `account2.json`, etc. (one file per account)

**Q: How do I know if the JSON is valid?**
A: It should start with `{` and end with `}`, and have proper quotes and commas.



