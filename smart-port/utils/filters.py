from datetime import datetime, timezone
import math

def time_ago(dt):
    if not dt:
        return "Unknown"
        
    # Ensure both datetimes are offset-naive for calculation, since db returns naive datetime in UTC
    now = datetime.utcnow()
    diff = now - dt
    
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return "just now"
    
    minutes = math.floor(seconds / 60)
    if minutes < 60:
        return f"{minutes} min{'s' if minutes > 1 else ''} ago"
        
    hours = math.floor(minutes / 60)
    if hours < 24:
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
        
    days = math.floor(hours / 24)
    if days < 30:
        return f"{days} day{'s' if days > 1 else ''} ago"
        
    months = math.floor(days / 30)
    if months < 12:
        return f"{months} month{'s' if months > 1 else ''} ago"
        
    years = math.floor(days / 365)
    return f"{years} year{'s' if years > 1 else ''} ago"
