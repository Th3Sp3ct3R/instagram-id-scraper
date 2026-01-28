# How to Extract Instagram Cookies for accounts.json

This guide will walk you through extracting the required cookies from Instagram to use with the scraper.

## Required Cookies

You need to extract these cookies from Instagram:
- **sessionid** (most important - this is your authentication token)
- **csrftoken** (CSRF protection token)
- **ds_user_id** (your Instagram user ID)
- **rur** (optional but recommended)

## Method 1: Using Chrome/Edge/Brave (Recommended)

### Step 1: Log into Instagram
1. Open Chrome (or Edge/Brave)
2. Go to [https://www.instagram.com](https://www.instagram.com)
3. **Log in** to your Instagram account

### Step 2: Open Developer Tools
1. Press **F12** (or **Cmd+Option+I** on Mac, **Ctrl+Shift+I** on Windows/Linux)
2. Or right-click anywhere on the page → Select **"Inspect"**

### Step 3: Navigate to Cookies
1. Click on the **"Application"** tab (at the top of Developer Tools)
2. In the left sidebar, expand **"Cookies"**
3. Click on **"https://www.instagram.com"**

### Step 4: Find and Copy Cookies
You'll see a table with all cookies. Find and copy these values:

| Cookie Name | What to Look For | Example |
|------------|------------------|---------|
| **sessionid** | A long string starting with something like `"xxxxx%3Axxxxx%3Axxxxx"` | This is your main session token |
| **csrftoken** | A shorter alphanumeric string | Usually 32 characters |
| **ds_user_id** | A numeric string (your Instagram user ID) | e.g., `"1234567890"` |
| **rur** | A string like `"ATN"` or similar | Optional but helpful |

### Step 5: Copy the Values
- Click on each cookie name to see its **Value**
- Copy the entire value (double-click to select, then Ctrl+C / Cmd+C)

## Method 2: Using Firefox

### Step 1: Log into Instagram
1. Open Firefox
2. Go to [https://www.instagram.com](https://www.instagram.com)
3. **Log in** to your Instagram account

### Step 2: Open Developer Tools
1. Press **F12** (or **Cmd+Option+I** on Mac, **Ctrl+Shift+I** on Windows/Linux)
2. Or right-click → **"Inspect Element"**

### Step 3: Navigate to Storage
1. Click on the **"Storage"** tab
2. Expand **"Cookies"** in the left sidebar
3. Click on **"https://www.instagram.com"**

### Step 4: Find and Copy Cookies
Same as Chrome - find the cookie values in the table and copy them.

## Method 3: Using Browser Extension (Easiest)

### Option A: Cookie-Editor Extension
1. Install **Cookie-Editor** extension:
   - Chrome: [Cookie-Editor](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm)
   - Firefox: [Cookie-Editor](https://addons.mozilla.org/en-US/firefox/addon/cookie-editor/)

2. Log into Instagram
3. Click the Cookie-Editor icon in your browser toolbar
4. Find `instagram.com` in the list
5. Click **"Export"** → Select **"JSON"**
6. Copy the values you need from the exported JSON

### Option B: EditThisCookie Extension
1. Install **EditThisCookie**:
   - Chrome: [EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg)

2. Log into Instagram
3. Click the EditThisCookie icon
4. Find and copy the cookie values

## Method 4: Using Browser Console (Quick Copy)

1. Log into Instagram
2. Open Developer Tools (F12)
3. Go to **"Console"** tab
4. Paste this code and press Enter:

```javascript
// Copy all Instagram cookies to clipboard
const cookies = document.cookie.split(';').reduce((acc, cookie) => {
  const [name, value] = cookie.trim().split('=');
  acc[name] = value;
  return acc;
}, {});

// Display important cookies
console.log('sessionid:', cookies.sessionid);
console.log('csrftoken:', cookies.csrftoken);
console.log('ds_user_id:', cookies.ds_user_id);
console.log('rur:', cookies.rur);

// Copy to clipboard (Chrome/Edge)
navigator.clipboard.writeText(JSON.stringify({
  sessionid: cookies.sessionid,
  csrftoken: cookies.csrftoken,
  ds_user_id: cookies.ds_user_id,
  rur: cookies.rur
}, null, 2)).then(() => {
  console.log('Cookies copied to clipboard!');
});
```

5. Check the console output or your clipboard for the cookie values

## Filling Out accounts.json

Once you have the cookie values, create `accounts.json`:

```json
{
  "accounts": [
    {
      "name": "account1",
      "cookies": {
        "sessionid": "PASTE_YOUR_SESSIONID_HERE",
        "csrftoken": "PASTE_YOUR_CSRFTOKEN_HERE",
        "ds_user_id": "PASTE_YOUR_DS_USER_ID_HERE",
        "rur": "PASTE_YOUR_RUR_HERE"
      },
      "session_id": "PASTE_YOUR_SESSIONID_HERE_AGAIN",
      "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
  ]
}
```

**Important Notes:**
- The `session_id` field should be the same value as `sessionid` in cookies
- Keep the quotes around the values
- Don't include any extra spaces
- You can add multiple accounts by adding more objects to the `accounts` array

## Getting Your User Agent

To get your browser's user agent:
1. Open Developer Tools (F12)
2. Go to **Console** tab
3. Type: `navigator.userAgent` and press Enter
4. Copy the result and paste it in the `user_agent` field

## Troubleshooting

### Cookies Not Showing Up?
- Make sure you're **logged in** to Instagram
- Refresh the page after logging in
- Check that you're looking at cookies for `https://www.instagram.com` (not `instagram.com`)

### Session Expired?
- Instagram sessions expire after some time (usually days/weeks)
- If you get authentication errors, extract fresh cookies
- Consider extracting cookies from multiple accounts for better rotation

### Can't Find sessionid?
- Make sure you're logged in
- Try clearing cookies and logging in again
- The sessionid cookie should be present when you're authenticated

## Security Warning

⚠️ **Keep your cookies secure!**
- Never share your `sessionid` - it gives full access to your account
- Don't commit `accounts.json` to public repositories
- Consider using environment variables in production
- Rotate cookies periodically

## Quick Test

After creating `accounts.json`, test it:

```bash
python scraper_cli.py instagram --stats
```

If it works, you'll see the user ID for @instagram. If you get authentication errors, your cookies may have expired - extract fresh ones!





