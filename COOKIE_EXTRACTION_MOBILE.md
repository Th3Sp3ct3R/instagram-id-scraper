# Extracting Instagram Cookies from Mobile Devices

This guide shows you how to extract Instagram cookies from your phone/tablet and use them in the scraper.

## Method 1: Using Mobile Browser Developer Tools (Recommended)

### For iPhone/iPad (Safari)

#### Step 1: Enable Developer Tools on Your Mac

1. **On your iPhone/iPad:**
   - Go to **Settings** → **Safari** → **Advanced**
   - Turn on **Web Inspector**

2. **On your Mac:**
   - Open **Safari**
   - Go to **Safari** → **Preferences** → **Advanced**
   - Check **"Show Develop menu in menu bar"**

#### Step 2: Connect and Extract

1. **Connect your iPhone/iPad to your Mac** via USB
2. **On your iPhone/iPad:**
   - Open Safari
   - Log into Instagram (instagram.com)
   - Make sure you're logged in and on the main feed

3. **On your Mac:**
   - Open Safari
   - Go to **Develop** menu → Select your iPhone/iPad name
   - Click on **instagram.com** (it will open Web Inspector)
   - In the Web Inspector, go to **Storage** tab → **Cookies** → **https://www.instagram.com**
   - Find and copy:
     - `sessionid`
     - `csrftoken`
     - `ds_user_id`
     - `rur`

4. **Use the extraction script:**
   - In Web Inspector, go to **Console** tab
   - Paste `extract_single_account.js`
   - Copy the JSON output

### For Android (Chrome)

#### Step 1: Enable USB Debugging

1. **On your Android device:**
   - Go to **Settings** → **About Phone**
   - Tap **Build Number** 7 times (enables Developer Options)
   - Go back → **Developer Options**
   - Enable **USB Debugging**

#### Step 2: Connect and Extract

1. **Connect Android to computer** via USB
2. **On your Android:**
   - Open Chrome
   - Log into Instagram (instagram.com)

3. **On your computer:**
   - Open Chrome
   - Go to `chrome://inspect`
   - Find your device → Click **inspect**
   - In DevTools, go to **Application** tab → **Cookies** → `https://www.instagram.com`
   - Copy the cookie values

---

## Method 2: Using Desktop Browser (Easiest)

### Step 1: Log into Instagram on Desktop

1. **Open your browser** (Chrome, Firefox, Safari, Edge)
2. **Go to** [instagram.com](https://www.instagram.com)
3. **Log in** with your credentials:
   - Username: `ffddnn87`
   - Password: `Aged#123`
   - (or use email: `ffddnn87@gmail.com` with password: `Aged#8181`)

### Step 2: Extract Cookies

#### Option A: Using Console Script (Fastest)

1. **While logged into Instagram**, press **F12** (or right-click → Inspect)
2. **Click the "Console" tab**
3. **Copy the entire contents** of `extract_single_account.js`
4. **Paste into the console** and press **Enter**
5. **When prompted**, enter account number (e.g., `1`)
6. **Copy the JSON output** that appears
7. **Save to file**: `account1.json`

#### Option B: Manual Extraction

1. **Press F12** → **Application** tab (Chrome) or **Storage** tab (Firefox)
2. **Expand "Cookies"** → Click **`https://www.instagram.com`**
3. **Find these cookies** and copy their **Value**:
   - `sessionid` ← **Most important!**
   - `csrftoken`
   - `ds_user_id`
   - `rur` (optional)

4. **Get User-Agent:**
   - Go to **Console** tab
   - Type: `navigator.userAgent`
   - Press Enter
   - Copy the result

5. **Create JSON file:**
   ```json
   {
     "name": "account1",
     "cookies": {
       "sessionid": "PASTE_SESSIONID_HERE",
       "csrftoken": "PASTE_CSRFTOKEN_HERE",
       "ds_user_id": "PASTE_DS_USER_ID_HERE",
       "rur": "PASTE_RUR_HERE"
     },
     "session_id": "PASTE_SESSIONID_HERE_AGAIN",
     "user_agent": "PASTE_USER_AGENT_HERE"
   }
   ```

---

## Method 3: Using Instagram Mobile App (Advanced)

### Extracting from Instagram App

**Note:** This is more complex and requires root/jailbreak or special tools.

#### For Android (Root Required)

1. **Install a root file browser** (like Root Explorer)
2. **Navigate to:** `/data/data/com.instagram.android/shared_prefs/`
3. **Find:** `com.instagram.android_preferences.xml`
4. **Look for:** Session cookies stored in preferences
5. **Extract:** Use a tool like `adb` to pull the file

#### For iPhone (Jailbreak Required)

1. **Install Filza** (file manager)
2. **Navigate to:** `/var/mobile/Containers/Data/Application/[Instagram]/Library/Preferences/`
3. **Find:** Instagram preference files
4. **Extract:** Session data

**⚠️ Warning:** Rooting/jailbreaking voids warranties and has security risks. Not recommended unless you're experienced.

---

## Step-by-Step: Complete Cookie Extraction

### For Account 1 (ffddnn87)

1. **Open browser** → Go to instagram.com
2. **Log in** with:
   - Username: `ffddnn87`
   - Password: `Aged#123`
3. **Press F12** → **Console** tab
4. **Paste** `extract_single_account.js` → Press Enter
5. **Enter:** `1` when prompted
6. **Copy JSON** output
7. **Save to:** `account1.json`

### For Account 2 (Email account)

1. **Open browser** (or new incognito window)
2. **Go to** instagram.com
3. **Log in** with:
   - Email: `ffddnn87@gmail.com`
   - Password: `Aged#8181`
4. **Press F12** → **Console** tab
5. **Paste** `extract_single_account.js` → Press Enter
6. **Enter:** `2` when prompted
7. **Copy JSON** output
8. **Save to:** `account2.json`

### Merge Both Accounts

```bash
python merge_accounts.py
```

This creates `accounts.json` with both accounts!

---

## Visual Guide: Where to Find Cookies

### Chrome/Edge/Brave

```
F12 → Application Tab
  └── Cookies (left sidebar)
      └── https://www.instagram.com
          ├── sessionid      ← Copy this Value
          ├── csrftoken      ← Copy this Value
          ├── ds_user_id     ← Copy this Value
          └── rur            ← Copy this Value (optional)
```

### Firefox

```
F12 → Storage Tab
  └── Cookies (left sidebar)
      └── https://www.instagram.com
          ├── sessionid      ← Copy this Value
          ├── csrftoken      ← Copy this Value
          ├── ds_user_id     ← Copy this Value
          └── rur            ← Copy this Value (optional)
```

### Safari

```
Cmd+Option+I → Storage Tab
  └── Cookies
      └── instagram.com
          ├── sessionid      ← Copy this Value
          ├── csrftoken      ← Copy this Value
          ├── ds_user_id     ← Copy this Value
          └── rur            ← Copy this Value (optional)
```

---

## What Each Cookie Does

| Cookie | Purpose | Required? |
|--------|---------|-----------|
| **sessionid** | Your authentication token - proves you're logged in | ✅ **YES** - Most important! |
| **csrftoken** | CSRF protection token | ✅ **YES** |
| **ds_user_id** | Your Instagram user ID | ✅ **YES** |
| **rur** | Region/user routing info | ⚠️ Optional but recommended |

---

## Troubleshooting

### "Cookies not showing up"
- **Solution:** Make sure you're **logged into Instagram** first
- Refresh the page after logging in
- Check you're looking at cookies for `https://www.instagram.com` (not `instagram.com`)

### "sessionid is missing"
- **Solution:** You might not be fully logged in
- Try logging out and logging back in
- Clear browser cache and try again

### "Cookies expired quickly"
- **Solution:** This is normal - Instagram sessions expire
- Extract fresh cookies when they expire
- Cookies typically last days/weeks, but can expire sooner

### "Can't extract from mobile"
- **Solution:** Use desktop browser method instead (easier)
- Or use remote debugging (Chrome DevTools on Android)

### "Script doesn't work"
- **Solution:** Make sure you're in the **Console** tab, not Network or Elements
- Check that JavaScript is enabled
- Try refreshing the Instagram page and running script again

---

## Security Best Practices

1. **Never share your cookies** - They give full account access
2. **Don't commit cookies to Git** - Already in `.gitignore`
3. **Extract cookies fresh** - Don't use old/expired ones
4. **Use different browsers** - For multiple accounts, use incognito windows
5. **Keep accounts.json secure** - Store it safely on your computer

---

## Quick Checklist

- [ ] Logged into Instagram in browser
- [ ] Opened Developer Tools (F12)
- [ ] Found Console tab
- [ ] Pasted `extract_single_account.js`
- [ ] Entered account number
- [ ] Copied JSON output
- [ ] Saved to `account1.json` (or `account2.json`)
- [ ] Repeated for second account
- [ ] Ran `python merge_accounts.py`
- [ ] Verified `accounts.json` has both accounts

---

## Next Steps

After extracting cookies:

1. **Test the scraper:**
   ```bash
   python scraper_cli.py instagram --stats
   ```

2. **Verify accounts are active:**
   - Check stats show 2 accounts
   - Make sure both are active

3. **Start scraping:**
   ```bash
   python scraper_cli.py username1 username2 --output results.json
   ```

---

## Need Help?

If you're stuck:
1. Check `HOW_TO_COPY_JSON.md` for detailed copy instructions
2. Review `COOKIE_EXTRACTION_GUIDE.md` for more methods
3. Make sure you're logged into Instagram before extracting



