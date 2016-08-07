"""
python -m novaposhta.tests
python -m novaposhta.tests TestInternetDocument.test_get_document_list
"""
import unittest
import logging

from .models import Address, InternetDocument, Counterparty

class TestAddress(unittest.TestCase):

    def test_get_cities(self):
        self.assertIsInstance(Address().get_cities(), list)
        self.assertIsInstance(Address().get_cities(find='Здолбунів'), list)


class TestInternetDocument(unittest.TestCase):

    def test_get_document_list(self):
        self.assertIsInstance(InternetDocument().get_document_list(), list)

    def test_save(self):
        InternetDocument().save()


class TestCounterparty(unittest.TestCase):

    def test_get_counterparties(self):
        self.assertIsInstance(Counterparty().get_counterparties(), list)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
