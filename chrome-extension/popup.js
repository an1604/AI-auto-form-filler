function sendRequest(request_type, routeName, response = null, userData = null) {
    alert(`request_type: ${request_type}, routeName: ${routeName}`)
    if (request_type === 'POST') {
        alert("In 'POST' request...")
        return fetch(`http://localhost:5000/${routeName}`, {
            method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({
                htmlContent: response.htmlContent, userData: userData, url: response.url
            })
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Server error: ${response.status}`);
                }
                return response.json();
            })
            .catch(error => {
                console.error('Error during fetch or form fill:', error);
                throw error; // Re-throw the error so it can be handled by the caller
            });
    } else {
        return fetch(`http://localhost:5000/${routeName}`, {
            method: 'GET', headers: {'Content-Type': 'application/json'}
        })
            .then(response => {
                if (!response.ok) {
                    alert(`Server error: ${response.status}`)
                    throw new Error(`Server error: ${response.status}`);
                }
                const res = response.json();
                alert(`Success\n\n ${res}`)
                return res; // Parse the JSON response
            })
    }
}


// popup.js
document.addEventListener('DOMContentLoaded', function (message) {
    const uploadButton = document.getElementById('upload');
    const deleteButton = document.getElementById('deleteFile');
    const submitButton = document.getElementById('submitButton');
    const fileContentDiv = document.getElementById('fileContent');
    const PingButton = document.getElementById('sendPing');

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
                chrome.storage.local.set({userData: fileContent}, () => {
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

    PingButton.addEventListener('click', function () {
        console.log("Pinging server...");

        // Perform the GET request to the server

        sendRequest("GET", "ping").then(serverData => {
            console.log("Ping Response:", serverData);

            // After successful fetch, send the server response to the content script
            chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
                if (!tabs.length || !tabs[0]?.id) {
                    console.error("No active tab found.");
                    return;
                }

                chrome.tabs.sendMessage(tabs[0].id, {
                    action: "Ping", text: "Ping from popup with server data", data: serverData
                });
            });
        }).catch(error => {
            console.error("Error during ping:", error);
            alert("Ping failed:\n" + error.message);
        });
    });

    // Handle form submission
    submitButton.addEventListener('click', function (message) {
        chrome.storage.local.get('userData', (result) => {
            const userData = result.userData || '';

            chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
                if (!tabs || tabs.length === 0) {
                    console.error('No active tab found.');
                    return;
                }
                // Send message to collect form data
                chrome.tabs.sendMessage(tabs[0].id, {action: 'collectFormData'}, (response) => {
                    console.log(`response: ${response}`)
                    if (!response || !response.htmlContent || !response.url) {
                        console.error('Invalid response received:', response);
                        return;
                    }
                    // Sending the request to the server
                    console.log("Calling sendRequest...")
                    sendRequest("POST", "submit", response, userData)
                        .then(data => {
                            console.log(`Server Response: ${data}`);
                            return data;
                        })
                        .then(data => {
                            console.log(`line 128 ${data}`)
                            if (data.status && data.status === "Job applied from manually server!") {
                                alert("Job applied from manually server!")
                            } else {
                                alert(`The received data: ${response}`)
                                chrome.tabs.sendMessage(tabs[0].id, {
                                    action: 'fillForm', data: data
                                });
                            }
                        })
                        .catch(error => {
                            console.error("Error during sendHTML:", error);
                            alert("Failed to submit form data.");
                        });
                });
            });
        });
    });
});
