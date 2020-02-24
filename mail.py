import base64
import os
from sendgrid.helpers.mail import (
    Mail, Attachment, FileContent, FileName,
    FileType, Disposition, ContentId)
from sendgrid import SendGridAPIClient

EMAIL_API_KEY = "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"

def send_certificate_by_mail(name, to_email, file_path):
    message = Mail(
        from_email='rahul@widhya.org',
        to_emails=to_email,
        subject='Congratulations Are In Order From Widhya \u2764\uFE0F',
        html_content='<html><body><strong>and easy to do anywhere, even with Python</strong><br/><img src=\"' + file_path + '\"></body></html>')
    file_path = file_path
    filename = name.split(" ")[0] + "certificate.png"
    with open(file_path, 'rb') as f:
        data = f.read()
        f.close()
    encoded = base64.b64encode(data).decode()
    attachment = Attachment()
    attachment.file_content = FileContent(encoded)
    attachment.file_type = FileType('image/png')
    attachment.file_name = FileName(filename)
    attachment.disposition = Disposition('attachment')
    attachment.content_id = ContentId('cert')
    message.attachment = attachment
    sendgrid_client = SendGridAPIClient(EMAIL_API_KEY)
    response = sendgrid_client.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)


send_certificate_by_mail('Rahul','rahulkumaran313@gmail.com','modules/certificates/MOHAMMED REHAN HUSSAIN KHAN .png')
