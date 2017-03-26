# -*- coding: utf-8 -*-
class Medicamento:

    def __init__(self, name, dose):
        self.name = name.capitalize()
        self.dose = int(dose)
        self.patients = []

    @staticmethod
    def create_batch(medicaments, dose):
        """Crea instancias de la clase 'Medicamento' en masa.

        A partir de los medicamentos proporcionados en forma de lista
        instancía objetos de la clase Medicamento con la dósis específicada.

        Args:
            medicaments (list): Lista de cadenas, cada una es un medicamento.
            dose (int): Dósis en la cual se administran los medicamentos.

        Returns:
            list: Lista de objetos, cada elemento es una instancia de
                la clase Medicamento.
        """
        meds = []

        for medicine in medicaments:
            meds.append(Medicamento(medicine, dose))

        return meds
