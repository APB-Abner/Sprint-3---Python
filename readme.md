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
- **Conexão MQTT**: A comunicação entre o Arduino e o servidor é feita via MQTT, permitindo uma comunicação rápida e eficiente entre os dispositivos.
- **Server em Flask:** Mostra dados do carrinho, como distância, linha e velocidade.
- **Processamento de Dados**: O servidor recebe os dados dos sensores e atualiza uma interface em tempo real, possibilitando o acompanhamento remoto dos carrinhos.
- **Interface em Tempo Real**: Através do Flask e Socket.IO, os dados dos carrinhos são atualizados automaticamente em uma interface web, facilitando a interação e visualização.
- **Gráficos com `Chart.js`:** Exibe um gráfico em tempo real com os dados de velocidade ao longo do tempo.
- **Testes Automatizados:** Testes unitários para as principais funções da aplicação (conexão MQTT, recebimento de mensagens e processamento de dados).
  
## Estrutura do Projeto

Abaixo está a estrutura dos principais arquivos do projeto:

```
├── app.py               # Arquivo principal do Flask que gerencia as rotas e MQTT
├── test_app.py          # Testes automatizados usando unittest
├── templates/
│   └── index.html       # Template HTML do dashboard
└── README.md            # Documentação do projeto
```

### Arquivo `app.py`

O arquivo `app.py` contém a lógica do servidor Flask e a configuração do cliente MQTT. As principais funções incluem:

- `on_connect(client, userdata, flags, rc)`: Função chamada quando o cliente MQTT conecta ao broker.
- `on_message(client, userdata, msg)`: Função chamada quando uma mensagem MQTT é recebida.
- `processar_mensagem(topic, payload)`: Função para processar as mensagens recebidas do carrinho e atualizar os dados no dashboard.

### Arquivo `test_app.py`

O arquivo `test_app.py` contém os testes automatizados para garantir o correto funcionamento da aplicação. Os principais testes são:

- **Teste de conexão MQTT:** Verifica se a conexão com o broker é bem-sucedida e se as mensagens de erro são logadas corretamente em caso de falha.
- **Teste de processamento de mensagem:** Testa a função `processar_mensagem` para garantir que as mensagens do MQTT são processadas corretamente.
- **Integração entre Flask e MQTT:** Simula a publicação de mensagens MQTT e verifica se os dados são processados e exibidos corretamente no dashboard.

#### Exemplo de Testes:

```python
def test_on_connect_success(self):
    # Testa a conexão bem-sucedida ao broker MQTT (rc = 0)
    with patch('app.logging.info') as mock_log_info:
        on_connect(self.client, None, None, 0)
        mock_log_info.assert_called_with("Conexão bem-sucedida ao broker MQTT.")
```

O arquivo também contém testes para a página inicial do Flask e integração entre Flask e MQTT.

### Arquivo `templates/index.html`

O arquivo `templates/index.html` é o template que define a interface do dashboard do carrinho. Ele utiliza o Bootstrap para o layout e o `Chart.js` para a renderização do gráfico de velocidade.

- **Cards de Dados:** Exibe a distância, linha e velocidade do carrinho.
- **Gráfico de Velocidade:** Atualiza em tempo real com os dados recebidos via MQTT.

Exemplo de exibição de dados em tempo real:

```javascript
socket.on('atualizacao_dados', function (dados) {
    distanciaElement.innerText = dados.distancia;
    linhaElement.innerText = dados.linha;
    velocidadeElement.innerText = dados.velocidade;

    // Adiciona novos dados ao gráfico
    var agora = new Date().toLocaleTimeString();
    adicionarDadosAoGrafico(agora, dados.velocidade);
});
```


## Estrutura do Código

### 1. **Servidor Flask**

O servidor Flask lida com a lógica da aplicação, exibindo os dados recebidos dos carrinhos e se comunicando com o front-end via Socket.IO para atualizar a interface web em tempo real.

### 2. **Cliente MQTT**

O cliente MQTT é responsável por se conectar ao broker MQTT, assinar tópicos específicos (como distância, velocidade, linha), e processar as mensagens recebidas.

### 3. **Processamento de Mensagens**

As mensagens recebidas dos sensores dos carrinhos são processadas e armazenadas em variáveis globais. Em seguida, o servidor Flask emite eventos de atualização que são enviados para a interface web.

### 4. **Desconexão Segura**

O código inclui uma finalização apropriada, que garante que o cliente MQTT seja desconectado corretamente quando o servidor Flask for interrompido.

## **Utilizando**

### 1. **Dependências**

- **Python 3.x**
- Flask (`pip install flask`)
- Flask-SocketIO (`pip install flask-socketio`)
- Paho-MQTT (`pip install paho-mqtt`)
- Eventlet para melhorar o desempenho com Flask-SocketIO (`pip install eventlet`)
- Unittest (`pip install unittest`)

### 2. **Clonar o Repositório**

```bash
git clone https://github.com/APB-Abner/Sprint-3---Python.git
cd Sprint-3---Python
```


### 3. **Execute o servidor Flask:**
   ```bash
   python app.py
   ```

### 4. **Teste a aplicação:**
   Para rodar os testes automatizados, use:
   ```bash
   python test_app.py
   ```

### 5. **Acesse o Dashboard:**
   Abra o navegador e vá para `http://127.0.0.1:5000/` para ver o dashboard do carrinho.


## Testes

Os testes estão configurados no arquivo `test_app.py`, cobrindo:

- Conexão ao broker MQTT.
- Recebimento de mensagens MQTT.
- Processamento de mensagens no dashboard.
- Integração entre Flask e MQTT.
- Testes da interface Flask (acesso à página inicial e renderização correta).

Para executar os testes:

```bash
python -m unittest test_app.py
```

## Autores

Este projeto foi desenvolvido por:

- **Abner de Paiva Barbosa** | RM558468
- **Beatriz Vieira de Novais** | RM554746
- **Fernando Luiz Silva Antonio** | RM555201
- **Mariana Neugebauer Dourado** | RM550494
- **Thomas de Almeida Reichmann** | RM554812

## Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).




