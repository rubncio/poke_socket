from fastapi import FastAPI

app=FastAPI()
@app.websocket("/ws")
async def raiz(name):
    print(name)
