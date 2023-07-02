# File contenente il codice Python per l'applicazione della legge di Amdahl
# per il calcolo della speedup e dell'efficienza di un programma parallelo.
# L'applicazione è stata sviluppata con il framework Flask e permette di
# visualizzare i risultati in una pagina web considerando anche la capacità
# di mostrare dei grafici.
import uuid
from io import BytesIO

import matplotlib.pyplot as plt
import numpy as np
import redis
from flask import Flask, request, send_file, session, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'CHIAVE'
r = redis.Redis(host='redis', port=6379, db=0)


@app.route('/', methods=['GET', 'POST'])
def home():
    if 'id' not in session:
        session['id'] = str(uuid.uuid4())
    return render_template('home.html')


def amdahl_law(p, n):
    """
    Funzione che si occupa di calcolare il miglioramento delle prestazioni (speedup) secondo la legge di Amdahl.

    :param p: (float) è la percentuale del programma che può essere parallelizzata (0 <= p <= 1)
    :param n: (int) è il numero di processori
    :return: (float) lo speedup, cioè il miglioramento delle prestazioni
    """
    if not (0 <= p <= 1):
        raise ValueError("p deve essere compreso tra 0 e 1")

    try:
        n = int(n)
    except ValueError:
        raise ValueError("n deve essere un intero positivo")

    if n < 1:
        raise ValueError("n deve essere un intero positivo")

    # Qui calcoliamo lo speedup seguendo la formula della legge di Amdahl
    speedup = 1 / ((1 - p) + (p / n))

    return speedup


@app.route('/amdahl', methods=['GET'])
def amdahl():
    """
    Funzione che si occupa della rotta per visualizzare i risultati della legge di Amdahl.

    :return: (str) pagina HTML con i risultati
    """
    # Recuperiamo i parametri della richiesta GET
    p = float(request.args.get('p', ''))
    n = int(request.args.get('n', ''))

    # Creiamo una chiave univoca per questa combinazione di p e n per Redis
    key = f'amdahl:{session["id"]}:{p}:{n}'

    # Otteniamo l'eventualmente già calcolato risultato da Redis
    speedup = r.get(key)

    if speedup is None:
        # Se il risultato non si trova in Redis, calcoliamolo e salviamolo, oltre a generare il grafico
        n_values = np.linspace(1, 100, 100)
        speedup_values = [amdahl_law(p, n_var) for n_var in n_values]

        # Creazione del grafico
        plt.figure()
        plt.plot(n_values, speedup_values, label='Speedup vs numero di processori variabile')
        plt.plot(n, amdahl_law(p, n), 'ro', label=f'Speedup per n = {n}')
        plt.xlabel('Numero di processori (n)')
        plt.ylabel('Speedup')
        plt.title(f'Legge di Amdahl (p = {p})')
        plt.legend()

        # Salvataggio del gragico come PNG in un buffer di memoria
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        # Memorizzazione del buffer di memoria in Redis
        r.set(key, buffer.read())

        # Riposizionamento del puntatore del buffer di memoria all'inizio
        buffer.seek(0)

        return send_file(buffer, mimetype='image/png')
    else:
        # Altrimenti, carichiamo il risultato da Redis nel buffer di memoria
        buffer = BytesIO(speedup)
        buffer.seek(0)

        return send_file(buffer, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
