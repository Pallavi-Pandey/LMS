import datetime
from celery import shared_task
import flask_excel as excel

from .mail_service import send_email_attachment, send_email_without_attachment
from .models import BookRequest, User, Role,db
from jinja2 import Template
from celery import shared_task

@shared_task(ignore_result=False)
def create_resource_csv():
    import time
    # time.sleep(20)
    all_users = User.query.all()
    print(all_users)
    

    csv_output = excel.make_response_from_query_sets(
        all_users, ['email', 'get_user_role','books_requested'], 'csv')
    
    filename = "test.csv"

    with open(filename, 'wb') as f:
        f.write(csv_output.data)

    return filename


@shared_task(ignore_result=True)
def daily_reminder(to, subject):
    users = User.query.filter(User.roles.any(Role.name == 'admin')).all()
    data={}
    data["email"]=to
    data["name"]="Gokulakrishnan"
    data["start_date"]="2024-02-06"
    data["end_date"]="2024-05-06"
    for user in users:
            send_email_attachment(to, subject,'Please find attached PDF', data) 
    return "OK"



@shared_task(ignore_result=True)
def another_task():
    # Task logic here
    print("This task runs every 10 seconds")
    return "OK"


@shared_task(ignore_result=True)
def revoke_access():
    requests=BookRequest.query.filter_by(status='approved').all()
    for book_request in requests:
        if datetime.datetime.now() - book_request.requested_date > datetime.timedelta(days=7):
            book_request.status = 'revoked'
    db.session.commit()
    return "OK"



@shared_task(ignore_result=True)
def send_remainder():
    # daily remainder
    users = User.query.filter(User.roles.any(Role.name == 'stud')).all()
    for user in users:
        # check if user logged in today
        if user.last_login_at.date() != datetime.datetime.now().date():
            send_email_without_attachment(user.email, 'Reminder','Remainder to visit Pallavi LMS')
    return "OK"

@shared_task(ignore_result=True)
def monthly_report():
    users = User.query.all()
    for user in users:
        data={"user_name": user.name, "email": user.email, "data":user.monthly_report}
        send_email_attachment(user.email, 'Monthly Report','Please find attached PDF', data)
                
    