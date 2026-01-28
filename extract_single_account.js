/**
 * Single Account Cookie Extractor
 * 
 * Use this for extracting ONE account at a time
 * 
 * Instructions:
 * 1. Log into ONE Instagram account in your browser
 * 2. Open Developer Tools (F12) → Console tab
 * 3. Copy and paste this entire script
 * 4. When prompted, enter the account number (1, 2, 3, etc.)
 * 5. Copy the JSON output
 * 6. Save it to account1.json, account2.json, etc.
 * 7. Repeat for all 10 accounts
 */

(function() {
  // Get all cookies
  const cookies = document.cookie.split(';').reduce((acc, cookie) => {
    const [name, value] = cookie.trim().split('=');
    acc[name] = decodeURIComponent(value);
    return acc;
  }, {});
  
  // Prompt for account number
  const accountNum = prompt('Enter account number (1-10):', '1') || '1';
  
  // Extract required cookies
  const accountData = {
    name: `account${accountNum}`,
    cookies: {
      sessionid: cookies.sessionid || '',
      csrftoken: cookies.csrftoken || '',
      ds_user_id: cookies.ds_user_id || '',
      rur: cookies.rur || ''
    },
    session_id: cookies.sessionid || '',
    user_agent: navigator.userAgent
  };
  
  // Display results
  console.log('\n=== INSTAGRAM ACCOUNT ' + accountNum + ' ===\n');
  console.log('Cookies Found:');
  console.log('  sessionid:', accountData.cookies.sessionid ? '✓' : '✗ MISSING');
  console.log('  csrftoken:', accountData.cookies.csrftoken ? '✓' : '✗ MISSING');
  console.log('  ds_user_id:', accountData.cookies.ds_user_id ? '✓' : '✗ MISSING');
  console.log('  rur:', accountData.cookies.rur ? '✓' : '✗ MISSING');
  
  console.log('\n=== COPY THIS JSON ===\n');
  const jsonOutput = JSON.stringify(accountData, null, 2);
  console.log(jsonOutput);
  console.log('\n=== END ===\n');
  console.log('💾 Save this to: account' + accountNum + '.json\n');
  
  // Try to copy to clipboard
  if (navigator.clipboard) {
    navigator.clipboard.writeText(jsonOutput)
      .then(() => {
        console.log('✓ Copied to clipboard!');
        console.log('📝 Paste into account' + accountNum + '.json file\n');
      })
      .catch(() => {
        console.log('⚠ Please copy manually from above\n');
      });
  } else {
    console.log('⚠ Please copy manually from above\n');
  }
  
  // Return the account data
  return accountData;
})();



