from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()
    
@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    await ws.send_text("Conectado. Introduce tu nombre.")
    while True:
        name = await ws.receive_text()
        print(f"Jugador conectado: {name}")
        await ws.send_text(f"Nombre recibido: {name}")
