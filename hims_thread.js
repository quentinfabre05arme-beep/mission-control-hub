/**
 * HIMS Healthcare Thread
 * Paste this entire code into Chrome DevTools Console (F12)
 * After navigating to x.com/compose/tweet
 */

(async function() {
  const tweets = [
    "The GLP-1 revolution is here.\n\nBut the real play isn't the drugs - it's the infrastructure delivering them.\n\nHIMS is quietly building the rails for healthcare's biggest transformation.\n\n(Thread 🧵)",
    
    "Most people think HIMS is just a telehealth app.\n\nThey're wrong.\n\nHIMS is healthcare infrastructure - the picks and shovels of the GLP-1 gold rush.",
    
    "The numbers prove it:\n• $725M revenue in 2024\n• 2.5M+ subscribers\n• Partnership with Novo Nordisk\n• 87% gross margins\n\nThis isn't a startup. It's infrastructure at scale.",
    
    "While GLP-1 makers fight for market share,\nHIMS extracts value from ALL sides:\n• Patients get access\n• Doctors get patients\n• Pharmacies get volume\n• Insurers get efficiency\n\nPlatform economics at work.",
    
    "The market is waking up.\nHIMS is down from $25 to $12, creating an entry point for patient investors.\n\nBut this isn't about catching a falling knife.\nIt's about recognizing infrastructure before the market does.",
    
    "What makes HIMS different?\nThey own the relationship.\nNot the drug. Not the pharmacy.\nThe patient relationship.\n\nThat's the enduring value in healthcare delivery."
  ];
  
  console.log('📝 Preparing thread...');
  
  for (let i = 0; i < tweets.length; i++) {
    console.log(`📝 Writing tweet ${i + 1}/${tweets.length}...`);
    
    const textarea = document.querySelector(`[data-testid="tweetTextarea_${i}"]`);
    if (textarea) {
      textarea.focus();
      textarea.innerHTML = tweets[i];
      textarea.textContent = tweets[i];
      const event = new InputEvent('input', { bubbles: true });
      textarea.dispatchEvent(event);
      await new Promise(r => setTimeout(r, 500));
    }
    
    // Add next tweet button if needed
    if (i < tweets.length - 1) {
      const addBtn = document.querySelector('[data-testid="addButton"]');
      if (addBtn) {
        addBtn.click();
        await new Promise(r => setTimeout(r, 500));
      }
    }
  }
  
  await new Promise(r => setTimeout(r, 1000));
  
  // Click post button
  const postBtn = document.querySelector('[data-testid="tweetButton"]');
  if (postBtn && !postBtn.disabled) {
    postBtn.click();
    console.log('✅ Thread posted successfully!');
  } else {
    console.log('⚠️ Post button disabled - check character counts');
  }
})();
