console.log('Hello from content script!');

function fillFieldsFromResponse(fields) {
    fields.forEach(field => {
        let element = null;

        // Try to locate the element by ID
        if (field.id) {
            element = document.getElementById(field.id);
        }

        // If not found, locate by name
        if (!element && field.name) {
            element = document.getElementsByName(field.name)[0];
        }

        // If not found, locate by class (use the first match)
        if (!element && field.class) {
            const classSelector = field.class.map(cls => `.${cls}`).join('');
            element = document.querySelector(classSelector);
        }

        // If the element is found and is an input field, set its value
        if (element) {
            try {
                element.value = field.value || ''; // Set value or empty string
                element.dispatchEvent(new Event('input')); // Trigger input event if needed
                console.log(`Filled field: ${field.name || field.id}`);
            } catch (e) {
                console.error(`Error filling field: ${field.name || field.id}`, e);
            }
        } else {
            console.warn(`Field not found: ${field.name || field.id}`);
        }
    });
}


// Wait until the page is fully rendered
window.addEventListener('load', () => {
    console.log('Page fully loaded');

    // Handle messages from the background script or popup
    chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
        if (msg.action === "Ping") {
            alert("Pong");
        } else if (msg.action === 'collectFormData') {
            const htmlContent = document.body.innerHTML;
            sendResponse({
                htmlContent: htmlContent,
                url: window.location.href
            });
            return true;
        } else if (msg.action === 'fillForm') {
            const response = msg.data
            alert("Response arrived to content.js!");
            response.forEach(form => {
                if (form.fields && form.fields.length > 0) {
                    fillFieldsFromResponse(form.fields);
                }
            });
        }
    });
});
