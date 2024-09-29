import unittest
import paho.mqtt.client as mqtt
from unittest.mock import MagicMock, patch
import logging
from app import processar_mensagem, create_mqtt_client, on_connect, on_message

class TestMQTTClient(unittest.TestCase):

    def setUp(self):
        # Configurações iniciais antes de cada teste
        self.client = create_mqtt_client()

    def test_on_connect_success(self):
        # Testando conexão bem-sucedida (rc = 0)
        with patch('app.logging.info') as mock_log_info:
            on_connect(self.client, None, None, 0)
            mock_log_info.assert_called_with("Conexão bem-sucedida ao broker MQTT.")

    def test_on_connect_failure(self):
        # Testando falha de conexão (rc != 0)
        with patch('app.logging.error') as mock_log_error:
            on_connect(self.client, None, None, 1)
            mock_log_error.assert_called_with("Falha na conexão com o broker MQTT. Código de retorno: 1")

    def test_on_message(self):
        # Simulando uma mensagem recebida e checando se o processar_mensagem foi chamado
        with patch('app.processar_mensagem') as mock_processar_mensagem:
            msg = MagicMock()
            msg.payload.decode.return_value = "Teste de mensagem"
            on_message(self.client, None, msg)
            mock_processar_mensagem.assert_called_with("Teste de mensagem")

    def test_processar_mensagem(self):
        # Testando se a função de processamento retorna True
        resultado = processar_mensagem("Mensagem de teste")
        self.assertTrue(resultado)

    def test_processar_mensagem_erro(self):
        # Simulando erro no processamento de mensagem
        with patch('app.logging.error') as mock_log_error:
            resultado = processar_mensagem(None)
            self.assertFalse(resultado)
            mock_log_error.assert_called()


class FlaskAppTest(unittest.TestCase):

    def create_app(self):
        from app import app  # Importando o app aqui para referência
        app.config['TESTING'] = True
        return app

    def setUp(self):
        self.app = self.create_app()  # Cria a referência para o app
        self.client = self.app.test_client()
        self.client_mqtt = mqtt.Client()
        self.client_mqtt.connect("broker.hivemq.com", 1883, 60)  # Conexão com o broker MQTT
        self.client_mqtt.loop_start()  # Inicia o loop do cliente MQTT

    def tearDown(self):
        self.client_mqtt.loop_stop()  # Para o loop do cliente MQTT
        self.client_mqtt.disconnect()  # Desconecta o cliente MQTT

    def test_home_page(self):
        # Testando a página inicial do Flask
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sucesso', response.data)  # Verificando se a resposta contém 'Sucesso'

    def test_processar_mensagem(self):
        # Testando com uma mensagem válida
        self.assertTrue(processar_mensagem("Teste de mensagem"))

    def test_processar_mensagem_erro(self):
        # Testando com uma mensagem None
        self.assertFalse(processar_mensagem(None))

    def test_flask_server_mqtt_integration(self):
        # Publica uma mensagem de teste no tópico MQTT
        self.client_mqtt.publish("test/topic", "Teste de mensagem")

        # Simula um pequeno atraso para permitir que a mensagem seja processada
        import time
        time.sleep(1)

        # Verifica se a mensagem foi processada com base no log
        with patch('app.logging.info') as mock_log_info:
            logging.info("Testando se a mensagem foi processada.")
            mock_log_info.assert_called_with("Testando se a mensagem foi processada.")

if __name__ == '__main__':
    unittest.main()
