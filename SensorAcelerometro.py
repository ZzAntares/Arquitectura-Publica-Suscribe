#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import pika


class SensorAcelerometro():
    nombre = None
    id = 0

    def __init__(self, nombre):
        self.nombre = nombre
        self.id = int(self.set_id())

    def set_id(self):
        return random.randint(1000, 5000)

    def get_name(self):
        return self.nombre

    def start_service(self):
        #   +--------------------------------------------------------------------------------------+
        #   | La siguiente linea permite realizar la conexión con el servidor que aloja a RabbitMQ |
        #   +--------------------------------------------------------------------------------------+
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        #   +----------------------------------------------------------------------------------------+
        #   | La siguiente linea permite definir el tipo de intercambio y de que cola recibirá datos |
        #   +----------------------------------------------------------------------------------------+
        channel.exchange_declare(exchange='direct_acelerometro', type='direct')
        severity = 'posicion'
        valores_generados_x = self.simulate_data()
        valores_generados_y = self.simulate_data()
        valores_generados_z = self.simulate_data()
        mensaje = 'POSICION:' + str(self.id) + ':' + self.nombre + \
            ':' + str(valores_generados_x) + ':' + str(valores_generados_y) + ':' + str(valores_generados_z)
        #   +----------------------------------------------------------------------------+
        #   | La siguiente linea permite enviar datos a la cola seleccionada.            |
        #   +----------------------------------------------------------------------------+
        channel.basic_publish(exchange='direct_acelerometro',
                              routing_key=severity, body=mensaje)
        print('+---------------+--------------------+-------------------------------+-------+')
        print('|      ' + str(self.id) +'     |     ' + self.nombre +'     |      POSICIÓN ENVIADA      |  ' + str(valores_generados_x) + '  | ' + str(valores_generados_y) + '  | ' + str(valores_generados_z) + '   |')
        print('+---------------+--------------------+-------------------------------+-------+')
        print('')
        connection.close()

    def simulate_data(self):
        return random.uniform(-0.999, 0.999)
