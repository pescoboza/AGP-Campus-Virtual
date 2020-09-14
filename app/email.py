from threading import Thread
from flask import current_app, render_template
from flask_mail import Message

from . import mail

def send_async_email(app, msg):
    with app.app_context():
        # print("[DEBUG] Sent wiht credentials: username: {}, password: {}".format(
        #     app.config["MAIL_SENDER"],app.config["MAIL_PASSWORD"]            
        # ))
        mail.send(msg)

def send_email(to, subject, template_no_ext, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config["MAIL_SUBJECT_PREFIX"] + ' ' + subject,
                    sender=app.config["MAIL_SENDER"], recipients=[to])
    msg.body = render_template(template_no_ext + ".txt", **kwargs)
    msg.html = render_template(template_no_ext + ".html", **kwargs)
    thread = Thread(target=send_async_email, args=[app, msg])
    thread.start()
    return thread