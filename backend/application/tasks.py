from celery import shared_task
import flask_excel as excel
from .mail_service import send_email_attachment
from .models import User, Role
from jinja2 import Template
from celery import shared_task

@shared_task(ignore_result=False)
def create_resource_csv():
    import time
    # time.sleep(20)
    all_users = User.query.all()
    print(all_users)
    

    csv_output = excel.make_response_from_query_sets(
        all_users, ['email', 'get_user_role'], 'csv')
    
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
