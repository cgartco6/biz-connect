from flask import Blueprint, render_template, request, jsonify, session
from app.models import Business, Town
from app.ai_team.curator import Curator

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Get featured businesses
    featured_businesses = Business.query.filter_by(is_featured=True, is_approved=True).limit(6).all()
    
    # Get popular categories
    categories = Business.query.with_entities(Business.category).distinct().all()
    categories = [cat[0] for cat in categories if cat[0]]
    
    return render_template('index.html', 
                         featured_businesses=featured_businesses,
                         categories=categories)

@main_bp.route('/search')
def search():
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    town = request.args.get('town', '')
    
    # Build query
    businesses_query = Business.query.filter_by(is_approved=True)
    
    if query:
        businesses_query = businesses_query.filter(
            (Business.name.ilike(f'%{query}%')) | 
            (Business.description.ilike(f'%{query}%'))
        )
    
    if category:
        businesses_query = businesses_query.filter_by(category=category)
    
    if town:
        businesses_query = businesses_query.filter_by(town=town)
    
    businesses = businesses_query.all()
    
    # Get all towns for filter
    towns = Town.query.all()
    
    # Get all categories for filter
    categories = Business.query.with_entities(Business.category).distinct().all()
    categories = [cat[0] for cat in categories if cat[0]]
    
    return render_template('listings.html', 
                         businesses=businesses,
                         towns=towns,
                         categories=categories,
                         search_query=query,
                         selected_category=category,
                         selected_town=town)

@main_bp.route('/town/<town_name>')
def town_page(town_name):
    town = Town.query.filter_by(name=town_name).first()
    if not town:
        return "Town not found", 404
    
    businesses = Business.query.filter_by(town=town_name, is_approved=True).all()
    
    return render_template('town.html', town=town, businesses=businesses)

@main_bp.route('/category/<category_name>')
def category_page(category_name):
    businesses = Business.query.filter_by(category=category_name, is_approved=True).all()
    
    return render_template('category.html', category=category_name, businesses=businesses)

@main_bp.route('/business/<int:business_id>')
def business_page(business_id):
    business = Business.query.get_or_404(business_id)
    
    # Increment view count
    business.views += 1
    
    # Update analytics
    from app.ai_team.analyst import Analyst
    analyst = Analyst()
    analyst.process_task({
        'task': 'track_business_view',
        'business_id': business_id,
        'view_data': {
            'timestamp': 'now',
            'user_agent': request.headers.get('User-Agent'),
            'ip_address': request.remote_addr
        }
    })
    
    return render_template('business.html', business=business)
