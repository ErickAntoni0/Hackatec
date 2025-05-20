from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# Configuración de la aplicación
app = Flask(__name__)
CORS(app)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database/parking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Importar modelos
from models.parking import ParkingSpot, ParkingLevel
from models.sensor import Sensor
from models.user import User

# Importar rutas
from routes.parking_routes import parking_bp
from routes.sensor_routes import sensor_bp
from routes.voice_routes import voice_bp

# Registrar blueprints
app.register_blueprint(parking_bp, url_prefix='/api/parking')
app.register_blueprint(sensor_bp, url_prefix='/api/sensors')
app.register_blueprint(voice_bp, url_prefix='/api/voice')

@app.route('/')
def index():
    return jsonify({
        'status': 'success',
        'message': 'API de Sistema de Estacionamiento Inteligente',
        'version': '1.0.0'
    })

if __name__ == '__main__':
    # Crear tablas si no existen
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000) 