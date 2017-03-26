# -*- coding: utf-8 -*-
from prettytable import PrettyTable
from Medicamento import Medicamento


class MedicamentosManager:

    def __init__(self):
        self.medicaments = Medicamento.create_batch([
            'paracetamol',
            'ibuprofeno',
            'insulina',
            'furosemida',
            'piroxicam',
            'tolbutamida',
        ], 8)

    def configure(self):
        table = PrettyTable(['CONFIGURACIÓN DE LA SIMULACIÓN'])
        table.add_row(['Grupos de medicamentos | 6'])
        print(table)

        # Build current medicines table
        self.medtable = PrettyTable(
            ['Grupos de medicamentos', 'Dosis', 'Pacientes'])

        for med in self.medicaments:
            self.medtable.add_row([med.name, med.dose, len(med.patients)])

        while True:
            print(self.medtable)

            choice = raw_input('¿Deseas agregar más medicamentos? [s/n]: ')
            choice.lower()

            if not (choice.startswith('y') or choice.startswith('s')):
                # End configuration process
                break

            # Ask for new meds
            table = PrettyTable(['CONFIGURACIÓN DE LA SIMULACIÓN'])
            table.add_row(['¿Cuántos nuevos medicamentos agregarás? | ?'])
            print(table)
            meds = raw_input('número entero: ')

            for i in xrange(1, int(meds) + 1):
                table = PrettyTable(['DATOS DEL MEDICAMENTO #%s' % i])
                table.add_row(['NOMBRE | ?'])
                print(table)
                name = raw_input('escribe el nombre: ')

                table = PrettyTable(['NOMBRE', name.capitalize()])
                table.add_row(['DOSIS', '?'])
                print(table)
                dose = raw_input('número entero (horas): ')

                # Update managed medicaments
                med = Medicamento(name, dose)
                self.medicaments.append(med)

                # Update medicaments table
                self.medtable.add_row([med.name, med.dose, len(med.patients)])
