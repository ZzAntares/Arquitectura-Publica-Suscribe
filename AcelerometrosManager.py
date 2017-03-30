# -*- coding: utf-8 -*-

import pika
import sys
from Acelerometro import Acelerometro

class AcelerometroManager:
    x = 0
    y = 0
    z = 0
    values_parameter_x = []

    def setUpManager(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def start_consuming(self):
        self.values_parameter_x = sys.argv[1]
        self.values_parameter_y = sys.argv[2]
        self.values_parameter_z = sys.argv[3]
        self.setUpManager(self.values_parameter_x, self.values_parameter_y, self.values_parameter_z)
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
        severity = 'posicion'
        #   +----------------------------------------------------------------------------+
        #   | La siguiente linea permite realizar la conexión con la cola que se definio |
        #   +----------------------------------------------------------------------------+
        channel.queue_bind(exchange='direct_acelerometro',
                            queue=queue_name, routing_key=severity)
        print(' [*] Inicio de monitoreo de posicion del adulto mayor. Presiona CTRL+C para finalizar el monitoreo')
        #   +----------------------------------------------------------------------------------------+
        #   | La siguiente linea permite definir las acciones que se realizarán al ocurrir un método |
        #   +----------------------------------------------------------------------------------------+
        channel.basic_consume(self.callback,
                              queue=queue_name,
                              no_ack=True)
        channel.start_consuming()

    def callback(self, ch, method, properties, body):
        values = body.split(':')
        x = int(values[3])
        y = int(values[4])
        z = int(values[5])
        monitor = Acelerometro()

        if (x >=-0.042 and x <= 0.599) and (y >= 0.690 and y <= 0.999) and (z >= 0.020 and z <= 0.783) :
            monitor.print_notification( 'CAIDA_LATERAL_DERECHA')
        elif (x >=-0.129 and x <= 0.536) and (y >= -0.171 and y <= 0.999) and (z >= -0.999 and z <= 0.999) :
            monitor.print_notification( 'CAIDA_FRONTAL')
        elif (x >=-0.236 and x <= 0.624) and (y >= -0.250 and y <= 0.999) and (z >= 0.525 and z <= 0.999) :
            monitor.print_notification( 'CAIDA_HACIA_ATRAS')
        elif (x >=-0.812 and x <= 0.171) and (y >= 0.080 and y <= 0.999) and (z >= -0.450 and z <= 0.999) :
            monitor.print_notification( 'CAIDA_LATERAL_IZQUIERDA')
        else:
            monitor.print_notification( 'OK')


test = AcelerometroManager()
test.start_consuming()
