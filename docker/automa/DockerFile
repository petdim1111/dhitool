# Använd en officiell Python-runtime som en förälder bild
FROM jupyter/base-notebook:latest

# Sätt arbetskatalogen i behållaren till /app
WORKDIR /app

# Kopiera specifika filer från din lokala katalog till behållaren
COPY requirements.txt _start.ipynb autoMA.py ./

# Installera eventuella nödvändiga paket som specificeras i requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Gör port 8866 tillgänglig för världen utanför denna behållare
EXPOSE 8866

# Kör voila på behållarens start
CMD ["voila", "--port=8866", "--no-browser", "--enable_nbextensions=True"]
