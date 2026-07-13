(function() {
    const editor = document.querySelector('[data-testid="tweetTextarea_0"]') || 
                   document.querySelector('[contenteditable="true"]') ||
                   document.querySelector('div[role="textbox"]');
    if (editor) {
        editor.focus();
        editor.innerHTML = '';
        const textNode = document.createTextNode('Testing automation with file-based JS');
        editor.appendChild(textNode);
        editor.dispatchEvent(new Event('input', { bubbles: true }));
        return 'typed';
    }
    return 'not_found';
})()
