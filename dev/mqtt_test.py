import paho.mqtt.client as mqtt
import logging

# Função chamada quando o cliente conecta ao broker MQTT
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("Conexão bem-sucedida ao broker MQTT.")
        client.subscribe("carrinho/leituras")
    else:
        logging.error(f"Falha na conexão com o broker MQTT. Código de retorno: {rc}")

# Função chamada quando uma mensagem é recebida
def on_message(client, userdata, msg):
    mensagem = msg.payload.decode()
    logging.info(f"Mensagem recebida: {mensagem}")
    print(f"Mensagem MQTT recebida: {mensagem}")
    processar_mensagem(mensagem)

# Função para processar a mensagem (ajuste conforme necessário)
def processar_mensagem(mensagem):
    try:
        # Aqui vai a lógica de processamento da mensagem recebida
        print(f"Processando mensagem: {mensagem}")
    except Exception as e:
        logging.error(f"Erro ao processar a mensagem: {e}")

# Criação do cliente MQTT com a versão mais recente da API
client = mqtt.Client(client_id="", clean_session=True, userdata=None, protocol=mqtt.MQTTv311)

client.on_connect = on_connect
client.on_message = on_message

# Conecta ao broker MQTT
client.connect("broker.hivemq.com", 1883, 60)

# Inicia o loop para receber mensagens
client.loop_start()



if __name__ == '__main__':
    mqtt_client=create_mqtt_client()