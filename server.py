from flask import Flask, redirect, render_template, request, send_file
import pickle
import random 
import requests


app = Flask(__name__)


import pickle

with open("database", "rb") as fp:
    arquivo = pickle.load(fp)

@app.route('/', methods=['GET'])
def index():
    return render_template("indexx.html")

@app.route('/search')
def search():
    word = request.args.get('query')

    def achararquivo():
        for i in arquivo:
            if i["word"] == word:
                return i["id"]
    if achararquivo() != None:
        return redirect('/word/'+ f'{achararquivo()}')
    else: 
        return redirect("/notfound")


@app.route('/notfound')
def notfound():
    return render_template("notfound.html")

@app.route('/word/<id>')
def outrapag(id):
    def acharpalavra():
        for i in arquivo:
            if i["id"] == id:
                return i

    
    g = acharpalavra()
    g = g["word"]
    if type(g) != None:
        response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{g}")
        response = response.json()
        response = response[0]
        audio = ""
        for i in response["phonetics"]:
            if i["audio"] != '':
                print(i["audio"])
                audio = i["audio"]
                break
    else:
        audio = "nothing"

    return render_template("word.html", cursor = acharpalavra(), audio = audio)

@app.route('/tenrandom')
def tenrandom():
    lista = []
    for i in range(0,10000):
        lista.append(i)

    x = random.choices(lista,k=10)

    outralista = []
    for h in x:
        for z in arquivo:
            if int(h) == int(z["id"]):
                outralista.append(z)
                break

    return render_template("tenrandom.html", outralista = outralista)

@app.route('/page/<id>')
def pages(id):
    z = int(id) * 20
    h = int(z + 20)
    lista = []

    if z != 0:
        for i in arquivo[z:h]:
            lista.append(i)
    else: 
        for i in arquivo[0:20]:
            lista.append(i)
    return render_template("all.html", lista = lista, id = int(id)  )
        
@app.route('/download')
def download_file():
	path = "10k.pdf"
	return send_file(path, as_attachment=True)
