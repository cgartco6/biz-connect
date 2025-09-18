from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Business, Town
from app.forms import BusinessForm
from app.utils.security import sanitize_input

business_bp = Blueprint('business', __name__, url_prefix='/business')

@business_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_business():
    form = BusinessForm()
    
    # Populate towns dropdown
    form.town.choices = [(t.name, t.name) for t in Town.query.order_by('name').all()]
    
    if form.validate_on_submit():
        # Create new business
        business = Business(
            name=sanitize_input(form.name.data),
            description=sanitize_input(form.description.data),
            category=form.category.data,
            town=form.town.data,
            address=sanitize_input(form.address.data),
            email=form.email.data,
            phone=form.phone.data,
            website=form.website.data,
            facebook=form.facebook.data,
            twitter=form.twitter.data,
            instagram=form.instagram.data,
            user_id=current_user.id
        )
        
        db.session.add(business)
        db.session.commit()
        
        # Review listing with AI Curator
        from app.ai_team.curator import Curator
        curator = Curator()
        review_result = curator.process_task({
            'task': 'review_listing',
            'business_id': business.id
        })
        
        # Categorize business with AI Curator
        categorization_result = curator.process_task({
            'task': 'categorize_business',
            'business_id': business.id
        })
        
        flash('Business added successfully! It will be visible after approval.', 'success')
        return redirect(url_for('dashboard.owner_dashboard'))
    
    return render_template('business/add.html', title='Add Business', form=form)

@business_bp.route('/edit/<int:business_id>', methods=['GET', 'POST'])
@login_required
def edit_business(business_id):
    business = Business.query.get_or_404(business_id)
    
    # Check if user owns this business
    if business.user_id != current_user.id and not current_user.is_admin:
        flash('You do not have permission to edit this business.', 'danger')
        return redirect(url_for('main.index'))
    
    form = BusinessForm(obj=business)
    
    # Populate towns dropdown
    form.town.choices = [(t.name, t.name) for t in Town.query.order_by('name').all()]
    
    if form.validate_on_submit():
        business.name = sanitize_input(form.name.data)
        business.description = sanitize_input(form.description.data)
        business.category = form.category.data
        business.town = form.town.data
        business.address = sanitize_input(form.address.data)
        business.email = form.email.data
        business.phone = form.phone.data
        business.website = form.website.data
        business.facebook = form.facebook.data
        business.twitter = form.twitter.data
        business.instagram = form.instagram.data
        
        db.session.commit()
        
        flash('Business updated successfully!', 'success')
        return redirect(url_for('dashboard.owner_dashboard'))
    
    return render_template('business/edit.html', title='Edit Business', form=form, business=business)

@business_bp.route('/delete/<int:business_id>', methods=['POST'])
@login_required
def delete_business(business_id):
    business = Business.query.get_or_404(business_id)
    
    # Check if user owns this business
    if business.user_id != current_user.id and not current_user.is_admin:
        flash('You do not have permission to delete this business.', 'danger')
        return redirect(url_for('main.index'))
    
    db.session.delete(business)
    db.session.commit()
    
    flash('Business deleted successfully!', 'success')
    return redirect(url_for('dashboard.owner_dashboard'))

@business_bp.route('/boost/<int:business_id>', methods=['POST'])
@login_required
def boost_business(business_id):
    business = Business.query.get_or_404(business_id)
    
    # Check if user owns this business
    if business.user_id != current_user.id and not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Permission denied'})
    
    # Process payment through AI Accountant
    from app.ai_team.accountant import Accountant
    accountant = Accountant()
    payment_result = accountant.process_task({
        'task': 'process_payment',
        'user_id': current_user.id,
        'amount': 99.00,
        'payment_type': 'boost',
        'item_id': business_id,
        'email': current_user.email
    })
    
    if payment_result['status'] == 'success':
        return jsonify({
            'success': True,
            'message': 'Boost payment processed',
            'payment_data': payment_result['payment_data']
        })
    else:
        return jsonify({
            'success': False,
            'message': payment_result.get('message', 'Payment failed')
        })
