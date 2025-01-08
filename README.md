# Auto Form Filler using AI - Chrome Extension

## Project Overview

The **Auto Form Filler Chrome Extension** is a tool designed to automate the process of filling dynamic or HTML forms on websites. The project leverages AI and communicates with an LLM (Large Language Model) to ensure accurate data population, even for unknown fields. While the Chrome extension interface is available, the actual form-filling functionality is currently managed by the Flask server, with future plans to integrate this feature into the Chrome extension. Contributions to this feature are highly welcomed!

## Features

- **Automatic Form Filling**: Automatically fills form fields using user-provided data.
- **Supports JSON Files**: Upload a `data.json` file containing personal information (e.g., CV details) to fill forms seamlessly.
- **Server-Driven Form Filling**: The Flask server handles form submission, ensuring secure and accurate processing.
- **LLM Integration**: Communicates with a Large Language Model to enhance the accuracy of information filled for unknown fields.
- **User-Friendly Interface**: Provides an intuitive interface for uploading and managing user data.
- **Future Enhancements**: Work is ongoing to integrate form-filling capabilities directly into the Chrome extension.

## Requirements

- A `data.json` file containing personal information (e.g., CV details) structured as key-value pairs for form fields.
- A valid Google Gemini API key (or equivalent).

## Installation

### Chrome Extension

1. **Clone the repository:**
   ```bash
   git clone https://github.com/an1604/AI-auto-form-filler.git
   ```
### Flask Backend Setup

1. **Clone the repository and navigate to the `api` directory:**

    ```bash
    git clone https://github.com/an1604/AI-auto-form-filler.git
   ```

2. **Set up a virtual environment (optional but recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Flask application locally:**

    ```bash
    python app.py
    ```
---

### Usage

1. **Upload User Data:**  
   Upload a `data.json` file containing all personal information (e.g., CV details) via the Chrome extension or directly to the server.

2. **Fill Forms:**  
   - The Flask server processes the data and automatically fills the forms.  
   - Navigate to the target website and use the Chrome extension (or server backend) to populate the form fields.

3. **Enhanced Accuracy:**  
   The server communicates with an LLM to improve accuracy, especially for unknown or ambiguous fields.

4. **Future Features:**  
   Integration of form-filling capabilities directly into the Chrome extension is in progress. Contributions to this feature are highly appreciated.

---

### Contributing

We welcome contributions to enhance this project, particularly the integration of form-filling functionality into the Chrome extension. If you're interested, feel free to submit a pull request or reach out to the repository owner.

