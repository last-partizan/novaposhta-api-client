"""
python -m novaposhta.tests
"""
import unittest

from .models import Address, InternetDocument, Counterparty

class TestAddress(unittest.TestCase):

    def test_get_cities(self):
        self.assertIsInstance(Address().get_cities(), list)
        self.assertIsInstance(Address().get_cities(find='Здолбунів'), list)


class TestInternetDocument(unittest.TestCase):

    def test_get_document_list(self):
        self.assertIsInstance(InternetDocument().get_document_list(), list)


class TestCounterparty(unittest.TestCase):

    def test_get_counterparties(self):
        self.assertIsInstance(Counterparty().get_counterparties(), list)


if __name__ == '__main__':
    unittest.main()
