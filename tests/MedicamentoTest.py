import unittest
from Medicamento import Medicamento


class MedicamentoTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_single_instance(self):
        m = Medicamento('amoxicilina', 6)
        self.assertEqual('Amoxicilina', m.name)

    def test_create_batch(self):
        meds = ['penicilina', 'amoxicilina', 'naproxeno']
        medicines = Medicamento.create_batch(meds, 4)

        self.assertEqual(3, len(medicines))

        for med in medicines:
            self.assertEqual(4, med.dose)
            self.assertEqual(0, len(med.patients))
            self.assertIsInstance(med, Medicamento)
