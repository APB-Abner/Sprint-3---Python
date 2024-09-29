# ///------------------------------------------------|||------------------------------------------------//
# ///------------------------------------------------|||------------------------------------------------//
# ///------------------------------------------------|||------------------------------------------------//
# ///------------------------------------------------|||------------------------------------------------//
'/-------------------------NÃO EDITAR, JÁ LIGA MQTT E FLASK PARA RECEBER AQUIVOS-------------------------/'
# ///------------------------------------------------|||------------------------------------------------//
# ///------------------------------------------------|||------------------------------------------------//
# ///------------------------------------------------|||------------------------------------------------//
# ///------------------------------------------------|||------------------------------------------------//
# ///------------------------------------------------|||------------------------------------------------//


import time
import paho.mqtt.client as mqtt
import logging
from flask import Flask, render_template, jsonify

# Configurações do Flask
app = Flask(__name__)

# Variáveis globais para armazenar dados do MQTT
dados_recebidos = {
    'distancia': 0.0,
    'linha': 0,
    'velocidade': 0.0
}

# Configuração do logging
logging.basicConfig(filename='../carrinho.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Função para calcular a velocidade (usando dados de dois sensores)
def calcular_velocidade(distancia_entre_sensores, tempo_inicio, tempo_fim):
    if tempo_fim > tempo_inicio:
        tempo_total = tempo_fim - tempo_inicio
        velocidade = distancia_entre_sensores / tempo_total  # m/s
        return velocidade
    else:
        logging.error("Erro nos dados de tempo: tempo_fim é menor que tempo_inicio.")
        return None

# Função para processar a mensagem recebida via MQTT
def processar_mensagem(mensagem):
    try:
        dados = mensagem.split(',')
        distancia = float(dados[0].split(':')[1])  # Extrair distância
        linha = int(dados[1].split(':')[1])  # Extrair o status da linha (0 ou 1)

        logging.info(f'Dados recebidos - Distância: {distancia} cm, Linha: {linha}')

        # Atualizar variáveis globais
        dados_recebidos['distancia'] = distancia
        dados_recebidos['linha'] = linha

        # Exemplo de uso de if-else e decisão lógica
        if linha == 1:
            logging.info("Carrinho está seguindo a linha corretamente.")
        else:
            logging.warning("Carrinho saiu da linha! Corrigir direção.")

        # Simulando sensores para cálculo de velocidade
        tempo_inicio = time.time()  # Registra o tempo em que o sensor 1 detecta o carrinho
        time.sleep(1.5)  # Simula o tempo entre os sensores
        tempo_fim = time.time()  # Registra o tempo quando o sensor 2 detecta o carrinho
        distancia_entre_sensores = 1.0  # Distância entre os sensores em metros (ajustável)

        # Calcular a velocidade
        velocidade = calcular_velocidade(distancia_entre_sensores, tempo_inicio, tempo_fim)
        if velocidade:
            dados_recebidos['velocidade'] = velocidade
            logging.info(f'Velocidade do carrinho: {velocidade:.2f} m/s')
        else:
            logging.error("Falha ao calcular a velocidade.")

    except Exception as e:
        logging.error(f"Erro ao processar a mensagem: {e}")

# Função callback chamada quando o cliente se conecta ao broker MQTT
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("Conexão bem-sucedida ao broker MQTT.")
        client.subscribe("carrinho/leituras")
    else:
        logging.error(f"Falha na conexão com o broker MQTT. Código de retorno: {rc}")

# Função callback chamada quando uma mensagem é recebida no tópico MQTT
def on_message(client, userdata, msg):
    mensagem = msg.payload.decode()
    logging.info(f"Mensagem recebida: {mensagem}")
    processar_mensagem(mensagem)

# Função principal que configura o cliente MQTT e conecta ao broker
def iniciar_mqtt():
    try:
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect("broker.hivemq.com", 1883, 60)  # Conectar ao broker MQTT

        # Loop principal do cliente MQTT
        client.loop_start()  # Usar loop_start para não bloquear o Flask

    except Exception as e:
        logging.error(f"Erro ao iniciar o cliente MQTT: {e}")

# Rota principal que renderiza a página HTML
@app.route('/')
def index():
    return render_template('index.html')

# Rota para enviar os dados ao front-end via JSON
@app.route('/dados', methods=['GET'])
def dados():
    return jsonify(dados_recebidos)



if __name__ == "__main__":
    # Iniciar o cliente MQTT
    iniciar_mqtt()
    # Iniciar o servidor Flask
    app.run(debug=True)
