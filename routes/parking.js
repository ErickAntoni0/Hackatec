const express = require('express');
const router = express.Router();
const { ParkingLevel, ParkingSpot } = require('../database/models');

// Get total available spots
router.get('/available', async (req, res) => {
    try {
        const totalAvailable = await ParkingSpot.count({
            where: { isOccupied: false }
        });
        res.json({ totalAvailable });
    } catch (error) {
        res.status(500).json({ error: 'Error al obtener espacios disponibles' });
    }
});

// Get total occupied spots
router.get('/occupied', async (req, res) => {
    try {
        const totalOccupied = await ParkingSpot.count({
            where: { isOccupied: true }
        });
        res.json({ totalOccupied });
    } catch (error) {
        res.status(500).json({ error: 'Error al obtener espacios ocupados' });
    }
});

// Get total accessible spots
router.get('/accessible', async (req, res) => {
    try {
        const totalAccessible = await ParkingSpot.count({
            where: { 
                isAccessible: true,
                isOccupied: false
            }
        });
        res.json({ totalAccessible });
    } catch (error) {
        res.status(500).json({ error: 'Error al obtener espacios accesibles' });
    }
});

// Get level information
router.get('/level/:levelNumber', async (req, res) => {
    try {
        const level = await ParkingLevel.findOne({
            where: { name: `Nivel ${req.params.levelNumber}` },
            include: [{
                model: ParkingSpot,
                attributes: ['isOccupied']
            }]
        });

        if (!level) {
            return res.status(404).json({ error: 'Nivel no encontrado' });
        }

        const availableSpots = level.ParkingSpots.filter(spot => !spot.isOccupied).length;
        
        res.json({
            levelNumber: req.params.levelNumber,
            totalSpots: level.totalSpots,
            availableSpots,
            accessibleSpots: level.accessibleSpots
        });
    } catch (error) {
        res.status(500).json({ error: 'Error al obtener información del nivel' });
    }
});

module.exports = router; 