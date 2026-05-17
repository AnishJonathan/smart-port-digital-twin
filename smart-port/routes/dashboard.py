from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.ship import Ship
from models.container import Container
from models.crane import Crane
from services.congestion import congestion_engine

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def index():
    # Fetch real data
    active_ships = Ship.query.filter(Ship.status.in_(['Docked', 'Arriving'])).count()
    total_containers = Container.query.count()
    running_cranes = Crane.query.filter_by(status='Active').count()
    
    congestion_data = congestion_engine.calculate_congestion()
    
    stats = {
        'active_ships': active_ships,
        'total_containers': total_containers,
        'running_cranes': running_cranes,
        'congestion_status': congestion_data['level'],
        'weather_condition': congestion_data['weather']['condition']
    }
    
    # Dummy data for Chart.js (could be made dynamic later)
    chart_data = {
        'labels': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        'containers_moved': [300, 450, 400, 600, 550, 350, 420]
    }
    
    return render_template('dashboard/index.html', stats=stats, chart_data=chart_data, user=current_user, alert=congestion_data['alert'])
