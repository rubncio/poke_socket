from fastapi import FastAPI, WebSocket, WebSocketDisconnect
class Cliente:
    def __init__(self, nombre, ws:WebSocket):
        self.nombre=nombre
        self.ws=ws
        self.pokemon=str()
    
    