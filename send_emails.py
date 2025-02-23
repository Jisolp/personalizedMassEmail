import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
import os
import time

# Load the CSV file with the contacts
try:
    contacts = pd.read_csv("emails.csv")
    print("CSV loaded successfully.")
    print(contacts.head()) 
except Exception as e:
    print(f"Error loading CSV: {e}")
    exit()

# Email credentials
your_email = "your email"
your_password = "your password"  # Use the password or app password if you have two-factor authentication enabled

smtp_server = "smtp.office365.com"
smtp_port = 587

# File to keep track of the last sent batch
batch_file = "batch_number.txt"

# Function to send an email
def send_email(to_email, name, company):
    # Customize the subject line
    subject = f"TEST EMAIL Hello {name} at {company}"
    
    # Customize the email body
    body = f"""
    Dear {name},

    I hope this email finds you well. I wanted to reach out regarding some exciting opportunities at {company}.
    
    Please feel free to get in touch if you'd like to learn more!

    Best,
    Jisol
    """
    
    # Set up the MIME
    message = MIMEMultipart()
    message["From"] = your_email
    message["To"] = to_email
    message["Subject"] = subject
    
    # Attach email body
    message.attach(MIMEText(body, "plain"))
    
    try:
        # Connect to the server with timeout to avoid freezing
        print(f"Connecting to SMTP server to send email to {to_email}...")
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=30)  # Increased timeout
        server.starttls()  # Upgrade to secure connection
        server.login(your_email, your_password)
        server.send_message(message)
        print(f"Email sent to {name} at {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")
    finally:
        server.quit()

# Function to get the current batch number
def get_current_batch_number():
    if os.path.exists(batch_file):
        try:
            with open(batch_file, 'r') as file:
                batch_number = file.read().strip()
                print(f"Batch number read: {batch_number}")  # Debugging line
                if batch_number == '': 
                    return 1
                return int(batch_number)
        except ValueError:
            print("Invalid batch number in file. Resetting to 1.")
            return 1
    else:
        return 1  # If the file doesn't exist, start from batch 1

# Function to update the batch number after sending emails
def update_batch_number(batch_number):
    with open(batch_file, 'w') as file:
        file.write(str(batch_number))

# Function to send emails in batches (automatically increments the batch number)
def send_emails():
    batch_number = get_current_batch_number()  # Get the current batch number
    total_emails = len(contacts)
    start_index = (batch_number - 1) * 50  # Calculate the start index for the batch
    end_index = start_index + 50  # Calculate the end index for the batch
    
    # Get the batch of contacts
    batch = contacts.iloc[start_index:end_index]
    
    print(f"Batch {batch_number}: Sending emails...")
    # Send emails to the batch
    for index, row in batch.iterrows():
        send_email(row["Email"], row["Name"], row["Company"])
        time.sleep(1)  # Add a 1-second delay between emails to avoid overloading the server
    
    print(f"Sent {len(batch)} emails from batch {batch_number}.")
    
    # Check if there are more emails to send
    if end_index < total_emails:
        print(f"Ready to send batch {batch_number + 1} next. Script will automatically pick up the next batch next time.")
        update_batch_number(batch_number + 1) 
    else:
        print("All emails have been sent.")

send_emails()
