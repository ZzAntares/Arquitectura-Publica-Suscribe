# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------
# Archivo: Medicamento.py
# Capitulo: 3 Estilo Publica-Subscribe
# Autor(es): Karina Chaires, Arturo Lagunas, Julio Gutiérrez
# Version: Marzo 2017
# Descripción:
#
#   Ésta clase encapsula el concepto de Medicamento, gestionando
#   los pacientes a los que se le receta dicha fórmula.
#
#   Las características de ésta clase son las siguientes:
#
#   Responsabilidades:
#       - Añadir nuevos medicamentos de manera sencilla.
#       - Registrar nuevos pacientes como consumidores de un medicamento.
#
#  En cada una de las funciones se encuentra documentado su responsabilidad,
#  argumentos y parámetros que cada una de ellas reciben.
#
# -----------------------------------------------------------------------------


class Medicamento:

    def __init__(self, name, dose, timer):
        """Constructor.

        Instancía un nuevo medicamento con la información dada.

        Args:
            name (str): Nombre del medicamento.
            dose (str): Cuanto se debe consumir del medicamento.
            timer (int): Cantidad de horas entre cada dosis.
        """
        self.name = name.capitalize()
        self.dose = dose
        self.timer = int(timer)
        self.patients = []

    @staticmethod
    def create_batch(medicaments, dose, timer):
        """Crea instancias de la clase 'Medicamento' en masa.

        A partir de los medicamentos proporcionados en forma de lista
        instancía objetos de la clase Medicamento con la dósis específicada.

        Args:
            medicaments (list): Lista de cadenas, cada una es un medicamento.
            dose (str): Dósis en la cual se administran los medicamentos.
            timer (int): Numero de horas entre dósis.

        Returns:
            dict: Diccionario donde la llave es el nombre del medicamento,
                y el valor es una instancia de la clase Medicamento.
        """
        meds = {}

        for medicine in medicaments:
            meds[medicine] = Medicamento(medicine, dose, timer)

        return meds

    def add_patient(self, name):
        """ Agrega un paciente al grupo del medicamento.

        Args:
            name (str): Nombre del paciente que recibirá el medicamento.
        """
        self.patients.append(name)
