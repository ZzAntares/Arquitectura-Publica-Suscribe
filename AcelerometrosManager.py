#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pika
import sys
from Acelerometro import Acelerometro

# -----------------------------------------------------------------------------
# Archivo: AcelerometrosManager.py
# Capitulo: 3 Estilo Publica-Subscribe
# Autor(es): Karina Chaires, Arturo Lagunas, Julio Gutiérrez
# Version: Marzo 2017
# Descripción:
#
#   Ésta clase define el rol de un subscriptor que consume los mensajes de
#   una cola específica.
#
#   Las características de ésta clase son las siguientes:
#
#                                AcelerometrosManager.py
#      +-----------------------+-------------------------+------------------------+
#      |  Nombre del elemento  |     Responsabilidad     |      Propiedades       |
#      +-----------------------+-------------------------+------------------------+
#      |                       |  - Recibir mensajes     |  - Se subscribe a la   |
#      |      Subscriptor      |  - Notificar al         |    cola de 'direct     |
#      |                       |    monitor.             |    acelerometro'       |
#      |                       |  - Filtrar valores      |  - Define rangos en    |
#      |                       |    de la fuerza de      |    los que los ejes    |
#      |                       |    aceleración de un    |    x,y,z son valores   |
#      |                       |    cuerpo en 3 ejes     |    válidos.            |
#      |                       |    x,y,z.               |                        |
#      |                       |                         |  - Notifica al monitor |
#      |                       |                         |    un segundo después  |
#      |                       |                         |    de recibir el       |
#      |                       |                         |    mensaje.            |
#      +-----------------------+-------------------------+------------------------+
#
#   A continuación se describen los métodos que se implementaron en ésta clase:
#
#                                             Métodos:
#           +------------------------+--------------------------+-----------------------+
#           |         Nombre         |        Parámetros        |        Función        |
#           +------------------------+--------------------------+-----------------------+
#           |                        |                          |  - Establece el valor |
#           |     setUpManager()     |         float: x         |    permitido para el  |
#           |                        |         float: y         |    acelerómetro.       |
#           |                        |         float: z         |                       |
#           +------------------------+--------------------------+-----------------------+
#           |                        |                          |  - Lee los argumentos |
#           |                        |                          |    con los que se e-  |
#           |                        |                          |    jecuta el programa |
#           |                        |                          |    para establecer el |
#           |                        |                          |    valor que puede    |
#           |                        |                          |    tomar el           |
#           |                        |                          |    acelerómetro       |
#           |   start_consuming()    |          None            |  - Realiza la conexi- |
#           |                        |                          |    ón con el servidor |
#           |                        |                          |    de RabbitMQ local. |
#           |                        |                          |  - Declara el tipo de |
#           |                        |                          |    tipo de intercam-  |
#           |                        |                          |    bio y a que cola   |
#           |                        |                          |    se va a subscribir.|
#           |                        |                          |  - Comienza a esperar |
#           |                        |                          |    los eventos.       |
#           +------------------------+--------------------------+-----------------------+
#           |                        |   ch: propio de Rabbit   |  - Contiene la lógica |
#           |                        | method: propio de Rabbit |    de negocio.        |
#           |       callback()       |   properties: propio de  |  - Se manda llamar    |
#           |                        |         RabbitMQ         |    cuando un evento   |
#           |                        |       String: body       |    ocurre.            |
#           +------------------------+--------------------------+-----------------------+
#
#           Nota: "propio de Rabbit" implica que se utilizan de manera interna para realizar
#            de manera correcta la recepcion de datos, para éste ejemplo no shubo necesidad
#            de utilizarlos y para evitar la sobrecarga de información se han omitido sus
#            detalles. Para más información acerca del funcionamiento interno de RabbitMQ
#            puedes visitar: https://www.rabbitmq.com/
#
#
#--------------------------------------------------------------------------------------------------

class AcelerometroManager:
    x = 0.0
    y = 0.0
    z = 0.0
    values_parameter_x = []
    values_parameter_y = []
    values_parameter_z = []

    def setUpManager(self, x, y, z):
        self.x = x #eje x
        self.y = y #eje y
        self.z = z #eje z

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
        x = float(values[3])
        y = float(values[4])
        z = float(values[5])
        monitor = Acelerometro()

        #Los acelerómetros registran el valor de la aceleración, medida en gs (1g equivale
        #a 9.8 ms2, la medida del valor de la gravedad en la Tierra) o directamente en ms2,
        #proporcionando una señal eléctrica para esta variación física.
        #rangos para cada una de los tipos de caídas de acuerdo a un estudio real.
        #fuente: Desarrollo de un sistema de detección de caídas basado en acelerómetros
        #http://eprints.ucm.es/38704/1/MemoriaTFG.pdf
        
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
