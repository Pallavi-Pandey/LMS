from smptlib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(email, subject):
    msg = MIMEMultipart()
    msg['From'] = 'pallavipandey181@gmail.com'
    msg['To'] = email
    msg['Subject'] = subject
    message = 'Your daily reminder'
    msg.attach(MIMEText(message))
    client = SMTP('smtp.gmail.com', 587)    
    