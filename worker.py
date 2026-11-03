"""Consome e processa pedidos da fila file_pedidos."""

import time

import pika

QUEUE_NAME = "file_pedidos"


def processar_pedido(ch, method, properties, body) -> None:
    mensagem_recebida = body.decode("utf-8")
    print(f" [x] Recebido: {mensagem_recebida}")

    # Cada ponto no texto representa um segundo de processamento.
    tempo_processamento = mensagem_recebida.count(".")
    print(f" [x] Iniciando processamento de: {mensagem_recebida}")
    time.sleep(tempo_processamento)
    print(f" [x] Finalizado processamento de: {mensagem_recebida}")

    # Confirma a mensagem somente depois de concluir o processamento.
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main() -> None:
    parametros = pika.ConnectionParameters(host="localhost")
    connection = pika.BlockingConnection(parametros)
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=processar_pedido,
    )

    print(" [*] Aguardando pedidos. Para sair pressione CTRL+C")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\n [!] Worker encerrado.")
        channel.stop_consuming()
    finally:
        if connection.is_open:
            connection.close()


if __name__ == "__main__":
    main()
