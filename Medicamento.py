# -*- coding: utf-8 -*-
class Medicamento:

    def __init__(self, name, dose, timer):
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
            list: Lista de objetos, cada elemento es una instancia de
                la clase Medicamento.
        """
        meds = []

        for medicine in medicaments:
            meds.append(Medicamento(medicine, dose, timer))

        return meds
