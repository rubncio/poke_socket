import asyncio
import random
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.websockets import WebSocketState
from cliente import Cliente
class Clientes:
    def __init__(self):
        self.lista_pokemons=["pokemon","charizard","bulbasur","squirtel","charmander"]
        self.listclientes=list[Cliente]()
        self.numeroClientes=0
        self.sala_espera=asyncio.Event()

    async def conexion_viva(self, ws:WebSocket)->bool:
        #en caso de que esetado este conectado aun asi se comprueba porque no siempre representa cuando se cierra la conexion.
        vivo_bool=True
        if ws.client_state != WebSocketState.CONNECTED:
            vivo_bool=False
        else:
            try:
                await ws.send_text("ping")
            except (RuntimeError, WebSocketDisconnect):
                vivo_bool=False
        return vivo_bool

    async def ver_numeroClientes(self):
        lista_a_borrar=list()
        print(f"comprobando vivos {len(self.listclientes)}")
        for cliente in self.listclientes:
            print(f"comprobando {cliente.nombre}:")
            if not await self.conexion_viva(cliente.ws):
                print(f"no esta vivo")
                lista_a_borrar.append(cliente)
        for cliente_a_borrar in lista_a_borrar:
            self.listclientes.remove(cliente_a_borrar)
        self.numeroClientes=len(self.listclientes)
        return self.numeroClientes
            


    def añadir(self, cliente:Cliente)->bool:
        if self.numeroClientes<2:
            self.numeroClientes+=1
            cliente.pokemon=random.choice(self.lista_pokemons)
            self.listclientes.append(cliente)
            return True
        else:
            return False
        
    def eliminar(self, ws:WebSocket):
        indice_eliminar=[cliente.ws for cliente in self.listclientes].index(ws)
        self.listclientes.pop(indice_eliminar)
        self.numeroClientes-=1
        print("Desconectando cliente")

    def clientes_completo(self)->bool:
        return self.numeroClientes==2
    
    async def esperar_clientes(self):
        """done, pending=await asyncio.wait(
            [asyncio.create_task()]
        )"""
        print("cliente se pone a la espera")
        
        await self.sala_espera.wait()
        print("cliente se despierta")

    """async def enviar_todos(self, text):
        for cliente in self.listclientes:
            await cliente.ws.send_text(text)"""

    async def elegir_pokemon(self, pokemon1, pokemon2):
        for cliente in self.listclientes:
            cliente.pokemon=random.choice([pokemon1, pokemon2])
            await cliente.ws.send_text(f"enhorabuena {cliente.nombre} te ha tocado el pokemon {cliente.pokemon.nombre}")