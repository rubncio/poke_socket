from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from cliente import Cliente
class Clientes:
    def __init__(self):
        
        self.listclientes=list()
        self.numeroClientes=0
    def añadir(self,nombre, ws:WebSocket)->bool:
        if self.numeroClientes<2:
            self.numeroClientes+=1
            
            self.listclientes.append(Cliente(nombre, ws))
            return True
        else:
            return False
        
    def eliminar(self, ws:WebSocket):
        self.listclientes.remove(ws)

    def clientes_completo(self)->bool:
        return self.numeroClientes==2
    
    def esperar_clientes(self):
        
        while(not self.clientes_completo):
            pass