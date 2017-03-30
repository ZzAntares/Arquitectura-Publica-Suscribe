import unittest
from Medicamento import Medicamento


class MedicamentoTest(unittest.TestCase):

    def setUp(self):
        self.med = Medicamento('amoxicilina', '120mg', 6)

    def tearDown(self):
        pass

    def test_single_instance(self):
        self.assertEqual('Amoxicilina', self.med.name)
        self.assertEqual('120mg', self.med.dose)
        self.assertEqual(6, self.med.timer)

    def test_create_batch(self):
        meds = ['penicilina', 'amoxicilina', 'naproxeno']
        medicines = Medicamento.create_batch(meds, 'Pildoras 60mg', 4)

        self.assertIsInstance(medicines, dict)
        self.assertEqual(3, len(medicines.items()))

        for k, med in medicines.items():
            self.assertIsInstance(med, Medicamento)
            self.assertEqual(4, med.timer)
            self.assertEqual('Pildoras 60mg', med.dose)
            self.assertEqual(0, len(med.patients))

            self.assertEqual(k, med.name.lower())

    def test_add_patient(self):
        self.med.add_patient('Doyle')
        self.assertEqual(self.med.patients, ['Doyle'])

        self.med.add_patient('Jane')
        self.assertEqual(len(self.med.patients), 2)
        self.assertIn('Jane', self.med.patients)
