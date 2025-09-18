import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Basic configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # File upload configuration
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    # Email configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['admin@capebizconnect.co.za']
    
    # Payment configuration (PayFast)
    PAYFAST_MERCHANT_ID = os.environ.get('PAYFAST_MERCHANT_ID') or '10000100'
    PAYFAST_MERCHANT_KEY = os.environ.get('PAYFAST_MERCHANT_KEY') or '46f0cd694581a'
    PAYFAST_SANDBOX = os.environ.get('PAYFAST_SANDBOX', 'True').lower() == 'true'
    PAYFAST_RETURN_URL = os.environ.get('PAYFAST_RETURN_URL') or 'http://localhost:5000/payment/success'
    PAYFAST_CANCEL_URL = os.environ.get('PAYFAST_CANCEL_URL') or 'http://localhost:5000/payment/cancel'
    PAYFAST_NOTIFY_URL = os.environ.get('PAYFAST_NOTIFY_URL') or 'http://localhost:5000/payment/notify'
    
    # AI configuration
    AI_LOG_FILE = os.path.join(basedir, 'ai_activity.log')
    
    # Platform settings
    PLATFORM_NAME = 'CapeBiz Connect'
    PLATFORM_DOMAIN = os.environ.get('PLATFORM_DOMAIN') or 'localhost:5000'
    SUPPORT_EMAIL = 'support@capebizconnect.co.za'
    
    # Subscription plans
    SUBSCRIPTION_PLANS = {
        'free': {
            'price': 0,
            'features': ['Basic listing', '1 photo', 'Contact information']
        },
        'starter': {
            'price': 199,
            'features': ['5 photos', 'Website link', 'Social media links', 'Basic analytics']
        },
        'professional': {
            'price': 499,
            'features': ['10 photos', 'SEO optimization', 'Featured placement', 'Advanced analytics']
        },
        'premium': {
            'price': 999,
            'features': ['20 photos', 'Video showcase', 'Priority support', 'Detailed reports', 'Monthly boost credit']
        },
        'enterprise': {
            'price': 1599,
            'features': ['Unlimited photos', 'Video showcase', 'Dedicated support', 'Custom analytics', 'API access']
        }
    }

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app-dev.db')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app-test.db')
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Email errors to administrators
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.SUPPORT_EMAIL,
            toaddrs=cls.ADMINS,
            subject=f'{cls.PLATFORM_NAME} Application Error',
            credentials=credentials,
            secure=secure
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
