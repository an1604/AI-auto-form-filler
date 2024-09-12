# Form Filler Chrome Extension

## Project Overview

The **Form Filler Chrome Extension** is designed to automate the process of filling dynamic or HTML forms on websites. Using the Google Gemini API, the extension utilizes user data from text or JSON files to accurately populate form fields, saving time and reducing manual input.

## Features

- **Automatic Form Filling**: Automatically fills form fields using user data.
- **Supports JSON and Text Files**: Upload user data in either JSON or text file format.
- **Integration with Google Gemini API**: Uses advanced AI to match user data with form fields.
- **Track Filled Forms**: Keeps track of websites where forms have been filled.
- **User-Friendly Interface**: Easy-to-use Chrome extension interface.

## Installation

### Chrome Extension

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sajidkassari/Auto-Form-Filler-ai.git

2. **Go to chrome://extensions/ in Chrome.**
3. **Enable Developer mode.**
4. **Click Load unpacked and select the directory containing the extension files.**

## Flask Backend
1. **Clone the repository and navigate to the api directory.**
2. **Set up a virtual environment (optional but recommended)**
      ```bash
      python -m venv venv
      source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
3. **Install dependencies:**
      ```bash
      pip install -r requirements.txt
4. **Set up environment variables in a .env file:**
      ```bash
      GEMINI_API_KEY=your_google_gemini_api_key
5. **Run the Flask application locally:**
      ```bash
      python app.py

## Usage
1. Upload User Data:
   Use the popup interface of the Chrome extension to upload user data in JSON or text file format.
2. Fill Forms:
   Navigate to a website with a form and click the extension icon to automatically fill the form fields with the uploaded data.
3. View Last Uploaded File:
   The extension displays the last uploaded file with options to open or delete it.
