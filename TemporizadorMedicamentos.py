# -*- coding: utf-8 -*-
import random
import pika
from prettytable import PrettyTable


class TemporizadorMedicamentos:
    id = 0
    name = None
    medicamentos = None

    def __init__(self, name, medicaments_manager):
        """Constructor. Instancía el manejador del temporizador.

        Args:
            name (str): Nombre del paciente al cual pertenece el temporizador.
            medicaments_manager (object): Gestor de medicamentos.
        """
        self.name = name
        self.id = int(self.set_id())
        self.medicaments_manager = medicaments_manager
        self.medicaments_manager.add_patient_to_medgroup(name)

    def set_id(self):
        """Establece un ID aleatorio al temporizador.
        """
        return random.randint(1000, 5000)

    def get_name(self):
        """Obtiene el nombre del paciente asociado al temporizador.
        """
        return self.name

    def start_service(self):
        """Inicia el servicio que notifica si el paciente
        necesita tomar su medicamento.
        """
        # +--------------------------------------------------------------------+
        # | Si el temporizador no ha expirado, aún no es hora del medicamento. |
        # +--------------------------------------------------------------------+
        if not self.timer_expired():
            return
        # +--------------------------------------------------------------------------------------+
        # | La siguiente linea permite realizar la conexión con el servidor que aloja a RabbitMQ |
        # +--------------------------------------------------------------------------------------+
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        # +----------------------------------------------------------------------------------------+
        # | La siguiente linea permite definir el tipo de intercambio y de que cola recibirá datos |
        # +----------------------------------------------------------------------------------------+
        channel.exchange_declare(exchange='direct_temporizador', type='direct')
        severity = 'temporizador'
        medicamento = self.medicaments_manager.get_med_for_patient(self.name)
        mensaje = 'TMM:' + str(self.id) + ':' + self.name + \
            ':' + medicamento.name + ':' + medicamento.dose
        # +-----------------------------------------------------------------+
        # | La siguiente linea permite enviar datos a la cola seleccionada. |
        # +-----------------------------------------------------------------+
        channel.basic_publish(exchange='direct_temporizador',
                              routing_key=severity, body=mensaje)
        table = PrettyTable(
            [self.id, self.name, medicamento.name, medicamento.dose])
        print(table)
        print('')
        connection.close()

    def timer_expired(self):
        """Determina si el temporizador ha llegado a cero.

        Returns:
            bool: True si es hora de tomar el medicamento
                o False en caso contrario.
        """
        return self.simulate_data()

    def simulate_data(self):
        return random.random() < 0.3
