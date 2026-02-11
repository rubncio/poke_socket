from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from clientes import Clientes
from cliente import Cliente

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
            cliente=Cliente(name, ws)
            clientes.añadir(cliente)
            print(f"Jugador conectado: {name}")
            await ws.send_text(f"Te has conectado: {name}")
    
            #Esperando dos jugadores
            if not clientes.clientes_completo():
                await ws.send_text("esperando otro jugador....")
                await clientes.esperar_clientes()
                await ws.send_text("2º jugador conectado")
            else:
                clientes.sala_espera.set()
            
            if clientes.clientes_completo():
                await ws.send_text(f"jugadores: {clientes.listclientes[0].nombre} VS {clientes.listclientes[1].nombre}")
                #await ws.send_text(f"jugadores: {clientes.listclientes[0].nombre} VS {clientes.listclientes[1].nombre}")
                await ws.send_text(f"enhorabuena {cliente.nombre} tu pokemon sera {cliente.pokemon}")
            """
            elegir_pokemon(pokemon1, pokemon2)
            while True:
                await ws.receive_text()"""
            
            
        else:
            await ws.send_text("ya hay suficientes jugadores.")
    except WebSocketDisconnect:
        clientes.eliminar(ws)
        
    
    
