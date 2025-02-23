# Batch Email Sender

## Description
This project automates the process of sending personalized emails in batches to a list of contacts stored in a CSV file. It customizes each email with the recipient's name and company, sends emails in batches of 50, and tracks progress using a batch number stored in a text file. The script ensures email delivery via a secure SMTP server and handles errors, making it suitable for automated email campaigns or outreach.

## Features
- **Personalized Emails:** Customizes the subject and body with the recipient's name and company.
- **Batch Processing:** Sends emails in batches of 50 to prevent overloading the email server.
- **Progress Tracking:** Keeps track of the last sent batch using a `batch_number.txt` file, ensuring emails can be resumed if interrupted.
- **SMTP Integration:** Sends emails securely through an SMTP server (Office 365 in this case).
- **Error Handling & Delays:** Automatically retries on failure and introduces a delay between emails to avoid being flagged as spam.

## Prerequisites
- Python
- `pandas` library
- An email accoung
- A CSV file containing contact details (`Email`, `Name`, `Company`)

## Installation
1. Clone this repository to your local machine.
2. Install the required Python libraries:
3. Prepare your `emails.csv` file
4. Modify the email credentials and the body:
```python
your_email = "your email"
your_password = "your password"

## run script
python send_emails.py
