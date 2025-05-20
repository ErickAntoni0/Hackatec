# Hackatec
SmartParking

# Sistema de Estacionamiento Inteligente

Proyecto para el Hackathon Tec, implementando un sistema inteligente de estacionamiento con frontend (dashboard web) y backend (API en Node.js).

## 🚀 Características Principales

- Dashboard web interactivo para monitoreo del estacionamiento.
- Asistente de voz integrado en el dashboard.
- Backend RESTful para gestión de datos.
- Monitoreo de niveles, espacios y sensores.
- Sistema de usuarios y autenticación.
- Base de datos SQLite.

## 🗣️ Implementación del Asistente de Voz

Se integró un asistente de voz en el dashboard para permitir a los usuarios consultar el estado del estacionamiento mediante comandos de voz o texto. Los cambios clave incluyen:

- **Frontend (`src/daashboard/`)**:

  - Creación de un componente reutilizable (`widget-assistant.html`, `widget-assistant.css`) para el widget del asistente.
  - Implementación de la lógica del asistente de voz (`voice-assistant.js`) utilizando la Web Speech API para reconocimiento de voz y síntesis de voz.
  - Conexión del asistente a las rutas API del backend para obtener datos en tiempo real.
  - Configuración del widget para que inicie minimizado en todas las páginas del dashboard y se maximice al hacer clic.

- **Backend (`src/backend-node/`)**:
  - Adición de rutas API en `src/routes/parkingSpotRoutes.js` para exponer datos agregados del estacionamiento:
    - `GET /api/spots/available`: Total de espacios disponibles.
    - `GET /api/spots/occupied`: Total de espacios ocupados.
    - `GET /api/spots/accessible`: Total de espacios accesibles disponibles.
    - `GET /api/spots/level/:levelNumber`: Información detallada (total y disponibles) para un nivel específico (buscado por nombre como "Nivel 1").
  - Configuración del archivo principal (`src/app.js`) para servir los archivos estáticos del dashboard desde el mismo origen que la API (`http://localhost:5001/`).
  - Corrección en la importación de modelos Sequelize y en la lógica de búsqueda por nombre de nivel para asegurar la comunicación correcta con la base de datos.

## ⚙️ Configuración e Inicio

1.  **Clonar el repositorio** (si aún no lo has hecho).
2.  **Navegar al directorio del backend**:
    ```bash
    cd src/backend-node
    ```
3.  **Instalar dependencias**:
    ```bash
    npm install
    ```
4.  **Configurar variables de entorno**:
    ```bash
    cp .env.example .env
    ```
    Editar el archivo `.env` si es necesario (la configuración por defecto usa SQLite).
5.  **Inicializar la base de datos (si es la primera vez o si quieres resetearla)**:
    ```bash
    npm run seed
    ```
6.  **Iniciar el servidor backend (servirá la API y el dashboard)**:
    ```bash
    npm start
    ```
    El servidor iniciará en `http://localhost:5001`.
7.  **Acceder al Dashboard**:
    Abre tu navegador y ve a `http://localhost:5001/main.html` (o el nombre del archivo HTML principal de tu dashboard).

## 📋 Rutas API Actualizadas (en `/api/spots`)

- `GET /api/spots/available` - Total de espacios disponibles.
- `GET /api/spots/occupied` - Total de espacios ocupados.
- `GET /api/spots/accessible` - Total de espacios accesibles disponibles.
- `GET /api/spots/level/:levelNumber` - Información por nivel (reemplaza `:levelNumber` con el número del nivel, ej. `/api/spots/level/1`).
- (Las rutas CRUD existentes `/api/spots/`, `/:id`, etc., se mantienen).

## 🤝 Contribución y Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE.md](LICENSE.md) para más detalles.

## ✨ Agradecimientos

- Equipo de desarrollo
- Mentores del Hackathon
- Contribuidores
