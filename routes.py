from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from models import db, Listing, Request, Comment, Message, User
from utils import login_required_with_message

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    listings = Listing.query.filter_by(is_active=True).order_by(Listing.created_at.desc()).limit(10).all()
    requests = Request.query.filter_by(is_active=True).order_by(Request.created_at.desc()).limit(10).all()
    return render_template('index.html', listings=listings, requests=requests)

@main_bp.route('/listings')
def listings():
    page = request.args.get('page', 1, type=int)
    listings = Listing.query.filter_by(is_active=True).order_by(Listing.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False)
    return render_template('listings.html', listings=listings)

@main_bp.route('/requests')
def requests():
    page = request.args.get('page', 1, type=int)
    requests = Request.query.filter_by(is_active=True).order_by(Request.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False)
    return render_template('requests.html', requests=requests)

@main_bp.route('/listing/<int:id>')
def listing_detail(id):
    listing = Listing.query.get_or_404(id)
    comments = Comment.query.filter_by(listing_id=id).order_by(Comment.created_at.desc()).all()
    return render_template('listing_detail.html', listing=listing, comments=comments)

@main_bp.route('/request/<int:id>')
def request_detail(id):
    req = Request.query.get_or_404(id)
    comments = Comment.query.filter_by(request_id=id).order_by(Comment.created_at.desc()).all()
    return render_template('request_detail.html', request=req, comments=comments)

@main_bp.route('/new_listing', methods=['GET', 'POST'])
@login_required_with_message
def new_listing():
    if request.method == 'POST':
        listing = Listing(
            title=request.form['title'],
            description=request.form['description'],
            power_amount=float(request.form['power_amount']),
            price_per_kwh=float(request.form['price_per_kwh']),
            location=request.form['location'],
            available_from=datetime.strptime(request.form['available_from'], '%Y-%m-%dT%H:%M'),
            available_until=datetime.strptime(request.form['available_until'], '%Y-%m-%dT%H:%M'),
            seller_id=current_user.id
        )
        
        db.session.add(listing)
        db.session.commit()
        
        flash('出品を作成しました')
        return redirect(url_for('main.listing_detail', id=listing.id))
    
    return render_template('new_listing.html')

@main_bp.route('/new_request', methods=['GET', 'POST'])
@login_required_with_message
def new_request():
    if request.method == 'POST':
        req = Request(
            title=request.form['title'],
            description=request.form['description'],
            power_amount=float(request.form['power_amount']),
            max_price_per_kwh=float(request.form['max_price_per_kwh']),
            location=request.form['location'],
            needed_from=datetime.strptime(request.form['needed_from'], '%Y-%m-%dT%H:%M'),
            needed_until=datetime.strptime(request.form['needed_until'], '%Y-%m-%dT%H:%M'),
            buyer_id=current_user.id
        )
        
        db.session.add(req)
        db.session.commit()
        
        flash('買取リクエストを作成しました')
        return redirect(url_for('main.request_detail', id=req.id))
    
    return render_template('new_request.html')

@main_bp.route('/add_comment', methods=['POST'])
@login_required_with_message
def add_comment():
    content = request.form['content']
    listing_id = request.form.get('listing_id')
    request_id = request.form.get('request_id')
    
    comment = Comment(
        content=content,
        author_id=current_user.id,
        listing_id=listing_id if listing_id else None,
        request_id=request_id if request_id else None
    )
    
    db.session.add(comment)
    db.session.commit()
    
    if listing_id:
        return redirect(url_for('main.listing_detail', id=listing_id))
    else:
        return redirect(url_for('main.request_detail', id=request_id))

@main_bp.route('/mypage')
@login_required_with_message
def mypage():
    user_listings = Listing.query.filter_by(seller_id=current_user.id).order_by(Listing.created_at.desc()).all()
    user_requests = Request.query.filter_by(buyer_id=current_user.id).order_by(Request.created_at.desc()).all()
    return render_template('mypage.html', listings=user_listings, requests=user_requests)

@main_bp.route('/messages')
@login_required_with_message
def message_box():
    received_messages = Message.query.filter_by(receiver_id=current_user.id).order_by(Message.created_at.desc()).all()
    sent_messages = Message.query.filter_by(sender_id=current_user.id).order_by(Message.created_at.desc()).all()
    return render_template('message_box.html', received_messages=received_messages, sent_messages=sent_messages)

@main_bp.route('/send_message/<int:user_id>', methods=['GET', 'POST'])
@login_required_with_message
def send_message(user_id):
    recipient = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        content = request.form['content']
        
        message = Message(
            content=content,
            sender_id=current_user.id,
            receiver_id=user_id
        )
        
        db.session.add(message)
        db.session.commit()
        
        flash('メッセージを送信しました')
        return redirect(url_for('main.message_box'))
    
    return render_template('send_message.html', recipient=recipient)