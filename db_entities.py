import datetime as dt
from pony.orm import *

db = Database()
db.bind('postgres', user='joao', password='teller', host='', database='desafioglobo')

class Paredao(db.Entity):
    id = PrimaryKey(int, auto=True)
    inicio = Required(dt.datetime, 5)
    participantes = Set('Participante')
    votos = Set('Voto')

class Participante(db.Entity):
    nome = PrimaryKey(str)
    avatar = Required(str)
    paredao = Set('Paredao')
    votos = Set('Voto')

class Voto(db.Entity):
    id = PrimaryKey(int, auto=True)
    data = Required(dt.datetime, 5)
    paredao = Required(Paredao)
    escolha = Required(Participante)

db.generate_mapping(create_tables=True)
