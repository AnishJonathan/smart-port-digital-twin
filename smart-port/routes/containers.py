from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models.container import Container
from database import db
from utils.decorators import role_required

containers_bp = Blueprint('containers', __name__)

@containers_bp.route('/')
@login_required
@role_required('Port Manager', 'Logistics Officer')
def index():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = Container.query
    if search:
        query = query.filter(Container.container_id.ilike(f'%{search}%'))
        
    pagination = query.order_by(Container.created_at.desc()).paginate(page=page, per_page=10, error_out=False)
    
    return render_template('containers/index.html', containers=pagination.items, pagination=pagination, search=search)

@containers_bp.route('/add', methods=['POST'])
@login_required
@role_required('Logistics Officer')
def add():
    container_id = request.form.get('container_id')
    location = request.form.get('location')
    destination = request.form.get('destination')
    weight = request.form.get('weight', type=float)
    priority = request.form.get('priority', 'Standard')
    
    if not all([container_id, location, destination, weight]):
        flash("All required fields must be provided.", "danger")
    else:
        container = Container(
            container_id=container_id,
            location=location,
            destination=destination,
            weight=weight,
            priority=priority
        )
        db.session.add(container)
        db.session.commit()
        flash("Container registered.", "success")
        
    return redirect(url_for('containers.index'))

@containers_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
@role_required('Logistics Officer')
def delete(id):
    container = Container.query.get_or_404(id)
    db.session.delete(container)
    db.session.commit()
    flash("Container deleted.", "success")
    return redirect(url_for('containers.index'))
