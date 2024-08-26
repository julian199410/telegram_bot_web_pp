from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from starlette.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Configurar CORS si necesitas permitir solicitudes desde otros dominios
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia "*" a tus dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def read_root():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Bot en la Web</title>
    </head>
    <body>
        <h1>Interfaz del Bot</h1>
        
        <!-- Incrustar el widget de Telegram -->
        <script async src="https://telegram.org/js/telegram-widget.js?7"
            data-telegram-login="Comfabot"
            data-size="large"
            data-auth-url="/auth"
            data-request-access="write">
        </script>
        
        <p>Haz clic en el botón de arriba para chatear con nuestro bot en Telegram.</p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get("/auth")
async def auth():
    # Este endpoint puede ser usado para manejar la autenticación de usuarios.
    return HTMLResponse(content="<p>Autenticación completada.</p>")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
