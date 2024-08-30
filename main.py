from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
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

# Montar carpeta estática para servir CSS y otros archivos
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_root():
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pediculosis y Parasitismo</title>
    <link rel="stylesheet" href="/static/css/styles.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/slick-carousel/1.8.1/slick.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/slick-carousel/1.8.1/slick-theme.min.css">
</head>
<body>
    <div class="dashboard">
        <header>
            <div class="logo-container">
                <img src="/static/images/logo.png" alt="Logo de la página" class="logo">
                <h1>Pediculosis y Parasitismo</h1>
            </div>
        </header>

        <div class="content">
            <section class="info">
                <h2>Bienvenido a nuestro sistema</h2>
                <p>Consulta información sobre pediculosis y parasitismo.</p>
            </section>
            
            <!-- Sliders -->
            <section class="sliders">
                <h2>Galería de Imágenes</h2>
                <div class="slider">
                    <div><img src="/static/images/pediculosis1.jpg" alt="Pediculosis 1"></div>
                    <div><img src="/static/images/pediculosis2.jpg" alt="Pediculosis 2"></div>
                    <div><img src="/static/images/parasitismo1.jpg" alt="Parasitismo 1"></div>
                    <div><img src="/static/images/parasitismo2.jpg" alt="Parasitismo 2"></div>
                </div>
            </section>
        </div>

        <!-- Pie de página -->
        <footer>
            <p>&copy; 2024 Pediculosis y Parasitismo. Todos los derechos reservados.</p>
        </footer>

        <!-- Widget de Telegram en la parte inferior derecha -->
        <div class="widget-telegram">
            <script async src="https://telegram.org/js/telegram-widget.js?22"
                data-telegram-login="Comfabot"
                data-size="large"
                data-auth-url="/https://telegram-bot-web-pp.onrender.com/auth"
                data-request-access="write">
            </script>
            <script type="text/javascript">
                function onTelegramAuth(user) {
                    alert('Logged in as ' + user.first_name + ' ' + user.last_name + ' (' + user.id + (user.username ? ', @' + user.username : '') + ')');
                }
            </script>
        </div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/slick-carousel/1.8.1/slick.min.js"></script>
    <script>
        $(document).ready(function(){
            $('.slider').slick({
                dots: true,
                infinite: true,
                speed: 500,
                slidesToShow: 1,
                slidesToScroll: 1
            });
        });
    </script>
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

    uvicorn.run(app, host="0.0.0.0", port=8000)
