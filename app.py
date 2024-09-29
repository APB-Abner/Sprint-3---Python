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
        # Assina os tópicos que você quer ouvir
        client.subscribe("APB/carrinho/leituras/distancia")
        client.subscribe("APB/carrinho/leituras/linha")
        client.subscribe("APB/carrinho/leituras/velocidade")
    else:
        logging.error(f"Falha na conexão com o broker MQTT. Código de retorno: {rc}")

# Função chamada quando uma mensagem é recebida
def on_message(client, userdata, msg):
    mensagem = msg.payload.decode()
    logging.info(f"Mensagem recebida no tópico {msg.topic}: {mensagem}")
    processar_mensagem(msg.topic, mensagem)

# Função para processar a mensagem e atualizar as variáveis globais
def processar_mensagem(topic, mensagem):
    global dados_recebidos
    try:
        if not mensagem:
            raise ValueError("Mensagem inválida ou None")
        
        logging.info(f"Processando mensagem: {mensagem}")

        # Atualiza as variáveis globais com base no tópico recebido
        if topic == "APB/carrinho/leituras/distancia":
            dados_recebidos['distancia'] = float(mensagem)
            logging.info(f"Distância atualizada: {dados_recebidos['distancia']} cm")
        elif topic == "APB/carrinho/leituras/linha":
            dados_recebidos['linha'] = int(mensagem)
            logging.info(f"Linha atualizada: {dados_recebidos['linha']}")
        elif topic == "APB/carrinho/leituras/velocidade":
            dados_recebidos['velocidade'] = float(mensagem)
            logging.info(f"Velocidade atualizada: {dados_recebidos['velocidade']} m/s")

        # Emite um evento para o front-end com os dados atualizados
        socketio.emit('atualizacao_dados', dados_recebidos)
        return True

    except Exception as e:
        logging.error(f"Erro ao processar a mensagem: {e}")
        return False

# Criação do cliente MQTT
def create_mqtt_client():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    try:
        client.connect("broker.hivemq.com", 1883, 60)
    except Exception as e:
        logging.error(f"Não foi possível conectar ao broker MQTT: {e}")
        return None
    client.loop_start()  # Inicia o loop em um thread separado
    return client

@app.route('/')
def index():
    return render_template('index.html')

# Rota para enviar os dados ao front-end via JSON
@app.route('/dados', methods=['GET'])
def dados():
    return jsonify(dados_recebidos)

if __name__ == '__main__':
    mqtt_client = create_mqtt_client()
    if mqtt_client:
        socketio.run(app, debug=True)
