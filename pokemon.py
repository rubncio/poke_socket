import random


class Ataque:
    def __init__(self, nombre, daño):
        self.nombre=nombre
        self.daño=daño

class Defensa:
    def __init__(self, nombre, escudo):
        self.nombre=nombre
        self.escudo=escudo

class Pokemon:
    def __init__(self, nombre, vida, ataques:list[Ataque], defensas:list[Defensa]):
        self.nombre=nombre
        self.vida=vida
        self.ataques=ataques
        self.defensas=defensas
        self.vivo=True

    def atacar(self)->Ataque:
        ataque:Ataque=random.choice(self.ataques)
        return ataque
        
    def defender(self, ataque_a_defender)->Defensa:
        defensa:Defensa=random.choice(self.defensas)
        
        self.recibir_daño(ataque_a_defender, defensa)
        return defensa

    """def recibir_daño(self, ataque:Ataque):
        daño=ataque.daño
        self.vida-=daño
        if self.vida<=0:
            self.vivo=False"""
    
    def recibir_daño(self, ataque:Ataque, defensa:Defensa=None):
        if ataque:
            daño=ataque.daño
            if defensa:
                daño-=defensa.escudo
            self.vida-=daño
            if self.vida<=0:
                self.vivo=False



