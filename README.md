# Atividade prática — Mensageria com RabbitMQ

Projeto desenvolvido a partir do minicurso **Mensageria com RabbitMQ**, demonstrando uma fila de trabalho com produtor, múltiplos workers, mensagens persistentes, confirmação manual (ACK) e distribuição de carga.

## Pré-requisitos

- Docker instalado e em execução.
- Python 3.10 ou superior.
- `pip` disponível no ambiente Python.

## 1. Iniciar o RabbitMQ

Execute:

```bash
docker run -d --name rabbitmq-server -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

Acesse a interface de gerenciamento em <http://localhost:15672> usando:

- Usuário: `guest`
- Senha: `guest`

Se já existir um contêiner com esse nome, use `docker start rabbitmq-server` ou remova o anterior com `docker rm -f rabbitmq-server` antes de executar o comando acima.

## 2. Instalar a dependência

É recomendado usar um ambiente virtual:

```bash
python -m venv .venv
```

No Linux/macOS:

```bash
source .venv/bin/activate
```

No Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Instale o `pika`:

```bash
python -m pip install -r requirements.txt
```

## 3. Executar os workers

Abra dois terminais na pasta do projeto. Em cada um, execute:

```bash
python worker.py
```

Os dois processos consumirão mensagens da fila `file_pedidos`. O `prefetch_count=1` limita cada worker a uma mensagem não confirmada por vez, favorecendo o balanceamento entre workers.

## 4. Publicar pedidos

Em outro terminal:

```bash
python produtor.py "Pedido A .."
python produtor.py "Pedido B ..."
```

Cada ponto simula um segundo de processamento. Também é possível publicar a mensagem padrão:

```bash
python produtor.py
```

Na interface do RabbitMQ, observe a fila `file_pedidos`, o número de mensagens e os consumidores conectados.

## Conceitos demonstrados

- **Fila durável:** a fila `file_pedidos` é declarada com `durable=True`.
- **Mensagem persistente:** as mensagens são publicadas com `delivery_mode=2`.
- **ACK manual:** o worker confirma a mensagem somente depois do processamento.
- **Concorrência:** vários workers podem consumir a mesma fila.
- **Prefetch:** cada worker recebe uma mensagem por vez.
- **Default exchange:** o envio usa `exchange=""` e o nome da fila como `routing_key`.

## Encerramento

Para parar os workers, pressione `Ctrl+C`. Para parar e remover o RabbitMQ:

```bash
docker rm -f rabbitmq-server
```
