const { sequelize, ParkingLevel, ParkingSpot, Sensor, User } = require('../models');

const seedDatabase = async () => {
  try {
    // Sincronizar base de datos
    await sequelize.sync({ force: true });
    console.log('Base de datos sincronizada');

    // Crear niveles de estacionamiento
    const levels = await Promise.all([
      ParkingLevel.create({
        name: 'Nivel 1',
        totalSpots: 20,
        availableSpots: 15,
        accessibleSpots: 3
      }),
      ParkingLevel.create({
        name: 'Nivel 2',
        totalSpots: 20,
        availableSpots: 18,
        accessibleSpots: 2
      }),
      ParkingLevel.create({
        name: 'Nivel 3',
        totalSpots: 20,
        availableSpots: 20,
        accessibleSpots: 4
      })
    ]);
    console.log('Niveles creados');

    // Crear espacios de estacionamiento
    for (const level of levels) {
      for (let i = 1; i <= 20; i++) {
        const isAccessible = i % 5 === 0;
        // Asegurar spotNumber único
        const spotNumber = `${level.name.replace(/\s/g, '')}_${i}`;
        await ParkingSpot.create({
          spotNumber,
          levelId: level.id,
          isOccupied: Math.random() > 0.7,
          isAccessible
        });
      }
    }
    console.log('Espacios creados');

    // Crear sensores
    const spots = await ParkingSpot.findAll();
    for (const spot of spots) {
      await Sensor.create({
        sensorId: `SENSOR-${spot.spotNumber}-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
        status: 'active',
        lastReading: spot.isOccupied,
        batteryLevel: Math.floor(Math.random() * 100),
        spotId: spot.id
      });
    }
    console.log('Sensores creados');

    // Crear usuarios de prueba
    await User.create({
      username: 'admin',
      email: 'admin@example.com',
      password: 'admin123',
      role: 'admin'
    });

    await User.create({
      username: 'staff',
      email: 'staff@example.com',
      password: 'staff123',
      role: 'staff'
    });

    await User.create({
      username: 'user',
      email: 'user@example.com',
      password: 'user123',
      role: 'user'
    });
    console.log('Usuarios creados');

    console.log('Base de datos inicializada con éxito');
    process.exit(0);
  } catch (error) {
    console.error('Error al inicializar la base de datos:', error);
    process.exit(1);
  }
};

seedDatabase(); 