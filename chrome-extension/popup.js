// popup.js
document.addEventListener('DOMContentLoaded', function () {
    const uploadButton = document.getElementById('upload');
    const deleteButton = document.getElementById('deleteFile');
    const submitButton = document.getElementById('submitButton');
    const fileContentDiv = document.getElementById('fileContent');

    // Load previously uploaded file
    chrome.storage.local.get('userData', (result) => {
        if (result.userData) {
            fileContentDiv.textContent = result.userData;
        } else {
            fileContentDiv.textContent = 'No file uploaded yet.';
        }
    });

    // Handle file upload
    uploadButton.addEventListener('change', function (event) {
        const file = event.target.files[0];
        if (file && file.type === 'text/plain') {
            const reader = new FileReader();
            reader.onload = function (e) {
                const fileContent = e.target.result;
                chrome.storage.local.set({ userData: fileContent }, () => {
                    fileContentDiv.textContent = fileContent;
                });
            };
            reader.readAsText(file);
        } else {
            alert('Please upload a valid text file.');
        }
    });

    // Handle file deletion
    deleteButton.addEventListener('click', function () {
        chrome.storage.local.remove('userData', () => {
            fileContentDiv.textContent = 'No file uploaded yet.';
        });
    });

    // Handle form submission
    submitButton.addEventListener('click', function () {
        chrome.storage.local.get('userData', (result) => {
            const userData = result.userData || '';
            chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
                chrome.tabs.sendMessage(tabs[0].id, { action: 'collectFormData' }, (response) => {
                    fetch('https://affai-one.vercel.app/submit', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            htmlContent: response.htmlContent,
                            userData: userData,
                            url: response.url
                        })
                    })
                        .then(response => response.json())
                        .then(data => {
                            chrome.tabs.sendMessage(tabs[0].id, {
                                action: 'fillForm',
                                data: data
                            });
                        })
                        .catch(error => console.error('Error:', error));
                });
            });
        });
    });
});
