// content.js
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'collectFormData') {
        // Get the HTML content of the body
        const htmlContent = document.body.innerHTML;

        // Send the HTML content to the background script
        chrome.runtime.sendMessage({
            action: 'sendHtmlContent',
            htmlContent: htmlContent,
            url: window.location.href
        });
    }
});
