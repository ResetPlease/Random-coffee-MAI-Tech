from worker.app.Base import celery
from typing import Any


@celery.task
def send_simple_email(
                    smtp_server : str,
                    smtp_port : int,
                    receiver_email : str,
                    subject : str,
                    html_body_file : str,
                    login : str,
                    password : str,
                    html_boby_kwargs : dict[str, Any]
                ) -> None:
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from jinja2 import Template
    
    msg = MIMEMultipart()
    msg['From'] = login
    msg['To'] = receiver_email
    msg['Subject'] = subject
    
    body = Template(html_body_file)
    
    msg.attach(MIMEText(body.render(**html_boby_kwargs), 'html'))
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(login, password)

    server.sendmail(login, receiver_email, msg.as_string())
    server.quit()
    
    