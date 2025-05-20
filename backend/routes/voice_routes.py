from flask import Blueprint, jsonify, request
from models.parking import ParkingLevel, ParkingSpot
from models.sensor import Sensor

voice_bp = Blueprint('voice', __name__)

@voice_bp.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    
    # Extraer la intención del usuario
    intent = data.get('queryResult', {}).get('intent', {}).get('displayName', '')
    
    # Procesar diferentes intenciones
    if intent == 'CheckAvailability':
        return handle_availability_check()
    elif intent == 'FindAccessibleSpot':
        return handle_accessible_spot()
    elif intent == 'ReportIssue':
        return handle_issue_report(data)
    else:
        return jsonify({
            'fulfillmentText': 'Lo siento, no entiendo tu solicitud. ¿Podrías reformularla?'
        })

def handle_availability_check():
    # Obtener disponibilidad general
    levels = ParkingLevel.query.all()
    total_available = sum(level.available_spots for level in levels)
    total_spots = sum(level.total_spots for level in levels)
    
    return jsonify({
        'fulfillmentText': f'Actualmente hay {total_available} espacios disponibles de un total de {total_spots}.'
    })

def handle_accessible_spot():
    # Buscar espacios accesibles disponibles
    accessible_spots = ParkingSpot.query.filter_by(
        is_accessible=True,
        is_occupied=False
    ).all()
    
    if accessible_spots:
        return jsonify({
            'fulfillmentText': f'Hay {len(accessible_spots)} espacios accesibles disponibles.'
        })
    else:
        return jsonify({
            'fulfillmentText': 'Lo siento, no hay espacios accesibles disponibles en este momento.'
        })

def handle_issue_report(data):
    # Extraer información del reporte
    parameters = data.get('queryResult', {}).get('parameters', {})
    issue_type = parameters.get('issue_type', '')
    location = parameters.get('location', '')
    
    # Aquí se podría implementar la lógica para registrar el problema
    return jsonify({
        'fulfillmentText': f'He registrado el problema de {issue_type} en {location}. Un técnico será notificado.'
    }) 