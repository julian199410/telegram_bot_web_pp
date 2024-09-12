# Telegram Bot Integration with FastAPI

Este proyecto integra un bot de Telegram en una página web utilizando FastAPI.

## Estructura del Proyecto

- `main.py`: Configuración y ejecución de la aplicación FastAPI.
- `templates/index.html`: Interfaz web con el widget de Telegram.
- `static/`: Archivos estáticos opcionales.
- `.env`: Variables de entorno.
- `requirements.txt`: Dependencias del proyecto.

## Ejecutar el Proyecto

1. Instala las dependencias:
   ```bash
   pip install -r requirements.txt

# Create environment
   python -m venv venv 
# Activate environment
   venv\Scripts\activate

# Run Project
   uvicorn main:app --reload
   uvicorn main:app --reload --port 7000

# Para correr con serveo
   - ssh -R 80:localhost:5000 serveo.net