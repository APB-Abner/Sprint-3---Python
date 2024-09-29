from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt
import logging


# Configurando o logger para capturar logs
logging.basicConfig(level=logging.INFO)

# Configurando Flask Server
app = Flask(__name__)
socketio = SocketIO(app)

# Variáveis globais para armazenar dados do MQTT
dados_recebidos = {
    'distancia': 0.0,
    'linha': 0,
    'velocidade': 0.0
}

# Função chamada quando o cliente conecta ao broker MQTT
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("Conexão bem-sucedida ao broker MQTT.")
        client.subscribe("APB/carrinho/leituras")
    else:
        logging.error(f"Falha na conexão com o broker MQTT. Código de retorno: {rc}")

# Função chamada quando uma mensagem é recebida
def on_message(client, userdata, msg):
    mensagem = msg.payload.decode()
    logging.info(f"Mensagem recebida: {mensagem}")
    processar_mensagem(mensagem)

# Função para processar a mensagem (ajuste conforme necessário)
def processar_mensagem(mensagem):
    msg = mensagem
    topic = msg.topic()
    try:
        if not mensagem:
            raise ValueError("Mensagem inválida ou None")
        # Simulação do processamento
        logging.info(f"Processando mensagem: {mensagem}")
        if topic == "*/distancia":
            distancia = float(mensagem)
            logging.info(f"Distância recebida: {distancia} cm")
        elif topic == "*/linha":
            linha = int(mensagem)
            logging.info(f"Linha recebida: {linha}")
        elif topic == "*/velocidade":
            velocidade = float(mensagem)
            logging.info(f"Velocidade recebida: {velocidade} m/s")
        return True
    except Exception as e:
        logging.error(f"Erro ao processar a mensagem: {e}")
        return False


# Criação do cliente MQTT
def create_mqtt_client():
    client = mqtt.Client()
    logging.info(f"Resultado do client: {client}")
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

# Rota para enviar os dados ao front-end via JSON
@app.route('/dados', methods=['GET'])
def dados():
    return jsonify(dados_recebidos)

if __name__ == '__main__':
    mqtt_client=create_mqtt_client()
    if mqtt_client:
        socketio.run(app, debug=True)