from flask import Flask, render_template, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from config import Config
from app.ai_team import Architect, Accountant, Concierge, Curator, Sentinel, Analyst, Trainer

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# Initialize AI Team
ai_architect = Architect()
ai_accountant = Accountant()
ai_concierge = Concierge()
ai_curator = Curator()
ai_sentinel = Sentinel()
ai_analyst = Analyst()
ai_trainer = Trainer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/town/<town_name>')
def town_page(town_name):
    # Get businesses for this town
    businesses = Business.query.filter_by(town=town_name, approved=True).all()
    return render_template(f'town/{town_name}.html', businesses=businesses)

@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    product_type = request.form.get('type')  # 'boost' or 'subscription'
    product_id = request.form.get('id')
    
    if 'cart' not in session:
        session['cart'] = []
    
    session['cart'].append({'type': product_type, 'id': product_id})
    session.modified = True
    
    return jsonify({'success': True, 'cart_count': len(session['cart'])})

if __name__ == '__main__':
    app.run(debug=True)
