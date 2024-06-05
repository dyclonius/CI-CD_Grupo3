# imagen Python para el backend
FROM python:3.9 AS backend

# directorio backend
WORKDIR /app/backend

# Copia e instala las dependencias del backend
COPY ./backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia código fuente del backend
COPY ./backend/ .

EXPOSE 5000

# Comando para ejecutar app
CMD ["python", "App_IntContinua.py"]








