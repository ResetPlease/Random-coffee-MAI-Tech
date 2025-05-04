from faststream import FastStream
from core.models.rabbitmq.email import SendSimpleMessageForm
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from core.dao.http import HTTPRequest, HTTPResponseType






class EmailSender:
    
    @staticmethod
    async def send_simple_email(form : SendSimpleMessageForm) -> None:
        
        msg = MIMEMultipart()
        msg['From'] = form.login
        msg['To'] = form.receiver_email
        msg['Subject'] = form.subject

        body : str = await HTTPRequest.get(
                                     server = form.request_page_server,
                                     port = form.request_page_port,
                                     endpoint = form.request_page_endpoint,
                                     query = form.request_page_query,
                                     headers = form.request_page_headers,
                                     response_method = HTTPResponseType.TEXT
                                 )

        msg.attach(MIMEText(body, 'html'))
        server = smtplib.SMTP(form.smtp_server, form.smtp_port)
        server.starttls()
        server.login(form.login, form.password)

        server.sendmail(form.login, form.receiver_email, msg.as_string())
        server.quit()