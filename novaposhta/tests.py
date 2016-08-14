"""
python -m novaposhta.tests
python -m novaposhta.tests TestInternetDocument.test_get_document_list
"""
import unittest
import logging

from novaposhta.models import Address, InternetDocument, Counterparty, ContactPerson

class TestAddress(unittest.TestCase):

    def test_get_cities(self):
        self.assertIsInstance(Address.get_cities(), list)
        self.assertIsInstance(Address.get_cities(find='Здолбунів'), list)


class TestInternetDocument(unittest.TestCase):

    def test_get_document_list(self):
        self.assertIsInstance(InternetDocument.get_document_list(), list)

    def notest_save(self):
        InternetDocument.save()


class TestCounterparty(unittest.TestCase):
    data = {
        "CityRef": "db5c88d7-391c-11dd-90d9-001a92567626",
        "FirstName": "Фелікс",
        "MiddleName": "Едуардович",
        "LastName": "Яковлєв",
        "Phone": "0997979789",
        "Email": "",
        "CounterpartyType": "PrivatePerson",
        "CounterpartyProperty": "Recipient"
    }

    def test_get_counterparties(self):
        self.assertIsInstance(Counterparty.get_counterparties(), list)

    def test_save(self):
        cp = Counterparty(**self.data).save()
        self.assertIsInstance(cp, Counterparty)
        self.assertIsInstance(cp.ContactPerson, ContactPerson)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
