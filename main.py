from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde .env
load_dotenv()

# Variables de configuración de correo
MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.example.com")
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM")
MAIL_TLS = os.getenv("MAIL_TLS", "True").lower() == "true"
MAIL_SSL = os.getenv("MAIL_SSL", "False").lower() == "true"

# Validar que las variables críticas estén configuradas
if not all([MAIL_USERNAME, MAIL_PASSWORD, MAIL_FROM]):
    raise ValueError("Faltan variables de entorno para la configuración del correo")

# Configuración de FastAPI-Mail
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
    MAIL_SERVER=os.getenv("MAIL_SERVER", "smtp.example.com"),
    MAIL_STARTTLS=os.getenv("MAIL_STARTTLS", "True").lower() == "true",
    MAIL_SSL_TLS=os.getenv("MAIL_SSL_TLS", "False").lower() == "true",
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,  # Verifica los certificados SSL/TLS
)

# Inicializar la instancia de FastAPI
app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar carpeta estática para servir CSS y otros archivos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configurar Jinja2Templates
templates = Jinja2Templates(directory="templates")


# Modelo para recibir datos del formulario de contacto
@app.post("/enviar-correo")
async def enviar_correo(
    name: str = Form(...), email: EmailStr = Form(...), message: str = Form(...)
):
    # Crear mensaje de correo
    mensaje = MessageSchema(
        subject=f"Nuevo mensaje de {name}",
        recipients=[
            "julianobando@unicomfacauca.edu.co"
        ],  # Cambiar por el correo del receptor
        body=f"""
        Has recibido un nuevo mensaje:

        Nombre: {name}
        Correo: {email}
        Mensaje: {message}
        """,
        subtype="plain",
    )

    # Enviar correo
    fm = FastMail(conf)
    try:
        await fm.send_message(mensaje)
        return {"message": "Correo enviado exitosamente"}
    except Exception as e:
        return {"error": f"No se pudo enviar el correo: {str(e)}"}


# Manejador de error 404 personalizado
@app.exception_handler(StarletteHTTPException)
async def custom_404_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return templates.TemplateResponse(
            "404.html",
            {"request": request, "message": "Página no encontrada"},
            status_code=404,
        )
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


# Rutas para diferentes páginas
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/pediculosis", response_class=HTMLResponse)
async def pediculosis_page(request: Request):
    return templates.TemplateResponse("pediculosis.html", {"request": request})


@app.get("/parasitismo", response_class=HTMLResponse)
async def parasitismo_page(request: Request):
    return templates.TemplateResponse("parasitismo.html", {"request": request})


@app.get("/blog", response_class=HTMLResponse)
async def blog_page(request: Request):
    return templates.TemplateResponse("blog.html", {"request": request})


@app.get("/galeria", response_class=HTMLResponse)
async def galeria_page(request: Request):
    return templates.TemplateResponse("galeria.html", {"request": request})


@app.get("/recursos", response_class=HTMLResponse)
async def guia_recursos_page(request: Request):
    return templates.TemplateResponse("guia_recursos.html", {"request": request})


@app.get("/foro", response_class=HTMLResponse)
async def foro_page(request: Request):
    return templates.TemplateResponse("foro_comunidad.html", {"request": request})


@app.get("/contacto", response_class=HTMLResponse)
async def contacto_page(request: Request):
    return templates.TemplateResponse("contacto.html", {"request": request})


@app.get("/quiensomos", response_class=HTMLResponse)
async def quiensomos_page(request: Request):
    return templates.TemplateResponse("quiensomos.html", {"request": request})


@app.get("/auth")
async def auth(request: Request):
    query_params = request.query_params
    if "hash" not in query_params:
        raise HTTPException(status_code=400, detail="Missing hash parameter")

    # Si la autenticación es correcta, redirige al chat de Telegram
    bot_username = "Comfabot"  # Reemplaza con el nombre de tu bot
    telegram_url = f"https://t.me/{bot_username}"
    return RedirectResponse(url=telegram_url)


# Ejecutar el servidor con Uvicorn
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
