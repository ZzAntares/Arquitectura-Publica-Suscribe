# -*- coding: utf-8 -*-
from prettytable import PrettyTable
from Medicamento import Medicamento


class MedicamentosManager:

    def __init__(self):
        """Constructor.

         Carga una lista de medicamentos predeterminada para utilizar
         en el sistema y los almacena en una tabla.
         """
        medlist = Medicamento.create_batch([
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

        for med in medlist:
            medtable.add_row(
                [med.name, med.dose, med.timer, len(med.patients)])

        self.medtable = medtable
        self.medlist = medlist

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
        self.medlist.append(med)

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
                break

