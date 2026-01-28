/**
 * Instagram Cookie Extractor Script
 * 
 * Instructions:
 * 1. Log into Instagram in your browser
 * 2. Open Developer Tools (F12)
 * 3. Go to Console tab
 * 4. Copy and paste this entire script
 * 5. Press Enter
 * 6. Copy the output JSON and use it in accounts.json
 */

(function() {
  // Get all cookies
  const cookies = document.cookie.split(';').reduce((acc, cookie) => {
    const [name, value] = cookie.trim().split('=');
    acc[name] = decodeURIComponent(value);
    return acc;
  }, {});
  
  // Extract required cookies
  const requiredCookies = {
    sessionid: cookies.sessionid || 'NOT_FOUND',
    csrftoken: cookies.csrftoken || 'NOT_FOUND',
    ds_user_id: cookies.ds_user_id || 'NOT_FOUND',
    rur: cookies.rur || 'NOT_FOUND'
  };
  
  // Get user agent
  const userAgent = navigator.userAgent;
  
  // Create accounts.json structure
  const accountsJson = {
    accounts: [
      {
        name: "account1",
        cookies: requiredCookies,
        session_id: requiredCookies.sessionid,
        user_agent: userAgent
      }
    ]
  };
  
  // Display results
  console.log('\n=== INSTAGRAM COOKIE EXTRACTION ===\n');
  console.log('Required Cookies Found:');
  console.log('  sessionid:', requiredCookies.sessionid ? '✓ Found' : '✗ NOT FOUND');
  console.log('  csrftoken:', requiredCookies.csrftoken ? '✓ Found' : '✗ NOT FOUND');
  console.log('  ds_user_id:', requiredCookies.ds_user_id ? '✓ Found' : '✗ NOT FOUND');
  console.log('  rur:', requiredCookies.rur ? '✓ Found' : '✗ NOT FOUND');
  
  console.log('\n=== COPY THIS JSON ===\n');
  console.log(JSON.stringify(accountsJson, null, 2));
  console.log('\n=== END ===\n');
  
  // Try to copy to clipboard
  if (navigator.clipboard) {
    navigator.clipboard.writeText(JSON.stringify(accountsJson, null, 2))
      .then(() => {
        console.log('✓ JSON copied to clipboard!');
        console.log('Paste it into accounts.json file\n');
      })
      .catch(() => {
        console.log('⚠ Could not copy to clipboard. Please copy manually from above.\n');
      });
  } else {
    console.log('⚠ Clipboard API not available. Please copy manually from above.\n');
  }
  
  // Return the JSON for easy access
  return accountsJson;
})();





