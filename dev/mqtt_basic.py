import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Conectado com o código: " + str(rc))
    client.subscribe("APB/carrinho/leituras")

def on_message(client, userdata, msg):
    print(f"Mensagem recebida: {msg.payload.decode()}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.hivemq.com", 1883, 60)  # Ou seu servidor MQTT
client.loop_forever()
