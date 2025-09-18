import json
from datetime import datetime
from app import db
from app.models import User, Business
from app.utils.email import send_email

class Concierge:
    def __init__(self):
        self.name = "Concierge AI"
        self.version = "1.0"
        
    def process_task(self, task_data):
        task_type = task_data.get('task', '')
        
        if task_type == 'welcome_new_user':
            return self.welcome_new_user(task_data)
        elif task_type == 'listing_approved':
            return self.listing_approved(task_data)
        elif task_type == 'renewal_reminder':
            return self.renewal_reminder(task_data)
        elif task_type == 'customer_support':
            return self.handle_customer_support(task_data)
        else:
            return {"status": "error", "message": "Unknown task type"}
    
    def welcome_new_user(self, task_data):
        user_id = task_data.get('user_id')
        user = User.query.get(user_id)
        
        if not user:
            return {"status": "error", "message": "User not found"}
        
        # Send welcome email
        send_email(
            subject="Welcome to CapeBiz Connect!",
            sender="noreply@capebizconnect.co.za",
            recipients=[user.email],
            text_body=f"""
Hi {user.first_name or 'there'},

Welcome to CapeBiz Connect! We're excited to have you on board.

With CapeBiz Connect, you can:
- List your business for free
- Reach customers across the Western Cape
- Boost your visibility with our affordable promotion options

Get started by adding your first business listing.

Best regards,
The CapeBiz Connect Team
            """,
            html_body=f"""
<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
    <h2>Welcome to CapeBiz Connect!</h2>
    <p>Hi {user.first_name or 'there'},</p>
    <p>We're excited to have you on board.</p>
    <p>With CapeBiz Connect, you can:</p>
    <ul>
        <li>List your business for free</li>
        <li>Reach customers across the Western Cape</li>
        <li>Boost your visibility with our affordable promotion options</li>
    </ul>
    <p>Get started by adding your first business listing.</p>
    <p>Best regards,<br>The CapeBiz Connect Team</p>
</div>
            """
        )
        
        return {"status": "success", "message": "Welcome email sent"}
    
    def listing_approved(self, task_data):
        business_id = task_data.get('business_id')
        business = Business.query.get(business_id)
        
        if not business:
            return {"status": "error", "message": "Business not found"}
        
        # Send approval notification
        send_email(
            subject=f"Your listing '{business.name}' has been approved!",
            sender="noreply@capebizconnect.co.za",
            recipients=[business.owner.email],
            text_body=f"""
Hi {business.owner.first_name or 'there'},

Great news! Your business listing '{business.name}' has been approved and is now live on CapeBiz Connect.

You can view your listing here: http://yourdomain.com/business/{business.id}

To maximize your visibility, consider:
1. Adding more photos to your listing
2. Using our Boost feature to get featured placement
3. Upgrading to a premium subscription for more benefits

Thank you for choosing CapeBiz Connect.

Best regards,
The CapeBiz Connect Team
            """,
            html_body=f"""
<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
    <h2>Your listing has been approved!</h2>
    <p>Hi {business.owner.first_name or 'there'},</p>
    <p>Great news! Your business listing '<strong>{business.name}</strong>' has been approved and is now live on CapeBiz Connect.</p>
    <p>You can <a href="http://yourdomain.com/business/{business.id}">view your listing here</a>.</p>
    <p>To maximize your visibility, consider:</p>
    <ol>
        <li>Adding more photos to your listing</li>
        <li>Using our Boost feature to get featured placement</li>
        <li>Upgrading to a premium subscription for more benefits</li>
    </ol>
    <p>Thank you for choosing CapeBiz Connect.</p>
    <p>Best regards,<br>The CapeBiz Connect Team</p>
</div>
            """
        )
        
        return {"status": "success", "message": "Approval notification sent"}
    
    def renewal_reminder(self, task_data):
        business_id = task_data.get('business_id')
        business = Business.query.get(business_id)
        
        if not business:
            return {"status": "error", "message": "Business not found"}
        
        # Send renewal reminder
        send_email(
            subject=f"Renew your subscription for '{business.name}'",
            sender="noreply@capebizconnect.co.za",
            recipients=[business.owner.email],
            text_body=f"""
Hi {business.owner.first_name or 'there'},

Your subscription for '{business.name}' is expiring soon. To maintain your premium features and visibility, please renew your subscription.

You can renew by visiting your dashboard: http://yourdomain.com/dashboard

If you have any questions, please reply to this email.

Best regards,
The CapeBiz Connect Team
            """,
            html_body=f"""
<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
    <h2>Renew your subscription</h2>
    <p>Hi {business.owner.first_name or 'there'},</p>
    <p>Your subscription for '<strong>{business.name}</strong>' is expiring soon. To maintain your premium features and visibility, please renew your subscription.</p>
    <p>You can <a href="http://yourdomain.com/dashboard">renew by visiting your dashboard</a>.</p>
    <p>If you have any questions, please reply to this email.</p>
    <p>Best regards,<br>The CapeBiz Connect Team</p>
</div>
            """
        )
        
        return {"status": "success", "message": "Renewal reminder sent"}
    
    def handle_customer_support(self, task_data):
        # This would integrate with a support ticket system
        # For now, just log the request
        support_request = {
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": task_data.get('user_id'),
            "subject": task_data.get('subject'),
            "message": task_data.get('message'),
            "status": "received"
        }
        
        # In a real implementation, this would save to a database
        print(f"Support request received: {support_request}")
        
        # Send acknowledgment
        if task_data.get('user_email'):
            send_email(
                subject="We've received your support request",
                sender="noreply@capebizconnect.co.za",
                recipients=[task_data.get('user_email')],
                text_body=f"""
Thank you for contacting CapeBiz Connect support.

We've received your request and will get back to you within 24 hours.

Request details:
Subject: {task_data.get('subject')}
Message: {task_data.get('message')}

Best regards,
CapeBiz Connect Support Team
                """,
                html_body=f"""
<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
    <h2>We've received your support request</h2>
    <p>Thank you for contacting CapeBiz Connect support.</p>
    <p>We've received your request and will get back to you within 24 hours.</p>
    <p><strong>Request details:</strong></p>
    <p>Subject: {task_data.get('subject')}</p>
    <p>Message: {task_data.get('message')}</p>
    <p>Best regards,<br>CapeBiz Connect Support Team</p>
</div>
                """
            )
        
        return {"status": "success", "message": "Support request logged"}
