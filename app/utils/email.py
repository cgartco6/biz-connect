from flask_mail import Message
from flask import current_app, render_template
from threading import Thread
from app import mail

def send_async_email(app, msg):
    """Send email asynchronously"""
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body, attachments=None, sync=False):
    """Send email with optional attachments"""
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    
    if attachments:
        for attachment in attachments:
            msg.attach(*attachment)
    
    if sync:
        mail.send(msg)
    else:
        Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()

def send_password_reset_email(user):
    """Send password reset email"""
    token = user.get_reset_password_token()
    send_email(
        '[CapeBiz Connect] Reset Your Password',
        sender=current_app.config['ADMINS'][0],
        recipients=[user.email],
        text_body=render_template('email/reset_password.txt', user=user, token=token),
        html_body=render_template('email/reset_password.html', user=user, token=token)
    )

def send_listing_approval_email(business):
    """Send listing approval email"""
    send_email(
        f'[CapeBiz Connect] Your Listing "{business.name}" Has Been Approved',
        sender=current_app.config['ADMINS'][0],
        recipients=[business.user.email],
        text_body=render_template('email/listing_approved.txt', business=business),
        html_body=render_template('email/listing_approved.html', business=business)
    )

def send_renewal_reminder(business):
    """Send renewal reminder email"""
    send_email(
        f'[CapeBiz Connect] Renew Your Listing for "{business.name}"',
        sender=current_app.config['ADMINS'][0],
        recipients=[business.user.email],
        text_body=render_template('email/renewal_reminder.txt', business=business),
        html_body=render_template('email/renewal_reminder.html', business=business)
    )

def send_payment_confirmation(payment):
    """Send payment confirmation email"""
    send_email(
        f'[CapeBiz Connect] Payment Confirmation for {payment.description}',
        sender=current_app.config['ADMINS'][0],
        recipients=[payment.user.email],
        text_body=render_template('email/payment_confirmation.txt', payment=payment),
        html_body=render_template('email/payment_confirmation.html', payment=payment)
    )
