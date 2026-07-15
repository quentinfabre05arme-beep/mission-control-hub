// x_post_console.js - Post to X via Browser Console (No dependencies)
// Paste this into Chrome DevTools console on x.com

(function() {
    const TWEET_TEXT = `%TWEET_TEXT%`;
    
    async function postTweet(text) {
        console.log('🚀 Starting X post automation...');
        
        // Find the compose button
        const composeBtn = document.querySelector('[data-testid="SideNav_NewTweet_Button"]') || 
                          document.querySelector('a[href="/compose/tweet"]') ||
                          document.querySelector('[aria-label*="Compose"]');
        
        if (!composeBtn) {
            console.error('❌ Compose button not found');
            return false;
        }
        
        console.log('📝 Clicking compose button...');
        composeBtn.click();
        
        // Wait for modal to open
        await new Promise(r => setTimeout(r, 1500));
        
        // Find text input
        const textInput = document.querySelector('[data-testid="tweetTextarea_0"]') ||
                         document.querySelector('div[role="textbox"][contenteditable="true"]');
        
        if (!textInput) {
            console.error('❌ Text input not found');
            return false;
        }
        
        console.log('⌨️ Typing tweet...');
        textInput.focus();
        textInput.innerHTML = text;
        textInput.dispatchEvent(new InputEvent('input', { bubbles: true }));
        
        await new Promise(r => setTimeout(r, 1000));
        
        // Find post button
        const postBtn = document.querySelector('[data-testid="tweetButton"]') ||
                       document.querySelector('[data-testid="tweetButtonInline"]') ||
                       document.querySelector('button[type="submit"]');
        
        if (!postBtn || postBtn.disabled) {
            console.error('❌ Post button not found or disabled');
            return false;
        }
        
        console.log('📤 Clicking post button...');
        postBtn.click();
        
        await new Promise(r => setTimeout(r, 3000));
        
        console.log('✅ Tweet posted successfully!');
        return true;
    }
    
    // Run
    postTweet(TWEET_TEXT).then(success => {
        if (success) {
            console.log('🎉 Success! Check your timeline.');
        } else {
            console.error('❌ Failed to post tweet');
        }
    });
})();
