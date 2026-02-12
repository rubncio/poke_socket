import random
import time
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from pokemon import Pokemon, Ataque, Defensa


app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()
    
@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    #ws=conexiones con el cliente
    
    await ws.accept()
     
    await ws.send_text("Introduzca su nombre y haga click en empezar.")
    
    try: 
        name = await ws.receive_text()
        await ws.send_text(f"bienvenido {name}")
        await ws.send_text("Empezando combate")
        
        #Creando pokemons
        #ataques
        impactrueno = Ataque("Impactrueno", 20)
        rayo = Ataque("Rayo", 35)
        lanzallamas = Ataque("Lanzallamas", 40)
        ascuas = Ataque("Ascuas", 15)
        pistola_agua = Ataque("Pistola Agua", 25)
        hidrobomba = Ataque("Hidrobomba", 45)
        latigo_cepa = Ataque("Látigo Cepa", 20)
        hoja_afilada = Ataque("Hoja Afilada", 30)
        
        #defensas
        escudo_electrico = Defensa("Escudo Eléctrico", 15)
        muro_fuego = Defensa("Muro de Fuego", 20)
        burbuja_protectora = Defensa("Burbuja Protectora", 18)
        barrera_hojas = Defensa("Barrera de Hojas", 22)
        defensa_rapida = Defensa("Defensa Rápida", 10)

        #pokemons
        pikachu = Pokemon(
        "Pikachu",
        100,
        [impactrueno, rayo],
        [escudo_electrico, defensa_rapida]
        )

        charmander = Pokemon(
        "Charmander",
        110,
        [ascuas, lanzallamas],
        [muro_fuego]
        )

        squirtle = Pokemon(
        "Squirtle",
        120,
        [pistola_agua, hidrobomba],
        [burbuja_protectora]
        )

        bulbasaur = Pokemon(
        "Bulbasaur",
        115,
        [latigo_cepa, hoja_afilada],
        [barrera_hojas]
        )

        raichu = Pokemon(
        "Raichu",
        105,
        [impactrueno, rayo],
        [escudo_electrico]
        )

        vulpix = Pokemon(
        "Vulpix",
        95,
        [ascuas, lanzallamas],
        [muro_fuego, defensa_rapida]
        )
        listaPokemon=[pikachu, charmander, squirtle, bulbasaur, raichu, vulpix]
        pokemon_cliente: Pokemon=random.choice(listaPokemon)
        #pa que no wse repita.
        listaPokemon.remove(pokemon_cliente)
        pokemon_servidor: Pokemon=random.choice(listaPokemon)
        await ws.send_text(f"tu pokemon será {pokemon_cliente.nombre} vida:{pokemon_cliente.vida} y tu contrincante será {pokemon_servidor.nombre}")
        time.sleep(2)
        await ws.send_text("empezar-combate")
        turno=0
        ataqueCliente:Ataque
        accionCliente=""
        while(True):
            turno+=1
            
            #Movimiento Servidor
            accion_servidor=random.choice(["atacar", "defender"])
            if accion_servidor=="atacar" or turno==1 or accionCliente=="defensa":
                ataqueServidor=pokemon_servidor.atacar()
                await ws.send_text(f"{pokemon_servidor.nombre} te ha atacado con {ataqueServidor.nombre} el cual te quitará {ataqueServidor.daño} de vida")

            else:
                defensa :Defensa=pokemon_servidor.defender(ataqueCliente)
                if not pokemon_servidor.vivo:
                        break
                await ws.send_text(f"{pokemon_servidor} se ha defendido usando {defensa.nombre} contra tu ataque {ataqueCliente.nombre} quedandole de vida {pokemon_servidor.vida}")

            #Movimiento Cliente
            await ws.send_text("Selecciona que quieres hacer ATACAR o DEFENDER el ataque")
            accion= await ws.receive_text()
            if accion=="ATACAR":
                pokemon_cliente.recibir_daño(ataqueServidor)
                if not pokemon_cliente.vivo:
                    break
                accionCliente="atacar"
                ataqueCliente=pokemon_cliente.atacar()
                await ws.send_text(f"has atacado a {pokemon_servidor.nombre} con {ataqueCliente.nombre}")
                
            else:
                defensa :Defensa=pokemon_cliente.defender(ataqueServidor)
                if not pokemon_cliente.vivo:
                    break
                await ws.send_text(f"{pokemon_servidor} te has defendido usando {defensa.nombre} contra su ataque {ataqueServidor.nombre} quedandote de vida {pokemon_cliente.vida}")

    
    except WebSocketDisconnect:
        print("cliente desconectado")