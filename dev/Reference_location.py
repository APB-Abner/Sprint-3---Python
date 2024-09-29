from flask import Flask, render_template
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt
import logging

app = Flask(__name__)
socketio = SocketIO(app)

# Configuração de logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Distância entre os sensores (em metros)
DISTANCIA = 2.0  # ajuste conforme sua configuração

# Variáveis para armazenar os timestamps
sensor1_time = None
sensor2_time = None

# Função chamada quando uma mensagem MQTT é recebida
def on_message(client, userdata, msg):
    global sensor1_time, sensor2_time
    try:
        mensagem = msg.payload.decode()
        logging.info(f"Mensagem recebida no tópico {msg.topic}: {mensagem}")

        partes = mensagem.split(',')
        sensor = partes[0].strip()
        timestamp = int(partes[1].strip())

        if sensor == "Sensor1":
            sensor1_time = timestamp
            logging.info(f"Sensor1_time atualizado: {sensor1_time}")
            # Emitir para front-end (opcional)
            socketio.emit('sensor1_triggered', {'time': sensor1_time})
            # Resetar sensor2_time
            sensor2_time = None
        elif sensor == "Sensor2":
            if sensor1_time is not None:
                sensor2_time = timestamp
                tempo = (sensor2_time - sensor1_time) / 1000.0  # Convertendo para segundos
                if tempo > 0:
                    velocidade = DISTANCIA / tempo  # m/s
                    velocidade_kmh = velocidade * 3.6  # Convertendo para km/h
                    logging.info(f"Velocidade calculada: {velocidade_kmh:.2f} km/h")
                    print(f"Velocidade: {velocidade_kmh:.2f} km/h")
                    # Emitir a velocidade para o front-end
                    socketio.emit('velocidade', {'velocidade_kmh': f"{velocidade_kmh:.2f}"})
                else:
                    logging.warning("Tempo entre sensores é zero ou negativo.")
                # Resetar os timestamps
                sensor1_time = None
                sensor2_time = None
            else:
                logging.warning("Sensor2 acionado sem Sensor1 acionado previamente.")
    except Exception as e:
        logging.error(f"Erro ao processar mensagem: {e}")

# Configurando o clxiente MQTT
def setup_mqtt():
    client = mqtt.Client()
    client.on_message = on_message
    try:
        client.connect("broker.hivemq.com", 1883, 60)  # Substitua pelo IP do seu broker
    except Exception as e:
        logging.error(f"Não foi possível conectar ao broker MQTT: {e}")
        return None
    client.subscribe("APB/carrinho/leituras")
    client.loop_start()
    return client

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    mqtt_client = setup_mqtt()
    if mqtt_client:
        socketio.run(app, debug=True)
