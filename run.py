from app import create_app
from app.models import User, Business, Town, SubscriptionPlan
from app import db
import os

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db, 
        'User': User, 
        'Business': Business,
        'Town': Town,
        'SubscriptionPlan': SubscriptionPlan
    }

@app.cli.command("init-db")
def init_db():
    """Initialize the database with default data"""
    db.create_all()
    
    # Create default towns
    towns = [
        {'name': 'Cape Town', 'region': 'City of Cape Town', 'description': 'The legislative capital of South Africa'},
        {'name': 'Stellenbosch', 'region': 'Winelands', 'description': 'Famous for its vineyards and Cape Dutch architecture'},
        {'name': 'Franschhoek', 'region': 'Winelands', 'description': 'Picturesque valley known for French-inspired cuisine and wines'},
        {'name': 'Paarl', 'region': 'Winelands', 'description': 'Known for its pearl-like granite rocks and wine production'},
        {'name': 'Worcester', 'region': 'Breede Valley', 'description': 'Largest town in the Breede River Valley'},
        {'name': 'Hermanus', 'region': 'Overberg', 'description': 'Popular whale watching destination'},
        {'name': 'George', 'region': 'Garden Route', 'description': 'The capital of the Garden Route'},
        {'name': 'Knysna', 'region': 'Garden Route', 'description': 'Known for its forests and lagoon'},
        {'name': 'Plettenberg Bay', 'region': 'Garden Route', 'description': 'Upscale beach resort town'},
        {'name': 'Mossel Bay', 'region': 'Garden Route', 'description': 'Historical town with beautiful beaches'},
        {'name': 'Oudtshoorn', 'region': 'Little Karoo', 'description': 'Ostrich capital of the world'},
        {'name': 'Swellendam', 'region': 'Overberg', 'description': 'Third oldest town in South Africa'}
    ]
    
    for town_data in towns:
        town = Town.query.filter_by(name=town_data['name']).first()
        if not town:
            town = Town(**town_data)
            db.session.add(town)
    
    # Create subscription plans
    plans = [
        {'name': 'Free', 'code': 'free', 'price': 0, 'duration_days': 36500, 'features': 'Basic listing, 1 photo, Contact information'},
        {'name': 'Starter', 'code': 'starter', 'price': 199, 'duration_days': 30, 'features': '5 photos, Website link, Social media links, Basic analytics'},
        {'name': 'Professional', 'code': 'professional', 'price': 499, 'duration_days': 30, 'features': '10 photos, SEO optimization, Featured placement, Advanced analytics'},
        {'name': 'Premium', 'code': 'premium', 'price': 999, 'duration_days': 30, 'features': '20 photos, Video showcase, Priority support, Detailed reports, Monthly boost credit'},
        {'name': 'Enterprise', 'code': 'enterprise', 'price': 1599, 'duration_days': 30, 'features': 'Unlimited photos, Video showcase, Dedicated support, Custom analytics, API access'}
    ]
    
    for plan_data in plans:
        plan = SubscriptionPlan.query.filter_by(code=plan_data['code']).first()
        if not plan:
            plan = SubscriptionPlan(**plan_data)
            db.session.add(plan)
    
    db.session.commit()
    print("Database initialized with default data.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
