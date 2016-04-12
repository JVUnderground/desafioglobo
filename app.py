#!flask/bin/python
# -*- coding: utf-8 -*-
import datetime as dt
from flask import Flask, render_template, request, redirect
from db_entities import *

app = Flask(__name__)
PIXWIDTH = 300;
PIXHEIGHT = 300;

@app.route('/paredao/ultimo')
@db_session
def ultimoParedao():
    """
    ultimoParedao: mostra a página de resultados detalhados do paredão mais recente.
    
    O modelo de dados é desenhado de tal forma que permite os paredões triplos, quadruplos, etc.
    """
    # Por alguma razão limit(1) retorna um resultado estranho, talvez bug? Não tem problema se usar um limite maior.
    ultimo = Paredao.select().order_by(Paredao.inicio.desc()).limit(2)[0]
    total = len(ultimo.votos)
    taxa = float("{0:.1f}".format(total/horasDesde(ultimo.inicio)))
    
    participantes = []
    for p in ultimo.participantes:
        participantes.append({
            "nome": p.nome,
            "votos": len(ultimo.votos.select(lambda v: v.escolha == p)[:]) 
        })

    dados = {
        "inicio": ultimo.inicio.strftime("%d/%m/%Y"),
        "total": total, 
        "taxa": taxa,
        "participantes": participantes,
    }

    return render_template("paredao.html", dados=dados)

@app.route('/')
@db_session
def pageVotar():
    """
    pageVotar: Essa função renderiza a página principal do usuário, onde este pode votar na eliminação ou não
               de um dos participantes.
    """

    ultimo = Paredao.select().order_by(Paredao.inicio.desc()).limit(2)[0]
    part_ordenado = ultimo.participantes.select().order_by(lambda p: p.nome)[:]
    participantes = []
    for i,p in enumerate(part_ordenado):
        participantes.append({
            "nome": p.nome,
            "avatar": p.avatar,
            "sms": 8001 + i,
            "telefone": "0800-123-%03d" % (i+1),
        })

    dados = {
        "paredao": ultimo.id,
        "inicio": ultimo.inicio.strftime("%d/%m/%Y"),
        "participantes": participantes,
        "width": (PIXWIDTH + 20)*len(participantes),
        "pixheight": PIXHEIGHT,
        "pixwidth": PIXWIDTH,
    }
    return render_template("vote.html", dados=dados)

@app.route('/votar', methods=["POST"])
@db_session
def registrarVoto():
    escolha = request.form["escolha"]
    pid = request.form["paredao"]
    voto = Voto(escolha=escolha, paredao=Paredao[pid], data=dt.datetime.now())
    return "sucesso"

@app.route('/resultado')
@db_session
def pageResultado():
    return "Página de resultados"

def horasDesde(tempo):
    delta = dt.datetime.now() - tempo
    dd = divmod(delta.days*86400 + delta.seconds, 60)
    horas = dd[0]/60. + dd[1]/3600.
    return horas

if __name__ == '__main__':
    app.run(debug=True)
