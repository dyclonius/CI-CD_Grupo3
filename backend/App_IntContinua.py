#Importar dependencias
from flask import Flask, request, jsonify
from pymongo import MongoClient, ASCENDING #manejo de la base de datos 
from flask_cors import CORS #Manejo de cabeceras en el cliente
from bson import ObjectId
import time
import pika # Manejo de conexiones con rabbitMq
import json 
import threading # Manejo de conexiones con rabbitMq - hilos de consumidores

app = Flask(__name__)
#implementar CORS para los request de otros dominios
CORS(app)

# Credenciales y datos de conexión Mongo
mongo_host = 'dbContable'
mongo_port = 27017
mongo_user = 'carlos'
mongo_password = '123'  
mongo_db = 'db_Contable'

# Construir la URI de conexión con las credenciales
mongo_uri = f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}/{mongo_db}?authSource=admin"

# Conexión a la base de datos Mongo
client = MongoClient(mongo_uri)
db = client[mongo_db]
#creacion de la colección de usuarios
collection = db.usuarios
collection.create_index([('identificacion', ASCENDING)], unique=True)
#creacion de la colección de ortidas fiscales
collectionPart = db.partidas_db
collectionPart.create_index([('identificacion', ASCENDING), ('codigo', ASCENDING)], unique=True)

#metodo prueba creación manual docker
@app.route('/prueba', methods=['GET'])
def prueba():
    return "Prueba de conexión satisfactoria"

# endpoint creacion de usuarios -----------------------------------------
# crear un usuari
@app.route('/create_user', methods=['POST'])
def create_user():
    user_data = request.json #json recibido en el endpoint
    #verificacion de datos completos
    if 'identificacion' not in user_data or 'nombre' not in user_data or 'apellidos' not in user_data or 'email' not in user_data or 'telefono' not in user_data:
        return 'Faltan campos requeridos (identificacion, nombre, apellidos, email, telefono)\n', 400
    #si los datos estan completos enviar a la cola de rabbitmq
    send_to_queue('user_queue', {'action': 'create_user', 'data': user_data})
    return 'usuario creado correctamente\n', 201

# endpoint creacion partida fiscal------------------------------------------
# crear una partida fiscal
@app.route('/partida_create', methods=['POST'])
def partida_create():
    user_data = request.json #json recibido en el endpoint
    required_fields = ['identificacionBuscar', 'fecha', 'nit', 'nombreComercio', 'itemDescripcion', 'subtotal', 'total', 'codigo']
    missing_fields = [field for field in required_fields if field not in user_data]
    #manejo de datos faltantes
    if missing_fields:
        return jsonify({'error': f'Faltan campos requeridos: {", ".join(missing_fields)}'}), 400
    #convertir datos para manejo de la bd
    try:
        identificacionBuscar = user_data['identificacionBuscar']
        fecha = user_data['fecha']
        nit = user_data['nit']
        nombreComercio = user_data['nombreComercio']
        itemDescripcion = user_data['itemDescripcion']
        subtotal = float(user_data['subtotal'])
        total = float(user_data['total'])
        codigo = int(user_data['codigo'])
    except ValueError as e:
        return jsonify({'error': f'Error en la conversión de tipos de datos: {e}'}), 400
    #buscar en la coleccion de usuarios la identificación eextraida
    user = collection.find_one({'identificacion': identificacionBuscar})
    # manejo de identificacion encontrada
    if not user:
        print(f"Usuario con identificación {identificacionBuscar} no encontrado.")
        return jsonify({'error': f'La identificación {identificacionBuscar} no existe, ¡Verifique o registre primero el cliente!'}), 400
    #si es encontrado creamos un json y los enviamos a la cola 
    new_data = {
        'identificacion': identificacionBuscar,
        'fecha': fecha,
        'nit': nit,
        'nombreComercio': nombreComercio,
        'itemDescripcion': itemDescripcion,
        'subtotal': subtotal,
        'total': total,
        'codigo': codigo
    }
    #especificamos cual es la accion que queremos hacer para que la identifique el consumidor
        #nombre de la cola, accion a realizar por el consumidor, datos
    send_to_queue('partida_queue', {'action': 'create_partida', 'data': new_data})
    return jsonify({'message': 'Partida Fiscal registrada correctamente'}), 201

#endpoint retornar partidas fiscales de una identificacion---------------------------------------------
#retorna partidas fiscales
@app.route('/partidas/<identificacionCliente>', methods=['GET'])
def get_partidas(identificacionCliente):
    #buscar por la identificacion del cliete
    if not collection.find_one({'identificacion': identificacionCliente}):
        return jsonify({'error': f'La identificación {identificacionCliente} no existe, ¡Verifique o registre primero el cliente!'}), 400
    #listar datos del cliente
    partidas = list(collectionPart.find({'identificacion': identificacionCliente}, {'_id': 0}))
    #sumar los valores de las partidas
    total_partidas = sum(partida['total'] for partida in partidas)
    #retornar el listado y el total
    response = {
        'partidas': partidas,
        'total_partidas': total_partidas
    }
    return jsonify(response), 200


#implementacion generador y consumidor de colas--------------------------------------------------------------------------------------
def send_to_queue(queue_name, message):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='rabbitmq', #nombre del contenedor docker de rabbitmq
            credentials=pika.PlainCredentials('cicdG3', 'password') #credenciales de acceso al host de rabbit mq, establecidas en la creacion del contenedor.
        )
    )
    #configuracion estandar de la conexion 
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,
        ))
    connection.close()
#implementacion d elos consumidores ------------------------------------------------------------------------------------------------
def callback(ch, method, properties, body):
    message = json.loads(body) #este json lo gestiona internamente rabbitmq, es el que se le envio a la cola del generador
    try:
        if 'action' in message: #conprueba la accion que se le envio en el mensaje a la cola
            if message['action'] == 'create_user':
                collection.insert_one(message['data'])# si la accion es crear un usuario
            elif message['action'] == 'create_partida':
                collectionPart.insert_one(message['data'])# si la accion es crear una partida
            ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        time.sleep(1) #manejo de errores en caso de que la cola este ocupada o caida
#inicializar los consumidores
def start_consuming(queue_name):
    while True:
        try: #datos del contenedor de rabbitmq
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host='rabbitmq',
                    credentials=pika.PlainCredentials('cicdG3', 'password')
                )
            )
            #configuracion estandar de conexion con rabbitmq, para una conexion permanente que permanece a la escucha y procesa 1 mensaje a la vez
            channel = connection.channel()
            channel.queue_declare(queue=queue_name, durable=True)
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue=queue_name, on_message_callback=callback)
            channel.start_consuming()
        except pika.exceptions.AMQPConnectionError as e:
            time.sleep(5) #manejo de errores en caso de que la cola este ocupada o caida

#definir e inicializar los dos consumidores en hilos independientes
user_consumer_thread = threading.Thread(target=start_consuming, args=('user_queue',))
partida_consumer_thread = threading.Thread(target=start_consuming, args=('partida_queue',))
user_consumer_thread.start()
partida_consumer_thread.start()

    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')











