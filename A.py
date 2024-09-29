import serial
import time
import logging

# Configurações do log
logging.basicConfig(filename='carrinho.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def conectar_arduino(porta='COM3', baudrate=9600):
    try:
        arduino = serial.Serial(porta, baudrate, timeout=1)
        logging.info(f"Conectado ao Arduino na porta {porta}")
        return arduino
    except serial.SerialException as e:
        logging.error(f"Erro ao conectar ao Arduino: {e}")
        raise

def processar_comando(comando):
    comando = comando.strip()
    if comando == "frente":
        print("O carrinho está indo para frente!")
        logging.info("Comando recebido: frente")
    elif comando == "esquerda":
        print("O carrinho está virando para a esquerda!")
        logging.info("Comando recebido: esquerda")
    elif comando == "direita":
        print("O carrinho está virando para a direita!")
        logging.info("Comando recebido: direita")
    else:
        print(f"Comando desconhecido: {comando}")
        logging.warning(f"Comando desconhecido recebido: {comando}")

def loop(arduino):
    while True:
        try:
            if arduino.in_waiting > 0:
                comando = arduino.readline().decode('utf-8').strip()
                if comando:
                    processar_comando(comando)
        except Exception as e:
            logging.error(f"Erro ao ler ou processar dados: {e}")
            print(f"Erro: {e}")
        time.sleep(1)

if __name__ == "__main__":
    try:
        arduino = conectar_arduino('COM3', 9600)  # Configuração da porta COM3 a 9600 baud
        loop(arduino)
    except Exception as e:
        print(f"Falha na execução do programa: {e}")
