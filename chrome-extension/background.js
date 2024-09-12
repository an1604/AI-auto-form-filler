// background.js
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'sendHtmlContent') {
        // Forward HTML content to popup for submission
        chrome.storage.local.set({ htmlContent: message.htmlContent, url: message.url }, () => {
            console.log('HTML content and URL stored.');
        });
    }
});
