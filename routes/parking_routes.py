from flask import Blueprint, jsonify, request
from models.parking import ParkingLevel, ParkingSpot
from app import db

parking_bp = Blueprint('parking', __name__)

@parking_bp.route('/levels', methods=['GET'])
def get_levels():
    levels = ParkingLevel.query.all()
    return jsonify([level.to_dict() for level in levels])

@parking_bp.route('/levels/<int:level_id>', methods=['GET'])
def get_level(level_id):
    level = ParkingLevel.query.get_or_404(level_id)
    return jsonify(level.to_dict())

@parking_bp.route('/spots', methods=['GET'])
def get_spots():
    level_id = request.args.get('level_id', type=int)
    query = ParkingSpot.query
    
    if level_id:
        query = query.filter_by(level_id=level_id)
    
    spots = query.all()
    return jsonify([spot.to_dict() for spot in spots])

@parking_bp.route('/spots/<int:spot_id>', methods=['GET'])
def get_spot(spot_id):
    spot = ParkingSpot.query.get_or_404(spot_id)
    return jsonify(spot.to_dict())

@parking_bp.route('/spots/<int:spot_id>/status', methods=['PUT'])
def update_spot_status(spot_id):
    spot = ParkingSpot.query.get_or_404(spot_id)
    data = request.get_json()
    
    if 'is_occupied' in data:
        spot.is_occupied = data['is_occupied']
        # Actualizar contadores del nivel
        level = spot.level
        if data['is_occupied']:
            level.available_spots -= 1
        else:
            level.available_spots += 1
    
    db.session.commit()
    return jsonify(spot.to_dict()) 