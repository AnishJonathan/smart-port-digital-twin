from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.ship import Ship
from models.container import Container
from models.crane import Crane
from models.audit import AuditLog
from services.congestion import congestion_engine
from services.weather import weather_service
from datetime import datetime, timedelta
from database import db
from sqlalchemy import func

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def index():
    # Fetch real data
    active_ships = Ship.query.filter(Ship.status.in_(['Arrived', 'Docked', 'Loading', 'Unloading'])).count()
    total_containers = Container.query.count()
    running_cranes = Crane.query.filter_by(status='Active').count()
    
    # Audit Logs for Activity Feed (Admin only in UI)
    recent_activities = []
    if current_user.role == 'Admin':
        recent_activities = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(15).all()
    
    # Get live metrics
    congestion_data = congestion_engine.calculate_congestion()
    weather_data = weather_service.get_weather()
    
    # New Analytics: Average Crane Health
    crane_avg_health = db.session.query(func.avg(Crane.health_score)).scalar() or 0.0
    
    # New Analytics: Delayed Ships
    delayed_ships = Ship.query.filter_by(status='Delayed').count()
    
    # New Analytics: Critical Containers
    critical_containers = Container.query.filter_by(priority='Critical').count()
    
    # Port Efficiency (Mock trend for now based on total containers)
    efficiency_trend = 5.2 if total_containers > 0 else 0.0
    
    stats = {
        'active_ships': active_ships,
        'total_containers': total_containers,
        'running_cranes': running_cranes,
        'congestion_status': congestion_data['level'],
        'weather_condition': weather_data.get('condition', 'Unknown'),
        'crane_avg_health': round(crane_avg_health, 1),
        'delayed_ships': delayed_ships,
        'critical_containers': critical_containers,
        'efficiency_trend': efficiency_trend
    }
    
    # Dummy data for Chart.js
    chart_data = {
        'labels': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        'containers_moved': [300, 450, 400, 600, 550, 350, 420]
    }
    
    return render_template(
        'dashboard/index.html', 
        stats=stats, 
        chart_data=chart_data, 
        user=current_user, 
        alert=congestion_data['alert'], 
        recent_activities=recent_activities, 
        congestion_data=congestion_data, 
        weather_data=weather_data, 
        now=datetime.utcnow()
    )
