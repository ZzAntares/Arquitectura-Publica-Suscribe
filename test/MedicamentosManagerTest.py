# -*- coding: utf-8 -*-
import unittest
import __builtin__
from mock import patch
from io import BytesIO as StringIO
from MedicamentosManager import MedicamentosManager


class MedicamentosManagerTest(unittest.TestCase):

    def setUp(self):
        self.meds = MedicamentosManager()

    def test_default_medicines(self):
        self.assertIsNotNone(self.meds.medtable)

    def test_report(self):
        with patch('sys.stdout', new=StringIO()) as output:
            self.meds.print_report()
            output = output.getvalue().strip()

            self.assertIn('CONFIGURACIÓN DE LA SIMULACIÓN', output)
            meds = ['Paracetamol', 'Ibuprofeno', 'Insulina',
                    'Furosemida', 'Piroxicam', 'Tolbutamida']

            for med in meds:
                self.assertIn(med, output)

    @patch.object(__builtin__, 'raw_input')
    @patch('MedicamentosManager.PrettyTable.add_row')
    def test_create_medicament(self, mock_add_row, mock_input):
        mock_input.side_effects = ['penicilina', '120mg', 6]

        with patch('sys.stdout', new=StringIO()) as output:
            self.meds.create_medicament()
            output = output.getvalue().strip()

            self.assertIn('DATOS DEL MEDICAMENTO', output)
            mock_add_row.assert_called()

    @patch.object(__builtin__, 'raw_input')
    @patch('MedicamentosManager.MedicamentosManager.create_medicament')
    def test_input_new_medicaments(self, mock_create_medicament, mock_input):
        mock_input.return_value = '2'

        with patch('sys.stdout', new=StringIO()):
            self.meds.input_new_medicaments()
            self.assertEqual(len(mock_create_medicament.mock_calls), 2)

    def test_add_patient_to_medgroup(self):
        self.medicamentos.add_patient_to_medgroup('Doyle')
        pass
