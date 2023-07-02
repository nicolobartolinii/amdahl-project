# Usiamo un'immagine base di Python
FROM python:3.10

# Impostiamo una directory di lavoro
WORKDIR /app

# Copiamo i file requirements.txt nel container
COPY requirements.txt .

# Installiamo le varie dipendenze
RUN pip install -r requirements.txt

# Copiamo il codice sorgente nel container
COPY . .

# Impostiamo la variabile d'ambiente per indicare il punto in cui deve essere eseguito Flask
ENV FLASK_APP=app.py

# Esponiamo la porta 5000
EXPOSE 5000

# Avviamo l'applicazione
CMD ["flask", "run", "--host=0.0.0.0"]