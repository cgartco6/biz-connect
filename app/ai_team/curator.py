import json
import re
from datetime import datetime
from app import db
from app.models import Business

class Curator:
    def __init__(self):
        self.name = "Curator AI"
        self.version = "1.0"
        
    def process_task(self, task_data):
        task_type = task_data.get('task', '')
        
        if task_type == 'review_listing':
            return self.review_listing(task_data)
        elif task_type == 'categorize_business':
            return self.categorize_business(task_data)
        elif task_type == 'optimize_seo':
            return self.optimize_seo(task_data)
        else:
            return {"status": "error", "message": "Unknown task type"}
    
    def review_listing(self, task_data):
        business_id = task_data.get('business_id')
        business = Business.query.get(business_id)
        
        if not business:
            return {"status": "error", "message": "Business not found"}
        
        # Check listing quality
        quality_score = 0
        issues = []
        
        # Check description
        if not business.description or len(business.description.strip()) < 50:
            issues.append("Description is too short")
        else:
            quality_score += 20
        
        # Check contact info
        if business.email and business.phone:
            quality_score += 20
        else:
            issues.append("Missing contact information")
        
        # Check category
        if business.category:
            quality_score += 20
        else:
            issues.append("Missing category")
        
        # Check location
        if business.town and business.address:
            quality_score += 20
        else:
            issues.append("Incomplete location information")
        
        # Check images
        if business.logo:
            quality_score += 20
        else:
            issues.append("No logo uploaded")
        
        # Auto-approve if score is high enough
        if quality_score >= 80 and not business.is_approved:
            business.is_approved = True
            db.session.commit()
            
            # Notify concierge to send approval email
            from app.ai_team.concierge import Concierge
            concierge = Concierge()
            concierge.process_task({
                'task': 'listing_approved',
                'business_id': business.id
            })
        
        return {
            "status": "success",
            "quality_score": quality_score,
            "issues": issues,
            "approved": business.is_approved
        }
    
    def categorize_business(self, task_data):
        business_id = task_data.get('business_id')
        business = Business.query.get(business_id)
        
        if not business:
            return {"status": "error", "message": "Business not found"}
        
        # Simple categorization based on keywords in the name and description
        # In a real implementation, this would use ML/NLP
        categories = {
            'restaurant': ['restaurant', 'cafe', 'coffee', 'food', 'eat', 'dine', 'bistro'],
            'retail': ['shop', 'store', 'retail', 'sell', 'market', 'boutique'],
            'service': ['service', 'repair', 'maintenance', 'clean', 'fix', 'install'],
            'professional': ['consult', 'advice', 'law', 'account', 'finance', 'real estate', 'agent'],
            'health': ['health', 'medical', 'doctor', 'dentist', 'clinic', 'pharmacy', 'wellness'],
            'beauty': ['beauty', 'salon', 'spa', 'hair', 'nails', 'massage', 'aesthetics'],
            'automotive': ['car', 'auto', 'vehicle', 'motor', 'tyre', 'mechanic', 'repair'],
            'education': ['school', 'learn', 'teach', 'tutor', 'education', 'training', 'course']
        }
        
        text = f"{business.name} {business.description}".lower()
        best_category = 'other'
        best_score = 0
        
        for category, keywords in categories.items():
            score = sum(1 for keyword in keywords if keyword in text)
            if score > best_score:
                best_score = score
                best_category = category
        
        # Update business category if needed
        if best_category != business.category:
            business.category = best_category
            db.session.commit()
        
        return {"status": "success", "category": best_category}
    
    def optimize_seo(self, task_data):
        business_id = task_data.get('business_id')
        business = Business.query.get(business_id)
        
        if not business:
            return {"status": "error", "message": "Business not found"}
        
        # Generate SEO-friendly description
        seo_description = f"{business.name} - {business.category} in {business.town}, Western Cape. {business.description[:150]}..."
        
        # Generate SEO-friendly title
        seo_title = f"{business.name} - {business.category} in {business.town} | CapeBiz Connect"
        
        # Generate keywords
        keywords = [business.name, business.category, business.town, 'Western Cape', 'South Africa']
        keywords.extend(business.tags.split(',') if business.tags else [])
        
        return {
            "status": "success",
            "seo_title": seo_title,
            "seo_description": seo_description,
            "keywords": keywords
        }
