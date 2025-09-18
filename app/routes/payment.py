from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Payment, SubscriptionPlan, Business
from app.utils.payments import payfast

payment_bp = Blueprint('payment', __name__, url_prefix='/payment')

@payment_bp.route('/subscribe/<int:business_id>/<plan_code>')
@login_required
def subscribe(business_id, plan_code):
    business = Business.query.get_or_404(business_id)
    
    # Check if user owns this business
    if business.user_id != current_user.id and not current_user.is_admin:
        flash('You do not have permission to subscribe for this business.', 'danger')
        return redirect(url_for('main.index'))
    
    # Get subscription plan
    plan = SubscriptionPlan.query.filter_by(code=plan_code, is_active=True).first()
    if not plan:
        flash('Invalid subscription plan.', 'danger')
        return redirect(url_for('dashboard.owner_dashboard'))
    
    # Process payment through AI Accountant
    from app.ai_team.accountant import Accountant
    accountant = Accountant()
    payment_result = accountant.process_task({
        'task': 'process_payment',
        'user_id': current_user.id,
        'amount': plan.price,
        'payment_type': 'subscription',
        'item_id': business_id,
        'email': current_user.email
    })
    
    if payment_result['status'] == 'success':
        # Redirect to PayFast
        return render_template('payment/redirect.html', 
                             payment_data=payment_result['payment_data'],
                             payfast_url=payfast.base_url)
    else:
        flash('Payment processing failed. Please try again.', 'danger')
        return redirect(url_for('dashboard.owner_dashboard'))

@payment_bp.route('/success/<int:payment_id>')
def payment_success(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    
    # Verify payment with PayFast
    if payfast.verify_notification(request.args.to_dict()):
        payment.mark_as_completed(
            request.args.get('pf_payment_id'),
            request.args.to_dict()
        )
        db.session.commit()
        
        flash('Payment completed successfully!', 'success')
    else:
        flash('Payment verification failed.', 'danger')
    
    return redirect(url_for('dashboard.owner_dashboard'))

@payment_bp.route('/cancel/<int:payment_id>')
def payment_cancel(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    payment.payment_status = 'cancelled'
    db.session.commit()
    
    flash('Payment was cancelled.', 'info')
    return redirect(url_for('dashboard.owner_dashboard'))

@payment_bp.route('/notify/<int:payment_id>', methods=['POST'])
def payment_notify(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    
    # Verify ITN notification from PayFast
    if payfast.verify_notification(request.form.to_dict()):
        payment.mark_as_completed(
            request.form.get('pf_payment_id'),
            request.form.to_dict()
        )
        db.session.commit()
        
        return '', 200
    else:
        return '', 400

@payment_bp.route('/plans')
def subscription_plans():
    plans = SubscriptionPlan.query.filter_by(is_active=True).all()
    return render_template('payment/plans.html', title='Subscription Plans', plans=plans)
