from app import db
from app.models.database import BaseModel
from datetime import datetime, timedelta

class SubscriptionPlan(BaseModel):
    __tablename__ = 'subscription_plans'
    
    name = db.Column(db.String(50), nullable=False)
    code = db.Column(db.String(20), nullable=False)  # free, starter, professional, etc.
    price = db.Column(db.Float, nullable=False)
    duration_days = db.Column(db.Integer, default=30)
    features = db.Column(db.Text)  # JSON string of features
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<SubscriptionPlan {self.name}>'

class Payment(BaseModel):
    __tablename__ = 'payments'
    
    # Payment details
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='ZAR')
    payment_method = db.Column(db.String(50))
    payment_status = db.Column(db.String(20), default='pending')  # pending, completed, failed, refunded
    payment_gateway = db.Column(db.String(50))
    gateway_transaction_id = db.Column(db.String(100))
    gateway_response = db.Column(db.Text)
    
    # What the payment is for
    payment_type = db.Column(db.String(20))  # subscription, boost, featured, etc.
    item_id = db.Column(db.Integer)  # ID of the business, subscription plan, etc.
    
    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __repr__(self):
        return f'<Payment {self.id} - {self.amount} {self.currency}>'
    
    def mark_as_completed(self, gateway_transaction_id, response_data=None):
        self.payment_status = 'completed'
        self.gateway_transaction_id = gateway_transaction_id
        if response_data:
            self.gateway_response = str(response_data)
        
        # If this is a subscription payment, update the business
        if self.payment_type == 'subscription':
            from app.models.business import Business
            business = Business.query.get(self.item_id)
            if business:
                plan = SubscriptionPlan.query.get(int(self.gateway_response))
                if plan:
                    business.subscription_tier = plan.code
                    if business.subscription_expiry and business.subscription_expiry > datetime.utcnow():
                        business.subscription_expiry += timedelta(days=plan.duration_days)
                    else:
                        business.subscription_expiry = datetime.utcnow() + timedelta(days=plan.duration_days)
        
        # If this is a boost payment, update the business
        elif self.payment_type == 'boost':
            from app.models.business import Business
            business = Business.query.get(self.item_id)
            if business:
                business.is_featured = True
                # Set boost expiry (e.g., 7 days from now)
                boost_expiry = datetime.utcnow() + timedelta(days=7)
                # Store boost expiry in gateway_response if not already used
                if not self.gateway_response:
                    self.gateway_response = f'boost_expiry:{boost_expiry.isoformat()}'
