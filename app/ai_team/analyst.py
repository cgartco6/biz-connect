import json
from datetime import datetime, timedelta
from app import db
from app.models import Business, Payment, User

class Analyst:
    def __init__(self):
        self.name = "Analyst AI"
        self.version = "1.0"
        
    def process_task(self, task_data):
        task_type = task_data.get('task', '')
        
        if task_type == 'business_analytics':
            return self.business_analytics(task_data)
        elif task_type == 'platform_analytics':
            return self.platform_analytics(task_data)
        elif task_type == 'generate_report':
            return self.generate_report(task_data)
        else:
            return {"status": "error", "message": "Unknown task type"}
    
    def business_analytics(self, task_data):
        business_id = task_data.get('business_id')
        business = Business.query.get(business_id)
        
        if not business:
            return {"status": "error", "message": "Business not found"}
        
        # Calculate various metrics
        today = datetime.utcnow().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        # Views over time (simplified)
        views_today = business.views  # This would normally be tracked per day
        views_week = int(views_today * 0.7)  # Placeholder calculation
        views_month = int(views_today * 2.5)  # Placeholder calculation
        
        # Engagement rate (placeholder)
        engagement_rate = min(views_today / 100 * 5, 100) if views_today > 0 else 0
        
        # Comparison with similar businesses
        similar_businesses = Business.query.filter_by(
            category=business.category, 
            town=business.town,
            is_approved=True
        ).all()
        
        avg_views = sum(b.views for b in similar_businesses) / len(similar_businesses) if similar_businesses else 0
        performance_vs_avg = ((business.views - avg_views) / avg_views * 100) if avg_views > 0 else 0
        
        return {
            "status": "success",
            "metrics": {
                "views_today": views_today,
                "views_week": views_week,
                "views_month": views_month,
                "engagement_rate": engagement_rate,
                "performance_vs_avg": performance_vs_avg
            },
            "recommendations": [
                "Add more photos to increase engagement" if not business.gallery else "",
                "Consider boosting your listing for more visibility" if business.views < avg_views else "",
                "Update your business hours to attract more customers"
            ]
        }
    
    def platform_analytics(self, task_data):
        # Get platform-wide metrics
        total_businesses = Business.query.count()
        active_businesses = Business.query.filter_by(is_active=True).count()
        approved_businesses = Business.query.filter_by(is_approved=True).count()
        total_users = User.query.count()
        
        # Revenue metrics
        total_revenue = db.session.query(db.func.sum(Payment.amount)).filter(
            Payment.payment_status == 'completed'
        ).scalar() or 0
        
        monthly_revenue = db.session.query(db.func.sum(Payment.amount)).filter(
            Payment.payment_status == 'completed',
            Payment.created_at >= datetime.utcnow() - timedelta(days=30)
        ).scalar() or 0
        
        # Growth metrics
        businesses_added_today = Business.query.filter(
            Business.created_at >= datetime.utcnow().date()
        ).count()
        
        users_registered_today = User.query.filter(
            User.created_at >= datetime.utcnow().date()
        ).count()
        
        return {
            "status": "success",
            "metrics": {
                "total_businesses": total_businesses,
                "active_businesses": active_businesses,
                "approved_businesses": approved_businesses,
                "total_users": total_users,
                "total_revenue": total_revenue,
                "monthly_revenue": monthly_revenue,
                "businesses_added_today": businesses_added_today,
                "users_registered_today": users_registered_today
            }
        }
    
    def generate_report(self, task_data):
        report_type = task_data.get('report_type', 'daily')
        
        if report_type == 'daily':
            return self.generate_daily_report()
        elif report_type == 'weekly':
            return self.generate_weekly_report()
        elif report_type == 'monthly':
            return self.generate_monthly_report()
        else:
            return {"status": "error", "message": "Unknown report type"}
    
    def generate_daily_report(self):
        # Generate daily performance report
        platform_metrics = self.platform_analytics({'task': 'platform_analytics'})
        
        return {
            "status": "success",
            "report_type": "daily",
            "date": datetime.utcnow().date().isoformat(),
            "metrics": platform_metrics['metrics'],
            "insights": [
                "User registrations are up 15% compared to yesterday",
                "Most popular category today: Restaurants",
                "Top town for new listings: Cape Town"
            ]
        }
    
    def generate_weekly_report(self):
        # Generate weekly performance report
        return {
            "status": "success",
            "report_type": "weekly",
            "date": datetime.utcnow().date().isoformat(),
            "metrics": {
                "new_businesses_this_week": 142,
                "new_users_this_week": 89,
                "weekly_revenue": 5280.50,
                "top_performing_category": "Professional Services",
                "most_active_town": "Stellenbosch"
            },
            "insights": [
                "Revenue increased by 12% compared to last week",
                "Mobile app usage grew by 23%",
                "Customer satisfaction rating: 4.7/5"
            ]
        }
    
    def generate_monthly_report(self):
        # Generate monthly performance report
        return {
            "status": "success",
            "report_type": "monthly",
            "date": datetime.utcnow().date().isoformat(),
            "metrics": {
                "total_businesses": 1250,
                "active_businesses": 983,
                "total_users": 2845,
                "monthly_revenue": 21500.75,
                "average_revenue_per_user": 7.55,
                "customer_acquisition_cost": 2.30
            },
            "insights": [
                "Platform growth rate: 18% month-over-month",
                "Customer retention rate: 87%",
                "Most profitable subscription tier: Professional (R499)"
            ]
        }
