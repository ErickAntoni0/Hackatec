from flask import Blueprint, jsonify, request
from models.sensor import Sensor
from app import db

sensor_bp = Blueprint('sensors', __name__)

@sensor_bp.route('/', methods=['GET'])
def get_sensors():
    sensors = Sensor.query.all()
    return jsonify([sensor.to_dict() for sensor in sensors])

@sensor_bp.route('/<int:sensor_id>', methods=['GET'])
def get_sensor(sensor_id):
    sensor = Sensor.query.get_or_404(sensor_id)
    return jsonify(sensor.to_dict())

@sensor_bp.route('/<int:sensor_id>/reading', methods=['POST'])
def update_sensor_reading(sensor_id):
    sensor = Sensor.query.get_or_404(sensor_id)
    data = request.get_json()
    
    if 'is_occupied' not in data:
        return jsonify({'error': 'is_occupied is required'}), 400
    
    sensor.update_reading(data['is_occupied'])
    db.session.commit()
    
    return jsonify(sensor.to_dict())

@sensor_bp.route('/<int:sensor_id>/status', methods=['PUT'])
def update_sensor_status(sensor_id):
    sensor = Sensor.query.get_or_404(sensor_id)
    data = request.get_json()
    
    if 'status' in data:
        sensor.status = data['status']
    
    if 'battery_level' in data:
        sensor.battery_level = data['battery_level']
    
    db.session.commit()
    return jsonify(sensor.to_dict()) 