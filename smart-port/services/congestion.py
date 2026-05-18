from models.ship import Ship
from models.container import Container
from models.crane import Crane
from services.weather import weather_service

class CongestionEngine:
    def calculate_congestion(self):
        """
        Calculates the port congestion level based on:
        - Number of arriving/docked ships
        - Delayed containers
        - Crane availability
        - Weather risk
        """
        weather_data = weather_service.get_weather()
        
        # Base scores
        congestion_score = 0
        
        # 1. Ship Factor
        active_ships = Ship.query.filter(Ship.status.in_(['Arriving', 'Docked'])).count()
        if active_ships > 10:
            congestion_score += 30
        elif active_ships > 5:
            congestion_score += 15
            
        # 2. Container Factor
        delayed_containers = Container.query.filter_by(status='Delayed').count()
        if delayed_containers > 50:
            congestion_score += 30
        elif delayed_containers > 20:
            congestion_score += 10
            
        # 3. Crane Factor
        faulty_cranes = Crane.query.filter_by(status='Fault').count()
        if faulty_cranes > 2:
            congestion_score += 20
        elif faulty_cranes > 0:
            congestion_score += 10
            
        # 4. Weather Factor
        wind_speed = weather_data.get('wind_speed', 0)
        condition = weather_data.get('condition', '')
        
        if wind_speed > 20.0 or condition == 'Thunderstorm':
            congestion_score += 40
        elif wind_speed > 15.0 or condition == 'Rain':
            congestion_score += 15
            
        # Determine Level
        if congestion_score >= 80:
            level = 'Critical'
            alert = "Critical congestion: Halt incoming vessels."
        elif congestion_score >= 50:
            level = 'High'
            alert = "Heavy congestion expected due to operations or weather."
        elif congestion_score >= 20:
            level = 'Medium'
            alert = "Moderate congestion."
        else:
            level = 'Low'
            alert = "Operations normal."
            
        return {
            'score': congestion_score,
            'level': level,
            'alert': alert,
            'weather': weather_data
        }

congestion_engine = CongestionEngine()
