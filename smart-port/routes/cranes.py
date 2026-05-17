from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from models.crane import Crane
from database import db
from utils.decorators import role_required

cranes_bp = Blueprint('cranes', __name__)

@cranes_bp.route('/')
@login_required
@role_required('Port Manager', 'Logistics Officer')
def index():
    cranes = Crane.query.all()
    return render_template('cranes/index.html', cranes=cranes)

@cranes_bp.route('/add', methods=['POST'])
@login_required
# Only Admins can add/delete Cranes (per requirements, managers monitor only)
# The decorator implicitly allows Admin, so we don't pass anything to restrict to admin only.
@role_required() 
def add():
    crane_name = request.form.get('crane_name')
    if crane_name:
        crane = Crane(crane_name=crane_name)
        db.session.add(crane)
        db.session.commit()
        flash("Crane registered.", "success")
    return redirect(url_for('cranes.index'))
