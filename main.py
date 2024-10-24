from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from fastapi.responses import RedirectResponse, JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

load_dotenv()

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

# Manejador de error 404 personalizado
@app.exception_handler(StarletteHTTPException)
async def custom_404_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return templates.TemplateResponse(
            "404.html", {"request": request, "message": "Página no encontrada"}, status_code=404
        )
    return JSONResponse(
        status_code=exc.status_code, content={"detail": exc.detail}
    )

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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
