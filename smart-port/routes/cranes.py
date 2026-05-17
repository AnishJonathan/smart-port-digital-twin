from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models.crane import Crane
from models.audit import AuditLog
from database import db
from utils.decorators import role_required

cranes_bp = Blueprint('cranes', __name__)

@cranes_bp.route('/')
@login_required
@role_required('Port Manager', 'Logistics Officer')
def index():
    search = request.args.get('search', '')
    status_filter = request.args.get('status', '')
    sort_by = request.args.get('sort', 'latest')
    
    query = Crane.query
    if search:
        query = query.filter(Crane.crane_name.ilike(f'%{search}%'))
    if status_filter:
        query = query.filter_by(status=status_filter)
        
    if sort_by == 'latest':
        query = query.order_by(Crane.id.desc())
    elif sort_by == 'oldest':
        query = query.order_by(Crane.id.asc())
    elif sort_by == 'health':
        query = query.order_by(Crane.health_percentage.asc())
        
    cranes = query.all()
    
    return render_template('cranes/index.html', cranes=cranes, search=search, status_filter=status_filter, sort_by=sort_by)

@cranes_bp.route('/add', methods=['POST'])
@login_required
# Only Admins can add/delete Cranes (per requirements, managers monitor only)
# The decorator implicitly allows Admin, so we don't pass anything to restrict to admin only.
@role_required() 
def add():
    crane_name = request.form.get('crane_name')
    status = request.form.get('status', 'Idle')
    if crane_name:
        crane = Crane(crane_name=crane_name, status=status)
        db.session.add(crane)
        
        audit = AuditLog(user=current_user.name, action="Registered Crane", target=crane_name)
        db.session.add(audit)
        
        db.session.commit()
        flash("Crane registered successfully.", "success")
    return redirect(url_for('cranes.index'))

@cranes_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
@role_required() # Admin only
def delete(id):
    crane = Crane.query.get_or_404(id)
    crane_name = crane.crane_name
    db.session.delete(crane)
    
    audit = AuditLog(user=current_user.name, action="Deleted Crane", target=crane_name)
    db.session.add(audit)
    
    db.session.commit()
    flash("Crane deleted.", "success")
    return redirect(url_for('cranes.index'))
