# Projeto de Divulgação da Fórmula E com Carrinhos Elétricos Controlados por Arduino

Este projeto foi desenvolvido com o objetivo de promover a **Fórmula E**, uma categoria de automobilismo totalmente elétrica, para um público mais amplo, incluindo jovens e pessoas com deficiência sensorial, como o Transtorno do Espectro Autista. A proposta é aumentar o interesse pela Fórmula E, incentivando a curiosidade sobre a **mobilidade sustentável** e mostrando que o esporte pode ser emocionante, acessível e inovador.

## Objetivo do Projeto

Nossa meta é atrair novos fãs para a Fórmula E, especialmente **jovens** e **pessoas sensíveis a barulhos**, oferecendo uma experiência interativa com **carrinhos elétricos** controlados por **Arduino**. Esses carrinhos foram projetados para replicar algumas das características dos veículos de Fórmula E, como o motor elétrico silencioso, tornando o projeto inclusivo e acessível, especialmente para pessoas no espectro autista que podem ser sensíveis a ruídos altos.

O projeto não é apenas uma ferramenta educacional para jovens interessados em tecnologia, mas também visa destacar as vantagens dos **veículos elétricos** e a importância da **sustentabilidade** no esporte.

## Tecnologias Utilizadas

- **Flask**: Framework web para criar a interface do sistema.
- **Paho MQTT**: Protocolo de comunicação para troca de mensagens entre os carrinhos e o servidor.
- **Socket.IO**: Comunicação em tempo real entre o servidor Flask e o front-end.
- **Arduino**: Microcontrolador usado nos carrinhos para coleta e envio de dados.

## Funcionalidades

O código inclui as seguintes funcionalidades:

- **Leitura de Sensores**: Os carrinhos monitoram dados como distância, velocidade e alinhamento (detecção de linha) e enviam essas informações via MQTT.
- **Processamento de Dados**: O servidor recebe os dados dos sensores e atualiza uma interface em tempo real, possibilitando o acompanhamento remoto dos carrinhos.
- **Interface em Tempo Real**: Através do Flask e Socket.IO, os dados dos carrinhos são atualizados automaticamente em uma interface web, facilitando a interação e visualização.
- **Conexão MQTT**: A comunicação entre o Arduino e o servidor é feita via MQTT, permitindo uma comunicação rápida e eficiente entre os dispositivos.

## Estrutura do Código

### 1. **Servidor Flask**

O servidor Flask lida com a lógica da aplicação, exibindo os dados recebidos dos carrinhos e se comunicando com o front-end via Socket.IO para atualizar a interface web em tempo real.

### 2. **Cliente MQTT**

O cliente MQTT é responsável por se conectar ao broker MQTT, assinar tópicos específicos (como distância, velocidade, linha), e processar as mensagens recebidas.

### 3. **Processamento de Mensagens**

As mensagens recebidas dos sensores dos carrinhos são processadas e armazenadas em variáveis globais. Em seguida, o servidor Flask emite eventos de atualização que são enviados para a interface web.

### 4. **Desconexão Segura**

O código inclui uma finalização apropriada, que garante que o cliente MQTT seja desconectado corretamente quando o servidor Flask for interrompido.

## Requisitos de Instalação

### 1. **Dependências**

- **Python 3.x**
- Flask (`pip install flask`)
- Flask-SocketIO (`pip install flask-socketio`)
- Paho-MQTT (`pip install paho-mqtt`)
- Eventlet para melhorar o desempenho com Flask-SocketIO (`pip install eventlet`)

### 2. **Clonar o Repositório**

```bash
git clone https://github.com/SeuUsuario/nome-do-repositorio.git
cd nome-do-repositorio
```

### 3. **Executar o Servidor**

Certifique-se de que você tenha as dependências instaladas e execute o seguinte comando para iniciar o servidor:

```bash
python app.py
```

O servidor será iniciado e os dados dos carrinhos começarão a ser exibidos na interface.

## Público-Alvo

Este projeto foi idealizado para:

- **Jovens e Estudantes**: Incentivar o interesse em **tecnologia**, **automobilismo** e **sustentabilidade**.
- **Pessoas com Deficiência Sensorial**: Proporcionar uma experiência de automobilismo mais inclusiva, com foco em **baixa emissão de ruído**, ideal para pessoas no **espectro autista**.

## Autores

Este projeto foi desenvolvido por:

- **Abner de Paiva Barbosa** | RM558468
- **Beatriz Vieira de Novais** | RM554746
- **Fernando Luiz Silva Antonio** | RM555201
- **Mariana Neugebauer Dourado** | RM550494
- **Thomas de Almeida Reichmann** | RM554812

## Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).

