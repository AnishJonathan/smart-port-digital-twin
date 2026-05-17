from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models.ship import Ship
from database import db
from utils.decorators import role_required

ships_bp = Blueprint('ships', __name__)

@ships_bp.route('/')
@login_required
@role_required('Port Manager', 'Logistics Officer')
def index():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = Ship.query
    if search:
        query = query.filter(Ship.ship_name.ilike(f'%{search}%'))
        
    pagination = query.order_by(Ship.arrival_time.desc()).paginate(page=page, per_page=10, error_out=False)
    
    return render_template('ships/index.html', ships=pagination.items, pagination=pagination, search=search)

@ships_bp.route('/add', methods=['POST'])
@login_required
@role_required('Port Manager')
def add():
    ship_name = request.form.get('ship_name')
    destination = request.form.get('destination')
    cargo_capacity = request.form.get('cargo_capacity', type=int)
    
    if not all([ship_name, destination, cargo_capacity]):
        flash("All fields are required.", "danger")
    else:
        ship = Ship(ship_name=ship_name, destination=destination, cargo_capacity=cargo_capacity)
        db.session.add(ship)
        db.session.commit()
        flash("Ship added successfully.", "success")
        
    return redirect(url_for('ships.index'))

@ships_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
@role_required('Port Manager')
def delete(id):
    ship = Ship.query.get_or_404(id)
    db.session.delete(ship)
    db.session.commit()
    flash("Ship deleted.", "success")
    return redirect(url_for('ships.index'))
