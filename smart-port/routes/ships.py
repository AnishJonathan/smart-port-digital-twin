from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models.ship import Ship
from models.audit import AuditLog
from database import db
from utils.decorators import role_required

ships_bp = Blueprint('ships', __name__)

@ships_bp.route('/')
@login_required
@role_required('Port Manager', 'Logistics Officer')
def index():
    search = request.args.get('search', '')
    status_filter = request.args.get('status', '')
    sort_by = request.args.get('sort', 'latest')
    
    query = Ship.query
    if search:
        query = query.filter(Ship.ship_name.ilike(f'%{search}%'))
    if status_filter:
        query = query.filter_by(status=status_filter)
        
    if sort_by == 'latest':
        query = query.order_by(Ship.arrival_time.desc())
    elif sort_by == 'oldest':
        query = query.order_by(Ship.arrival_time.asc())
    elif sort_by == 'status':
        query = query.order_by(Ship.status.asc())
        
    ships = query.all()
    
    return render_template('ships/index.html', ships=ships, search=search, status_filter=status_filter, sort_by=sort_by)

@ships_bp.route('/add', methods=['POST'])
@login_required
@role_required() # Admin only
def add():
    ship_name = request.form.get('ship_name')
    destination = request.form.get('destination')
    cargo_capacity = request.form.get('cargo_capacity', type=int)
    
    if not all([ship_name, destination, cargo_capacity]):
        flash("All fields are required.", "danger")
    else:
        ship = Ship(ship_name=ship_name, destination=destination, cargo_capacity=cargo_capacity)
        db.session.add(ship)
        
        audit = AuditLog(user=current_user.name, action="Created Ship", target=ship_name)
        db.session.add(audit)
        
        db.session.commit()
        flash("Ship added successfully.", "success")
        
    return redirect(url_for('ships.index'))

@ships_bp.route('/update_status/<int:id>', methods=['POST'])
@login_required
@role_required('Port Manager') # Admin implicitly allowed
def update_status(id):
    ship = Ship.query.get_or_404(id)
    new_status = request.form.get('status')
    
    if new_status:
        old_status = ship.status
        ship.status = new_status
        audit = AuditLog(user=current_user.name, action=f"Updated Ship Status ({old_status} → {new_status})", target=ship.ship_name)
        db.session.add(audit)
        db.session.commit()
        flash(f"Ship status updated to {new_status}.", "success")
        
    return redirect(url_for('ships.index'))

@ships_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
@role_required() # Admin only
def delete(id):
    ship = Ship.query.get_or_404(id)
    ship_name = ship.ship_name
    db.session.delete(ship)
    
    audit = AuditLog(user=current_user.name, action="Deleted Ship", target=ship_name)
    db.session.add(audit)
    
    db.session.commit()
    flash("Ship deleted.", "success")
    return redirect(url_for('ships.index'))
