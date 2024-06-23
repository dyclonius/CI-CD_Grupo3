# imagen Python para el backend
FROM python:3.9 AS backend

# directorio backend
WORKDIR /app/backend

# Copiar las dependencias al directorio del contenedor
COPY requirements.txt .

# Instalar las dependencias 
RUN pip install --no-cache-dir -r requirements.txt

# Copiar codigo fuente
COPY . .

#poner en escucha el puerto 5000 para el backend
EXPOSE 5000

# Comando para ejecutar backend
CMD ["python", "App_IntContinua.py"]