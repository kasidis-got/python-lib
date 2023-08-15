import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def send_email_with_attachments(subject, body, to_email, file_paths, smtp_details):
    from_email = smtp_details['email']
    from_password = smtp_details['password']
    smtp_server = smtp_details['server']
    smtp_port = smtp_details['port']
    use_tls = smtp_details.get('use_tls', False)

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    for file_path in file_paths:
        with open(file_path, 'rb') as attachment_file:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment_file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename= {file_path.split('/')[-1]}")
            msg.attach(part)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        if use_tls:
            server.starttls()
        server.login(from_email, from_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# File paths of the CSVs
# file_paths = [
    "TLT_Policy_Compliance_Report_Windows_2019_Member_Server_Monthly_latest.csv",
    "TLT_Policy_Compliance_Report_Windows_2019_Domain_Server_Monthly_latest.csv",
    "TLT_Policy_Compliance_Report_Windows_2016_Member_Server_Monthly_latest.csv",
    "TLT_Policy_Compliance_Report_Windows_10_Monthly_latest.csv",
    "checkmarx_results.json"
]

file_paths = [
    "checkmarx_results.json"
]

smtp_details = {
    'email': 'gotnotify@got.co.th',
    'password': 'fnGh%LS*F9F9QH',
    'server': 'smtp.office365.com',
    'port': 587,   # Often 587 for TLS or 465 for SSL
    'use_tls': True  # Set this to False if you don't want to use starttls
}

# Example usage:
# send_email_with_attachments("CSV Files Attached", "Please find the attached CSV files.", "jitrada_b@tlt.co.th", file_paths, smtp_details)
send_email_with_attachments("CSV Files Attached", "Please find the attached CSV files.", "kasidis@got.co.th", file_paths, smtp_details)