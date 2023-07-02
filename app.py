# File contenente il codice Python per l'applicazione della legge di Amdahl
# per il calcolo della speedup e dell'efficienza di un programma parallelo.
# L'applicazione è stata sviluppata con il framework Flask e permette di
# visualizzare i risultati in una pagina web considerando anche la capacità
# di mostrare dei grafici.
from flask import Flask, render_template, request
import redis
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64

app = Flask(__name__)
r = redis.Redis(host='redis', port=6379, db=0)


@app.route('/', methods=['GET', 'POST'])
def home():
    pass
