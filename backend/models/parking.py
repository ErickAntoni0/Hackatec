from app import db
from datetime import datetime

class ParkingLevel(db.Model):
    __tablename__ = 'parking_levels'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    total_spots = db.Column(db.Integer, nullable=False)
    available_spots = db.Column(db.Integer, nullable=False)
    accessible_spots = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relación con los espacios de estacionamiento
    spots = db.relationship('ParkingSpot', backref='level', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'total_spots': self.total_spots,
            'available_spots': self.available_spots,
            'accessible_spots': self.accessible_spots,
            'occupation_percentage': round((self.total_spots - self.available_spots) / self.total_spots * 100, 2)
        }

class ParkingSpot(db.Model):
    __tablename__ = 'parking_spots'
    
    id = db.Column(db.Integer, primary_key=True)
    spot_number = db.Column(db.String(10), nullable=False)
    level_id = db.Column(db.Integer, db.ForeignKey('parking_levels.id'), nullable=False)
    is_occupied = db.Column(db.Boolean, default=False)
    is_accessible = db.Column(db.Boolean, default=False)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensors.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'spot_number': self.spot_number,
            'level_id': self.level_id,
            'is_occupied': self.is_occupied,
            'is_accessible': self.is_accessible,
            'sensor_id': self.sensor_id
        } 