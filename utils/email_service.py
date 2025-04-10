from flask import current_app
from flask_mail import Message
from extensions import mail
from bs4 import BeautifulSoup
from flask import render_template


def strip_tags(html):
    return BeautifulSoup(html, 'html.parser').get_text()


def send_email(subject, to, context, template):
    try:
        # دسترسی به تنظیمات ایمیل
        default_sender = current_app.config['MAIL_DEFAULT_SENDER']

        # ایجاد محتوای HTML ایمیل
        html_message = render_template(template, **context)

        # ایجاد پیام ایمیل
        msg = Message(subject=subject, recipients=[to], sender=default_sender)
        msg.html = html_message
        msg.body = strip_tags(html_message)

        # ارسال ایمیل
        mail.send(msg)

    except Exception as e:
        print(f"Error sending email: {e}")
