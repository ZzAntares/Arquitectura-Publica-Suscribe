import unittest
from Medicamento import Medicamento


class MedicamentoTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_single_instance(self):
        m = Medicamento('amoxicilina', '120mg', 6)
        self.assertEqual('Amoxicilina', m.name)
        self.assertEqual('120mg', m.dose)
        self.assertEqual(6, m.timer)

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
