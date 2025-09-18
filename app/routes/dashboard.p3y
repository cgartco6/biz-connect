from flask import render_template, session, redirect, url_for, jsonify
from app import db
from app.models import Business, User
from app.ai_team import analyst, concierge

def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user = User.query.get(session['user_id'])
    businesses = Business.query.filter_by(user_id=user.id).all()
    
    # Get analytics from AI Analyst
    business_data = [b.to_dict() for b in businesses]
    analytics = analyst.process_task({
        'task': 'business_analytics',
        'businesses': business_data
    })
    
    return render_template('dashboard/owner.html', 
                         user=user, 
                         businesses=businesses,
                         analytics=analytics)

def renew_listing(listing_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'})
    
    business = Business.query.filter_by(id=listing_id, user_id=session['user_id']).first()
    if not business:
        return jsonify({'success': False, 'error': 'Listing not found'})
    
    # Use AI Concierge to send renewal reminder
    concierge.process_task({
        'task': 'renewal_reminder',
        'business_id': business.id,
        'business_name': business.name,
        'owner_email': business.user.email
    })
    
    return jsonify({'success': True, 'message': 'Renewal process initiated'})
