from email.mime.application import MIMEApplication
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib

from flask import make_response, render_template
from weasyprint import HTML

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
SENDER_EMAIL = 'pallavipandey181@gmail.com'
SENDER_PASSWORD = os.getenv('APP_PASSWORD')

def create_pdf(data, filename):
    rendered_html = render_template('newpdf.html',data=data)
    print("indide create pdf",data)

    # Convert rendered HTML to PDF using WeasyPrint
    pdf_content = HTML(string=rendered_html).write_pdf()
    # to save the pdf
    with open(data['email']+'.pdf', 'wb') as f:
        f.write(pdf_content)


    # Create response
    response = make_response(pdf_content)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename={filename}.pdf'

    return response



def send_email_attachment(To, subject, message, data):
    msg = MIMEMultipart()
    sender = SENDER_EMAIL
    msg['From'] = sender
    msg['To'] = To
    msg['Subject'] = subject
    file_name = To + '.pdf'
    create_pdf(data, file_name)
    msg.attach(MIMEText(message))
    filename = file_name
    path = os.path.join(os.getcwd(), filename)
    with open(path, 'rb') as f:
        attachment = MIMEApplication(f.read(), _subtype='pdf')
        attachment.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(attachment)
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = SENDER_EMAIL
    smtp_password = SENDER_PASSWORD

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender, To, msg.as_string())


def send_email_without_attachment(To, subject, message):
    msg = MIMEMultipart()
    sender = SENDER_EMAIL
    msg['From'] = sender
    msg['To'] = To
    msg['Subject'] = subject
    msg.attach(MIMEText(message))
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = SENDER_EMAIL
    smtp_password = SENDER_PASSWORD

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender, To, msg.as_string())
