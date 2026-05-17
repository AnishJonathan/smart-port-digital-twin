from flask import Blueprint, render_template
from flask_login import login_required, current_user

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def index():
    # Dummy data for dashboard statistics
    stats = {
        'active_ships': 12,
        'total_containers': 4520,
        'running_cranes': 8,
        'congestion_status': 'Moderate'
    }
    
    # Dummy data for Chart.js
    chart_data = {
        'labels': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        'containers_moved': [300, 450, 400, 600, 550, 350, 420]
    }
    
    return render_template('dashboard/index.html', stats=stats, chart_data=chart_data, user=current_user)
