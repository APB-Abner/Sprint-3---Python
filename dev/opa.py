from flask import Flask, render_template
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt

app = Flask(__name__)
socketio = SocketIO(app)


# Função chamada quando uma mensagem MQTT é recebida
def on_message(client, userdata, msg):
    sensor_data = msg.payload.decode()
    print(f"Mensagem recebida: {sensor_data}")

    # Enviar os dados do sensor para a página
    socketio.emit('update_data', {'data': sensor_data})


# Configurando o cliente MQTT
mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.connect("broker.hivemq.com", 1883, 60)
mqtt_client.subscribe("carrinho/leituras")
mqtt_client.loop_start()


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    socketio.run(app, debug=True)
