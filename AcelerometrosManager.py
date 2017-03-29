# -*- coding: utf-8 -*-

import pika
import sys
from Acelerometro import Acelerometro


class AcelerometroManager:
    x = 0
    y = 0
    z = 0
    status = ""
    values_parameters = 0

    def setUpManager(self, max):
        self.posicion_x = x
        self.posicion_y = y
        self.posicion_z = z

    def start_consuming(self):
        self.values_parameters = sys.argv[1]
        self.setUpManager(self.values_parameters)
        #   +--------------------------------------------------------------------------------------+
        #   | La siguiente linea permite realizar la conexión con el servidor que aloja a RabbitMQ |
        #   +--------------------------------------------------------------------------------------+
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))
        channel = connection.channel()
        #   +----------------------------------------------------------------------------------------+
        #   | La siguiente linea permite definir el tipo de intercambio y de que cola recibirá datos |
        #   +----------------------------------------------------------------------------------------+
        channel.exchange_declare(exchange='direct_acelerometro',
                                 type='direct')
        result = channel.queue_declare(exclusive=True)
        queue_name = result.method.queue
        severity = 'acelerometro'
        #   +----------------------------------------------------------------------------+
        #   | La siguiente linea permite realizar la conexión con la cola que se definio |
        #   +----------------------------------------------------------------------------+
        channel.queue_bind(exchange='direct_temperature',
                            queue=queue_name, routing_key=severity)
        print(' [*] Inicio de monitoreo de caidas. Presiona CTRL+C para finalizar el monitoreo')
        #   +----------------------------------------------------------------------------------------+
        #   | La siguiente linea permite definir las acciones que se realizarán al ocurrir un método |
        #   +----------------------------------------------------------------------------------------+
        channel.basic_consume(self.callback,
                              queue=queue_name,
                              no_ack=True)
        channel.start_consuming()

    def callback(self, ch, method, properties, body):
        values = body.split(':')
        valorx = int(values[3])
        valory = int(values[4])
        valorz = int(values[5])
        monitor = Acelerometro()
        sufrioUnaCaida = monitor.getEvento(valorx,valory,valorz)
        if event > int(self.temperatura_maxima):

            monitor.print_notification('+----------+-----------------------+----------+')
            monitor.print_notification('|   ' + str(values[3]) + '   |     TIENE CALENTURA   |   ' + str(values[2]) + '   |')
            monitor.print_notification('+----------+-----------------------+----------+')
            monitor.print_notification('')
            monitor.print_notification('')

test = AcelerometroManager()
test.start_consuming()
