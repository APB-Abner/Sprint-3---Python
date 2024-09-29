import paho.mqtt.client as mqtt
import time
import logging

# Configuração de logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Função chamada quando o cliente se conecta ao broker
def on_connect(client, userdata, flags, rc):
    logging.info(f"Conectado ao broker com código: {rc}")
    client.subscribe("APB/carrinho/leituras")  # Assinando o tópico


# Função chamada quando uma mensagem é recebida
def on_message(client, userdata, msg):
    logging.info(f"Mensagem recebida: {msg.payload.decode()}")


# Função principal
def main():
    # Criação do cliente MQTT
    client = mqtt.Client()

    # Definindo as funções de callback
    client.on_connect = on_connect
    client.on_message = on_message

    # Conexão ao broker
    try:
        client.connect("broker.hivemq.com", 1883, 60)  # ou seu servidor MQTT
    except Exception as e:
        logging.error(f"Falha ao conectar ao broker: {e}")
        return

    # Iniciando o loop de escuta de mensagens
    client.loop_start()  # Inicia a escuta em um thread separado

    try:
        while True:
            time.sleep(1)  # Mantém o programa em execução
    except KeyboardInterrupt:
        logging.info("Desconectando...")
    finally:
        client.loop_stop()  # Para o loop
        client.disconnect()  # Desconecta do broker


if __name__ == "__main__":
    main()
