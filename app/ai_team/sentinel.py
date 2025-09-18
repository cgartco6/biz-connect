import json
import re
from datetime import datetime, timedelta
from flask import request
from app import db
from app.models import User, LoginAttempt

class Sentinel:
    def __init__(self):
        self.name = "Sentinel AI"
        self.version = "1.0"
        
    def process_task(self, task_data):
        task_type = task_data.get('task', '')
        
        if task_type == 'monitor_security':
            return self.monitor_security(task_data)
        elif task_type == 'check_malicious_activity':
            return self.check_malicious_activity(task_data)
        elif task_type == 'block_suspicious_ip':
            return self.block_suspicious_ip(task_data)
        else:
            return {"status": "error", "message": "Unknown task type"}
    
    def monitor_security(self, task_data):
        # Monitor for suspicious activities
        # Check for multiple failed login attempts
        recent_attempts = LoginAttempt.query.filter(
            LoginAttempt.timestamp > datetime.utcnow() - timedelta(hours=1),
            LoginAttempt.success == False
        ).all()
        
        # Group by IP address
        ip_attempts = {}
        for attempt in recent_attempts:
            if attempt.ip_address in ip_attempts:
                ip_attempts[attempt.ip_address] += 1
            else:
                ip_attempts[attempt.ip_address] = 1
        
        # Check for suspicious patterns
        suspicious_ips = []
        for ip, count in ip_attempts.items():
            if count > 5:  # More than 5 failed attempts in an hour
                suspicious_ips.append(ip)
                
                # Automatically block if too many attempts
                if count > 10:
                    self.block_suspicious_ip({'ip_address': ip})
        
        return {
            "status": "success",
            "suspicious_ips": suspicious_ips,
            "total_attempts": len(recent_attempts)
        }
    
    def check_malicious_activity(self, task_data):
        ip_address = task_data.get('ip_address')
        user_agent = task_data.get('user_agent')
        
        # Check for known malicious patterns
        malicious = False
        reasons = []
        
        # Check user agent for suspicious patterns
        if user_agent:
            suspicious_agents = ['sqlmap', 'nikto', 'wget', 'curl', 'python-requests']
            for agent in suspicious_agents:
                if agent.lower() in user_agent.lower():
                    malicious = True
                    reasons.append(f"Suspicious user agent: {agent}")
        
        # Check for SQL injection patterns in request data
        if request:
            sql_patterns = [
                r'union.*select',
                r'select.*from',
                r'insert.*into',
                r'update.*set',
                r'delete.*from',
                r'drop.*table',
                r'exec.*\(\)',
                r'waitfor.*delay',
                r'--',
                r'\/\*',
                r'\*\/'
            ]
            
            # Check all request values
            for key, values in request.values.lists():
                for value in values:
                    for pattern in sql_patterns:
                        if re.search(pattern, value, re.IGNORECASE):
                            malicious = True
                            reasons.append(f"SQL injection attempt in {key}: {value}")
                            break
        
        return {
            "status": "success",
            "malicious": malicious,
            "reasons": reasons,
            "ip_address": ip_address
        }
    
    def block_suspicious_ip(self, task_data):
        ip_address = task_data.get('ip_address')
        duration_hours = task_data.get('duration_hours', 24)
        
        # Create or update IP block
        existing_block = IPBlock.query.filter_by(ip_address=ip_address).first()
        
        if existing_block:
            existing_block.expires_at = datetime.utcnow() + timedelta(hours=duration_hours)
        else:
            new_block = IPBlock(
                ip_address=ip_address,
                reason="Multiple failed login attempts",
                expires_at=datetime.utcnow() + timedelta(hours=duration_hours)
            )
            db.session.add(new_block)
        
        db.session.commit()
        
        return {"status": "success", "message": f"IP {ip_address} blocked for {duration_hours} hours"}
