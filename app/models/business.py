from app import db
from app.models.database import BaseModel

class Town(BaseModel):
    __tablename__ = 'towns'
    
    name = db.Column(db.String(100), unique=True, nullable=False)
    region = db.Column(db.String(100))
    description = db.Column(db.Text)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    
    def __repr__(self):
        return f'<Town {self.name}>'

class Business(BaseModel):
    __tablename__ = 'businesses'
    
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    town = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    website = db.Column(db.String(200))
    facebook = db.Column(db.String(200))
    twitter = db.Column(db.String(200))
    instagram = db.Column(db.String(200))
    
    # Media
    logo = db.Column(db.String(200))
    cover_image = db.Column(db.String(200))
    gallery = db.Column(db.Text)  # JSON string of image paths
    
    # Business details
    operating_hours = db.Column(db.Text)  # JSON string
    services = db.Column(db.Text)  # JSON string
    tags = db.Column(db.Text)  # Comma-separated values
    
    # Status and visibility
    is_approved = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)
    is_verified = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    
    # Subscription details
    subscription_tier = db.Column(db.String(20), default='free')
    subscription_expiry = db.Column(db.DateTime)
    
    # Analytics
    views = db.Column(db.Integer, default=0)
    clicks = db.Column(db.Integer, default=0)
    shares = db.Column(db.Integer, default=0)
    
    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'town': self.town,
            'address': self.address,
            'email': self.email,
            'phone': self.phone,
            'website': self.website,
            'logo': self.logo,
            'is_verified': self.is_verified,
            'is_featured': self.is_featured,
            'subscription_tier': self.subscription_tier,
            'views': self.views,
            'clicks': self.clicks
        }
    
    def __repr__(self):
        return f'<Business {self.name}>'
