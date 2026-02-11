import asyncio
import random
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from cliente import Cliente
class Clientes:
    def __init__(self):
        self.lista_pokemons=["pokemon","charizard","bulbasur","squirtel","charmander"]
        self.listclientes=list[Cliente]()
        self.numeroClientes=0
        self.sala_espera=asyncio.Event()
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