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

    @patch.object(__builtin__, 'raw_input')
    def test_read_medgroup_non_existent(self, mock_input):
        mock_input.return_value = 'Paracetamol'
        with patch('sys.stdout', new=StringIO()):
            self.assertEqual('paracetamol', self.meds.read_medgroup())

    @patch('MedicamentosManager.MedicamentosManager.read_medgroup')
    def test_add_patient_to_medgroup(self, mock_read):
        mock_read.return_value = 'paracetamol'
        self.meds.add_patient_to_medgroup('Doyle')

        # Doyle should appear as patient in 'paracetamol' group
        self.assertIn('Doyle', self.meds.meddict['paracetamol'].patients)
        self.assertIn('Doyle', self.meds.patients)
        self.assertEqual(
            self.meds.patients['Doyle'],
            self.meds.meddict['paracetamol']
        )

    def test_get_meds_with_patients(self):
        self.meds.meddict['paracetamol'].add_patient('Doyle')
        meds = self.meds.get_meds_with_patients()
        self.assertEqual('Paracetamol', meds[0].name)
        self.assertEqual(['Doyle'], meds[0].patients)

        self.meds.meddict['ibuprofeno'].add_patient('Jane')
        meds = self.meds.get_meds_with_patients()
        self.assertEqual(2, len(meds))

    @patch('MedicamentosManager.MedicamentosManager.read_medgroup')
    def test_get_med_for_patient(self, mock_read):
        mock_read.return_value = 'ibuprofeno'
        self.meds.add_patient_to_medgroup('Doyle')

        self.assertEqual(
            'Ibuprofeno',
            self.meds.get_med_for_patient('Doyle').name
        )
