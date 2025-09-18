import requests
from flask import current_app, url_for
import hashlib
import urllib.parse

class PayFast:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        self.merchant_id = app.config['PAYFAST_MERCHANT_ID']
        self.merchant_key = app.config['PAYFAST_MERCHANT_KEY']
        self.sandbox = app.config['PAYFAST_SANDBOX']
        self.return_url = app.config.get('PAYFAST_RETURN_URL', '')
        self.cancel_url = app.config.get('PAYFAST_CANCEL_URL', '')
        self.notify_url = app.config.get('PAYFAST_NOTIFY_URL', '')
        
        if self.sandbox:
            self.base_url = 'https://sandbox.payfast.co.za/onsite/process'
        else:
            self.base_url = 'https://www.payfast.co.za/onsite/process'
    
    def generate_signature(self, data, pass_phrase=None):
        """Generate PayFast signature for security"""
        # Create parameter string
        pf_output = []
        for key in sorted(data.keys()):
            if data[key] != '':
                pf_output.append(f"{key}={urllib.parse.quote_plus(data[key].replace('+', ' '))}")
        
        # Append passphrase if provided
        if pass_phrase:
            pf_output.append(f"passphrase={urllib.parse.quote_plus(pass_phrase.replace('+', ' '))}")
        
        # Concatenate parameters
        return_string = '&'.join(pf_output)
        
        # Generate MD5 hash
        return hashlib.md5(return_string.encode()).hexdigest()
    
    def create_payment(self, amount, item_name, return_url, cancel_url, notify_url, 
                      email_address=None, custom_str1=None, custom_str2=None):
        """Create a payment request"""
        data = {
            'merchant_id': self.merchant_id,
            'merchant_key': self.merchant_key,
            'return_url': return_url,
            'cancel_url': cancel_url,
            'notify_url': notify_url,
            'amount': str(amount),
            'item_name': item_name,
        }
        
        if email_address:
            data['email_address'] = email_address
        
        if custom_str1:
            data['custom_str1'] = custom_str1
        
        if custom_str2:
            data['custom_str2'] = custom_str2
        
        # Generate signature
        data['signature'] = self.generate_signature(data)
        
        return data
    
    def verify_notification(self, data, pass_phrase=None):
        """Verify PayFast ITN notification"""
        # Create copy of data
        verify_data = data.copy()
        
        # Get signature from data
        signature = verify_data.pop('signature', '')
        
        # Generate our signature
        our_signature = self.generate_signature(verify_data, pass_phrase)
        
        return signature == our_signature

# Initialize PayFast extension
payfast = PayFast()

def init_payment(app):
    """Initialize payment system with app"""
    payfast.init_app(app)
    return payfast
