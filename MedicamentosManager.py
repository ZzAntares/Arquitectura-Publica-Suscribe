#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import pika
from prettytable import PrettyTable
from Medicamento import Medicamento
from SignosVitales import SignosVitales


class MedicamentosManager:

    def __init__(self):
        """Constructor.

        Carga una lista de medicamentos predeterminada para utilizar
        en el sistema y los almacena en una tabla.
        """
        meds = Medicamento.create_batch([
            'paracetamol',
            'ibuprofeno',
            'insulina',
            'furosemida',
            'piroxicam',
            'tolbutamida',
        ], '1 Píldora 120mg', 8)

        # Build table
        medtable = PrettyTable([
            'Medicamentos suministrados',
            'Dosis',
            'Temporizador',
            'Pacientes',
        ])

        for med in meds.values():
            medtable.add_row(
                [med.name, med.dose, med.timer, len(med.patients)])

        self.medtable = medtable
        self.meddict = meds
        self.patients = {}

    def print_report(self):
        """Imprime un reporte de los medicamentos disponibles.
        """
        table = PrettyTable(['CONFIGURACIÓN DE LA SIMULACIÓN'])
        table.add_row(['Grupos de medicamentos | 6'])
        print(table)
        print(self.medtable)

    def create_medicament(self, title=None):
        """Dar de alta un nuevo medicamento de manera interactiva.

        Args:
            title (str): Título a utilizar en la tabla usada para preguntar
                los datos al cliente, es variable por que si se desea crear
                más un medicamento el titulo puede contener un contador.
        """
        if not title:
            title = 'DATOS DEL MEDICAMENTO'

        table = PrettyTable([title])
        table.add_row(['NOMBRE | ?'])
        print(table)
        name = raw_input('escribe el nombre: ')

        table = PrettyTable(['NOMBRE', name.capitalize()])
        table.add_row(['DOSIS', '?'])
        print(table)
        dose = raw_input('escribe la dósis (ej. "Tableta 500mg"): ')

        table = PrettyTable(['DOSIS', dose])
        table.add_row(['TEMPORIZADOR', '?'])
        print(table)
        timer = raw_input(
            'Cada cuantas horas se receta? (número entero): ')

        # Update medicaments table
        med = Medicamento(name, dose, timer)
        self.meddict[name] = med

        self.medtable.add_row([
            med.name,
            med.dose,
            med.timer,
            len(med.patients)
        ])

    def input_new_medicaments(self):
        """Dar de alta multiples medicamentos de manera interactiva.
        """
        table = PrettyTable(['CONFIGURACIÓN DE LA SIMULACIÓN'])
        table.add_row(['¿Cuántos nuevos medicamentos agregarás? | ?'])
        print(table)
        meds = raw_input('número entero: ')

        for i in xrange(0, int(meds)):
            title = 'DATOS DEL MEDICAMENTO #%s' % (i + 1)
            self.create_medicament(title)

    def configure(self):
        """Inicia el proceso de configuración para el caso que se deseen
        registrar nuevos medicamentos en el sistema.
        """
        print_report = False

        while True:
            choice = raw_input('¿Deseas agregar más medicamentos? [s/n]: ')
            choice.lower()

            if not (choice.startswith('y') or choice.startswith('s')):
                break  # End configuration process

            print_report = True  # Since new meds were added, show the medtable
            self.input_new_medicaments()

        if print_report:
            self.print_report()

    def read_medgroup(self):
        """Solicita el nombre del medicamento a suministrar a un paciente y
        valida que dicho medicamento exista.

        Returns:
            str: Nombre del medicamento existente a suministrar.
        """
        while True:
            print(self.medtable)

            group = raw_input(
                'escribe el nombre del medicamento a suministrar al paciente: '
            )

            if group.lower() in self.meddict:
                # He chooses a valid medicine group
                return group.lower()

            print(PrettyTable(
                ['ERROR: Medicamento "%s" no esta en la lista!' % (group)]))

            print('La selección no es válida. Intentalo de nuevo.')

    def add_patient_to_medgroup(self, name):
        """Inicia interacción para recetar medicamento a paciente.

        Args:
            name (str): Paciente al que se desea recetar un medicamento.
        """
        # Relate patient to med
        medgroup = self.read_medgroup()
        medicament = self.meddict[medgroup]
        medicament.add_patient(name)

        # Relate med to patient
        self.patients[name.capitalize()] = medicament

    def get_meds_with_patients(self):
        """Obtiene los grupos de medicamentos que tienen asociados pacientes.

        Returns:
            list: Lista con medicamentos donde solo aparecen aquellos
                que tienen pacientes asociados.
        """
        return [med for med in self.meddict.values() if med.patients]

    def get_med_for_patient(self, name):
        """A partir de un paciente obtiene el medicamento que consume.

        Args:
            name (str): Nombre del paciente al cual obtener su medicamento.

        Returns:
            object: Instancia de Medicamento que corresponde a su medicamento.
        """
        return self.patients[name.capitalize()]

    def setUpManager(self, medicament):
        """Configura el medicamento que se desea monitorear.
        """
        self.medicament = medicament

    def start_consuming(self):
        """Inicia el servicio que consume las notificaciones
        de prescripción de medicamentos.
        """
        self.values_parameters = sys.argv[1] if len(sys.argv) > 1 else None
        self.setUpManager(self.values_parameters)
        # +--------------------------------------------------------------------------------------+
        # | La siguiente linea permite realizar la conexión con el servidor que aloja a RabbitMQ |
        # +--------------------------------------------------------------------------------------+
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))
        channel = connection.channel()
        # +----------------------------------------------------------------------------------------+
        # | La siguiente linea permite definir el tipo de intercambio y de que cola recibirá datos |
        # +----------------------------------------------------------------------------------------+
        channel.exchange_declare(exchange='direct_temporizador',
                                 type='direct')
        result = channel.queue_declare(exclusive=True)
        queue_name = result.method.queue
        severity = 'temporizador'
        # +----------------------------------------------------------------------------+
        # | La siguiente linea permite realizar la conexión con la cola que se definió |
        # +----------------------------------------------------------------------------+
        channel.queue_bind(exchange='direct_temporizador',
                            queue=queue_name, routing_key=severity)
        print(' [*] Inicio de monitoreo de temporizador. Presiona CTRL+C para finalizar el monitoreo')
        # +----------------------------------------------------------------------------------------+
        # | La siguiente linea permite definir las acciones que se realizarán al ocurrir un método |
        # +----------------------------------------------------------------------------------------+
        channel.basic_consume(self.callback,
                              queue=queue_name,
                              no_ack=True)
        channel.start_consuming()

    def callback(self, ch, method, properties, body):
        """Envía al monitor las notificaciones recibidas.

        Si al ejecutar el manager se especificó un medicamento entonces el
        monitor solo recibirá notificaciones para dicho medicamento (grupo).
        """
        values = body.split(':')
        event = str(values[3]).capitalize()

        monitor = SignosVitales()
        notification = PrettyTable([str(values[2]), event, str(values[4])])

        if self.medicament and event != self.medicament.capitalize():
            # No se suscribió a este medicamento (no se notifica)
            return

        monitor.print_notification(notification)


if __name__ == '__main__':
    test = MedicamentosManager()
    test.start_consuming()
