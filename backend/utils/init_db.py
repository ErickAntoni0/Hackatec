import sys
import os

# Agregar el directorio padre al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from models.parking import ParkingLevel, ParkingSpot
from models.sensor import Sensor
from models.user import User

def init_db():
    with app.app_context():
        # Crear tablas
        db.create_all()
        
        # Crear niveles de estacionamiento
        levels = [
            ParkingLevel(name='Nivel 1', total_spots=20, available_spots=15, accessible_spots=3),
            ParkingLevel(name='Nivel 2', total_spots=20, available_spots=18, accessible_spots=2),
            ParkingLevel(name='Nivel 3', total_spots=20, available_spots=20, accessible_spots=4)
        ]
        
        for level in levels:
            db.session.add(level)
        
        db.session.commit()
        
        # Crear espacios de estacionamiento
        for level in levels:
            for i in range(1, 21):
                spot = ParkingSpot(
                    spot_number=f'{level.name[0]}{i}',
                    level_id=level.id,
                    is_accessible=(i % 5 == 0)  # Cada quinto espacio es accesible
                )
                db.session.add(spot)
        
        db.session.commit()
        
        # Crear sensores
        spots = ParkingSpot.query.all()
        for spot in spots:
            sensor = Sensor(
                sensor_id=f'SENSOR-{spot.spot_number}',
                status='active',
                last_reading=False
            )
            db.session.add(sensor)
            spot.sensor = sensor
        
        db.session.commit()
        
        # Crear usuario administrador
        admin = User(
            username='admin',
            email='admin@example.com',
            role='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        db.session.commit()

if __name__ == '__main__':
    init_db()
    print("Base de datos inicializada con datos de prueba.") 