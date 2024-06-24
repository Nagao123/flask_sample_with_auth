from flask import current_app
from email.mime.text import MIMEText
from email.utils import formataddr
from smtplib import SMTP, SMTP_SSL
import ssl

class SendEmail:

    def __init__(self):

        self.server = current_app.config['MAIL_SERVER']
        self.port = current_app.config['MAIL_PORT']
        self.sender = current_app.config['MAIL_SENDER']
        self.username = current_app.config['MAIL_USERNAME']
        self.password = current_app.config['MAIL_PASSWORD']
        self.tls = current_app.config['MAIL_USE_TLS']
        self.ssl = current_app.config['MAIL_USE_SSL']
        self.auth = current_app.config['MAIL_AUTH']
        self.bcc = current_app.config['MAIL_BCC']
     
    def send_email(self, email_data):

        try:
            smtp_server = self.conn_email_server()
            email_body = self.create_email(email_data)
            smtp_server.send_message(email_body)
            self.quit_email_server(smtp_server)
        except:
            print('Failed to send email. ({})'.format(email_body['To']))
            return False
    
    def conn_email_server(self):

        smtp_server = self.server
        smtp_port = self.port

        if int(smtp_port) == 465:
            context = ssl.create_default_context()
            conn_smtp = SMTP_SSL(smtp_server, smtp_port, context)
        else:
            conn_smtp = SMTP(smtp_server, smtp_port)

        if self.auth == True:
            smtp_user = self.username
            smtp_pwd = self.password
            conn_smtp.login(smtp_user, smtp_pwd)

        return conn_smtp
    
    def create_email(self, email_data):
        
        sender = self.sender
        from_email = self.username
        to_email = email_data['user']

        mail_subject = email_data['subject']
        message = email_data['message']

        msg = MIMEText(message, 'plain')
        msg['To'] = to_email
        msg['From'] = formataddr((sender, from_email))

        if self.bcc != '':
            bcc_email = self.bcc
            msg['bcc'] = bcc_email

        msg['Subject'] = mail_subject

        return msg
    
    def quit_email_server(self, server):

        server.quit()