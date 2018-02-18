"""
export NOVAPOSHTA_API_KEY="your test api key"
python -m novaposhta.tests
python -m novaposhta.tests TestInternetDocument.test_get_document_list
"""
import sys
import os
from datetime import datetime

import unittest
import logging

from novaposhta import models

logger = logging.getLogger(__name__)


def setUpModule():
    sys.setrecursionlimit(140)
    if not models.Model.api.api_key:
        raise RuntimeError("NOVAPOSHTA_API_KEY env is not set")
    print("Using NOVAPOSHTA_API_KEY='%s'" % models.Model.api.api_key)


class TestAddress(unittest.TestCase):

    def test_get_cities(self):
        self.assertIsInstance(models.Address.get_cities(), list)
        self.assertIsInstance(models.Address.get_cities(find='Здолбунів'), list)


class TestInternetDocument(unittest.TestCase):

    def test_get_document_list(self):
        self.assertIsInstance(models.InternetDocument.get_document_list(), list)


class TestAdditionalService(unittest.TestCase):

    def create_recipient(self):
        return models.Counterparty(**{
            "CityRef": "db5c88d7-391c-11dd-90d9-001a92567626",
            "CounterpartyProperty": "Recipient",
            "CounterpartyType": "PrivatePerson",
            "FirstName": "Тест",
            "LastName": "Тест",
            "Phone": "380631112223",
        }).save()

    def create_test_document(self):
        cp = models.Counterparty.get_counterparties()[0]
        contact = models.Counterparty.get_counterparty_contact_persons(cp.Ref)[0]
        recipient = self.create_recipient()
        data = {
            "PayerType": "Sender",
            "PaymentMethod": "Cash",
            "DateTime": datetime.now().strftime("%d.%m.%Y"),
            "CargoType": "Cargo",
            "VolumeGeneral": "0.1",
            "Weight": "10",
            "ServiceType": "WarehouseDoors",
            "SeatsAmount": "1",
            "Description": "абажур",
            "Cost": "500",

            "CitySender": "8d5a980d-391c-11dd-90d9-001a92567626",
            "Sender": cp.Ref,
            "SenderAddress": "01ae2635-e1c2-11e3-8c4a-0050568002cf",
            "ContactSender": contact.Ref,
            "SendersPhone": "380678734567",

            "CityRecipient": "db5c8892-391c-11dd-90d9-001a92567626",
            "Recipient": recipient.Ref,
            "RecipientAddress": "511fcfbd-e1c2-11e3-8c4a-0050568002cf",
            "ContactRecipient": recipient.ContactPerson.Ref,
            "RecipientsPhone": "380631112223"
        }
        return models.InternetDocument(**data).save()

    @unittest.skipUnless("NOVAPOSHTA_TEST_DOC_NUMBER" in os.environ, "NOVAPOSHTA_TEST_DOC_NUMBER env variable is not set")
    def test_return(self):
        test_id = os.environ["NOVAPOSHTA_TEST_DOC_NUMBER"]
        location = models.AdditionalService.check_possibility_create_return(
            test_id,
        )[0]
        resp = models.ReturnRequest(
            IntDocNumber=test_id,
            PaymentMethod="Cash",
            Reason="7d07b1de-1d6d-11e4-acce-0050568002cf",
            SubtypeReason="faaeb2b9-1d6d-11e4-acce-0050568002cf",
            Note="Тест запроса возврата",
            ReturnAddressRef=location.Ref,
        ).save()
        models.AdditionalService.delete(resp.Ref)

    def test_get_return_reasons(self):
        reasons = models.AdditionalService.get_return_reasons()
        self.assertGreaterEqual(len(reasons), 1)
        subtypes = models.AdditionalService.get_return_reason_subtypes(
            reasons[0].Ref,
        )
        self.assertGreaterEqual(len(subtypes), 1)

    def test_get_return_orders_list(self):
        self.assertIsInstance(
            models.AdditionalService.get_return_orders_list(),
            list,
        )


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
        self.assertIsInstance(models.Counterparty.get_counterparties(), list)

    def test_save(self):
        cp = models.Counterparty(**self.data).save()
        self.assertIsInstance(cp, models.Counterparty)
        self.assertIsInstance(cp.ContactPerson, models.ContactPerson)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
