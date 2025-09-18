import json
from datetime import datetime
from app import db
from app.models import Payment, SubscriptionPlan
from app.utils.payments import payfast

class Accountant:
    def __init__(self):
        self.name = "Accountant AI"
        self.version = "1.0"
        
    def process_task(self, task_data):
        task_type = task_data.get('task', '')
        
        if task_type == 'process_payment':
            return self.process_payment(task_data)
        elif task_type == 'generate_invoice':
            return self.generate_invoice(task_data)
        elif task_type == 'subscription_renewal':
            return self.handle_subscription_renewal(task_data)
        else:
            return {"status": "error", "message": "Unknown task type"}
    
    def process_payment(self, task_data):
        user_id = task_data.get('user_id')
        amount = task_data.get('amount')
        payment_type = task_data.get('payment_type')
        item_id = task_data.get('item_id')
        
        # Create payment record
        payment = Payment(
            user_id=user_id,
            amount=amount,
            payment_type=payment_type,
            item_id=item_id,
            payment_status='pending'
        )
        
        db.session.add(payment)
        db.session.commit()
        
        # Generate payment data for PayFast
        if payment_type == 'subscription':
            plan = SubscriptionPlan.query.get(item_id)
            item_name = f"{plan.name} Subscription"
        elif payment_type == 'boost':
            from app.models import Business
            business = Business.query.get(item_id)
            item_name = f"Boost for {business.name}"
        else:
            item_name = "CapeBiz Connect Payment"
        
        payment_data = payfast.create_payment(
            amount=amount,
            item_name=item_name,
            return_url=f"http://yourdomain.com/payment/success/{payment.id}",
            cancel_url=f"http://yourdomain.com/payment/cancel/{payment.id}",
            notify_url=f"http://yourdomain.com/payment/notify/{payment.id}",
            email_address=task_data.get('email'),
            custom_str1=str(payment.id)
        )
        
        return {"status": "success", "payment_data": payment_data, "payment_id": payment.id}
    
    def generate_invoice(self, task_data):
        payment_id = task_data.get('payment_id')
        payment = Payment.query.get(payment_id)
        
        if not payment:
            return {"status": "error", "message": "Payment not found"}
        
        # Generate invoice details
        invoice = {
            "invoice_id": f"INV-{payment.id:06d}",
            "date": datetime.utcnow().strftime("%Y-%m-%d"),
            "payment_id": payment.id,
            "amount": payment.amount,
            "currency": payment.currency,
            "status": payment.payment_status,
            "description": f"Payment for {payment.payment_type}"
        }
        
        return {"status": "success", "invoice": invoice}
    
    def handle_subscription_renewal(self, task_data):
        # Check for expiring subscriptions and send renewal reminders
        from app.models import Business
        from app.utils.email import send_renewal_reminder
        
        # Find businesses with subscriptions expiring in 3 days
        three_days_from_now = datetime.utcnow() + timedelta(days=3)
        expiring_businesses = Business.query.filter(
            Business.subscription_expiry <= three_days_from_now,
            Business.subscription_tier != 'free'
        ).all()
        
        for business in expiring_businesses:
            send_renewal_reminder(business)
            
        return {"status": "success", "message": f"Sent renewal reminders to {len(expiring_businesses)} businesses"}
