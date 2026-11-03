"""Publica pedidos na fila file_pedidos."""

import sys

import pika

QUEUE_NAME = "file_pedidos"


def main() -> None:
    parametros = pika.ConnectionParameters(host="localhost")
    connection = pika.BlockingConnection(parametros)
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    message = " ".join(sys.argv[1:]) or "Pedido Padrao"
    channel.basic_publish(
        exchange="",
        routing_key=QUEUE_NAME,
        body=message.encode("utf-8"),
        properties=pika.BasicProperties(delivery_mode=2),
    )

    print(f" [x] Enviado para a fila: {message}")
    connection.close()


if __name__ == "__main__":
    main()
