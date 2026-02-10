from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from clientes import Clientes

app = FastAPI()
clientes=Clientes()

@app.get("/", response_class=HTMLResponse)
def index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()
    
@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    #ws=conexiones con el cliente
    
    await ws.accept()
     
    await ws.send_text(f"jugadores en linea:{clientes.numeroClientes}/2")
    await ws.send_text("Introduce tu nombre.")
    name = await ws.receive_text()
    try: 
        if not clientes.clientes_completo():
            clientes.añadir(name, ws)
            print(f"Jugador conectado: {name}")
            await ws.send_text(f"Te has conectado: {name}")

            #Esperando dos jugadores
            if not clientes.clientes_completo():
                await ws.send_text("esperando otro jugador....")
                clientes.esperar_clientes()
            await ws.send_text(f"jugadores: {clientes.listclientes[0].nombre} VS {clientes.listclientes[1].nombre}")

            while True:
                pass
            
        else:
            await ws.send_text("ya hay suficientes jugadores.")
    except WebSocketDisconnect:
        clientes.eliminar(ws)
        
    
    
