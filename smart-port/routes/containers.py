from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models.container import Container
from models.ship import Ship
from models.audit import AuditLog
from database import db
from utils.decorators import role_required

containers_bp = Blueprint('containers', __name__)

@containers_bp.route('/')
@login_required
@role_required('Port Manager', 'Logistics Officer')
def index():
    search = request.args.get('search', '')
    status_filter = request.args.get('status', '')
    sort_by = request.args.get('sort', 'latest')
    
    query = Container.query
    if search:
        query = query.filter(
            (Container.container_id.ilike(f'%{search}%')) | 
            (Container.destination.ilike(f'%{search}%'))
        )
    if status_filter:
        query = query.filter_by(status=status_filter)
        
    if sort_by == 'latest':
        query = query.order_by(Container.created_at.desc())
    elif sort_by == 'oldest':
        query = query.order_by(Container.created_at.asc())
    elif sort_by == 'status':
        query = query.order_by(Container.status.asc())
        
    containers = query.all()
    ships = Ship.query.all()
    
    return render_template('containers/index.html', containers=containers, ships=ships, search=search, status_filter=status_filter, sort_by=sort_by)

@containers_bp.route('/add', methods=['POST'])
@login_required
@role_required() # Admin only
def add():
    container_id = request.form.get('container_id')
    location = request.form.get('location')
    destination = request.form.get('destination')
    weight = request.form.get('weight', type=float)
    priority = request.form.get('priority', 'Standard')
    ship_id = request.form.get('ship_id')
    
    if not all([container_id, location, destination, weight]):
        flash("All required fields must be provided.", "danger")
    else:
        container = Container(
            container_id=container_id,
            destination=destination,
            priority=priority,
            location=location,
            ship_id=ship_id if ship_id else None
        )
        db.session.add(container)
        
        audit = AuditLog(user=current_user.name, action="Created Container", target=container_id)
        db.session.add(audit)
        
        db.session.commit()
        flash("Container added successfully.", "success")
        
    return redirect(url_for('containers.index'))

@containers_bp.route('/update_status/<int:id>', methods=['POST'])
@login_required
@role_required('Logistics Officer') # Logistics Officer and Admin can update
def update_status(id):
    container = Container.query.get_or_404(id)
    new_status = request.form.get('status')
    
    if new_status:
        old_status = container.status
        container.status = new_status
        audit = AuditLog(user=current_user.name, action=f"Updated Container Status ({old_status} → {new_status})", target=container.container_id)
        db.session.add(audit)
        db.session.commit()
        flash(f"Container status updated to {new_status}.", "success")
        
    return redirect(url_for('containers.index'))

@containers_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
@role_required() # Admin only
def delete(id):
    container = Container.query.get_or_404(id)
    container_id = container.container_id
    db.session.delete(container)
    
    audit = AuditLog(user=current_user.name, action="Deleted Container", target=container_id)
    db.session.add(audit)
    
    db.session.commit()
    flash("Container deleted.", "success")
    return redirect(url_for('containers.index'))
