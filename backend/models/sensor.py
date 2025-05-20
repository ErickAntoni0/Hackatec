from app import db
from datetime import datetime

class Sensor(db.Model):
    __tablename__ = 'sensors'
    
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.String(50), unique=True, nullable=False)
    status = db.Column(db.String(20), default='active')  # active, inactive, maintenance
    last_reading = db.Column(db.Boolean, default=False)
    last_reading_time = db.Column(db.DateTime)
    battery_level = db.Column(db.Float, default=100.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relación con el espacio de estacionamiento
    parking_spot = db.relationship('ParkingSpot', backref='sensor', uselist=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'sensor_id': self.sensor_id,
            'status': self.status,
            'last_reading': self.last_reading,
            'last_reading_time': self.last_reading_time.isoformat() if self.last_reading_time else None,
            'battery_level': self.battery_level
        }
    
    def update_reading(self, is_occupied):
        self.last_reading = is_occupied
        self.last_reading_time = datetime.utcnow()
        if self.parking_spot:
            self.parking_spot.is_occupied = is_occupied 