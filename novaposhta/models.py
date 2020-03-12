# coding: utf-8
import attr

from .api import NovaPoshta
from .serializer import parse_datetime_universal, parse_date_dot, parse_datetime_dot


class Model(object):
    """
    Base model layer
    """
    # api path for testapi
    test_url = "{format}/{cls}/{method}/"
    api = NovaPoshta()

    convert_attrs = {}
    result_cls = {}

    def __init__(self, **params):
        for k, f in self.convert_attrs.items():
            try:
                params[k] = f(params[k])
            except (KeyError, IndexError):
                pass

        self.__dict__.update(params)

    @property
    def data(self):
        return self.__dict__

    def __repr__(self):
        return "<{}: {}>".format(self.__class__.__name__, str(self))

    def __str__(self):
        try:
            return self.Description
        except AttributeError:
            return "{} object".format(self.__class__.__name__)

    @classmethod
    def send(cls, method, method_props=None, test_url=None, raw=False):
        raw = cls.api.send(
            cls.api.build_url(cls, method, test_url or cls.test_url),
            getattr(cls, 'model_name', cls.__name__),
            method,
            method_props,
        )
        result_cls = cls.get_result_cls(method)

        if isinstance(raw, dict):
            return cls._convert(result_cls, raw)
        else:
            return [cls._convert(result_cls, attrs) for attrs in raw]

    @classmethod
    def get_result_cls(cls, method):
        return cls.result_cls.get(method, cls)

    @classmethod
    def _convert(cls, result_cls, data):
        try:
            return result_cls(**data)
        except TypeError:
            try:
                fields = [f.name for f in attr.fields(result_cls)]
                return result_cls(**{
                    k: v
                    for k, v in data.items() if k in fields
                })
            except TypeError:
                return attr.make_class("ApiResponse", list(data.keys()))(**data)


class BaseActions(object):

    def save(self):
        """Saving object"""
        return self.send(method='save', method_props=self.data)[0]

    def update(self):
        """Updating object"""
        return self.send(method='update', method_props=self.data)

    def delete(self):
        """Deleting objects"""
        return self.send(method='delete', method_props={'Ref': self.Ref})


@NovaPoshta.model
class Address(BaseActions, Model):
    """A class representing the `Address` model of Nova Poshta API.
    Used for parsing `geodata` (like cities, streets etc.).
    """
    test_url = "{format}/Address/{method}"

    @classmethod
    def get_cities(cls, find=None):
        """
        Method for fetching info about all cities.

        :example:
            ``Address.get_cities()``
            ``Address.get_cities(find='Здолбунів')``
        :return:
            list(dictionary)
        :rtype:
            list
        """
        return cls.send(method='getCities', method_props={'FindByString': find})

    @classmethod
    def get_streets(cls, city_ref, find=None):
        """
        Method for fetching info about streets in desired city.

        :example:
            ``Address.get_streets(city_ref='0006560c-4079-11de-b509-001d92f78698')``
            ``Address.get_streets(city_ref='0006560c-4079-11de-b509-001d92f78698', find='Незалежності')``
        :param city_ref:
            ID of the target city
        :type city_ref:
            str or unicode
        :param find:
            name of the target street
        :type street:
            str or unicode
        :return:
            list(dictionary)
        :rtype:
            list
        """
        props = {"CityRef": city_ref}
        if find:
            props["FindByString"] = find
        return cls.send(method='getStreet', method_props=props)

    @classmethod
    def get_warehouses(cls, city_ref):
        """
        Method for fetching info about all warehouses in desired city.

        :example:
            ``Address.get_warehouses(city='0006560c-4079-11de-b509-001d92f78698')``
        :param city_ref:
            ID of the target city
        :type city_ref:
            str or unicode
        :return:
            parsed dictionary with all info about warehouses
        :rtype:
            dict
        """
        return cls.send(
            method='getWarehouses', method_props={"CityRef": city_ref},
            test_url="{format}/AddressGeneral/{method}",
        )

    @classmethod
    def get_warehouse_types(cls):
        """
        Method for fetching info about warehouse's types.

        :example:
            ``Address.get_warehouse_types()``
        :return:
            parsed dictionary with info about warehouse's types
        :rtype:
            dict
        """
        return cls.send(method='getWarehouseTypes')

    @classmethod
    def get_areas(cls):
        """
        Method for fetching info about areas geographical areas.

        :example:
            ``Address.get_areas()``
        :return:
            parsed dictionary with info about areas
        :rtype:
            dict
        """
        return cls.send(method='getAreas')


@NovaPoshta.model
class ContactPerson(BaseActions, Model):
    """
    A class representing the `ContactPerson` model of Nova Poshta API.
    Used for manipulating contact person data.
    :NOTE: All counterpart details must be only in Ukrainian.
    """


@NovaPoshta.model
class Counterparty(BaseActions, Model):
    """
    A class representing the `Counterparty` model of Nova Poshta API.
    Used for interact with counterpart's info.
    """
    test_url = "Counterparty/{format}/{method}/"
    convert_attrs = {
        "ContactPerson": lambda data: ContactPerson(**data['data'][0]),
    }

    @classmethod
    def get_counterparties(cls, cp_type='Sender'):
        """
        Method for fetching all information about counterparties.

        :example:
            ``Counterparty.get_counterparties(cp_type='Recipient')``
        :param cp_type:
            type of the counterparty: can be either `Sender` or `Recipient` (`Sender` used as default)
        :type cp_type:
            str or unicode
        :return:
            dictionary with info about counterparties
        :rtype:
            dict
        """
        return cls.send(method='getCounterparties',
                        method_props={"CounterpartyProperty": cp_type})

    @classmethod
    def get_counterparty_by_name(cls, name, cp_type='Sender'):
        """
        Method for fetching info about counterparty by name.

        :example:
            ``Counterparty.get_counterparties(name='Талісман', cp_type='Recipient')``
        :param name:
            name of the desired counterparty
        :type name:
            str or unicode
        :param cp_type:
            type of the counterparty: can be either `Sender` or `Recipient` (`Sender` used as default)
        :type cp_type:
            str or unicode
        :return:
            dictionary with info about counterparty
        :rtype:
            dict
        """
        return cls.send(method='getCounterparties',
                        method_props={"CounterpartyProperty": cp_type, 'FindByString': name})

    @classmethod
    def get_counterparty_by_edrpou(cls, city_ref, code):
        """
        Method for fetching info about counterparty by `EDRPOU` - National State Registry
        of Ukrainian Enterprises and Organizations (8-digit code).

        :example:
            ``Counterparty.get_counterparty_by_edrpou(city_ref='0006560c-4079-11de-b509-001d92f78698', code='12345678')``
        :param city_ref:
            ID of the city of counterparty
        :type city_ref:
            str or unicode
        :param code:
            EDRPOU code of the counterparty
        :type code:
            str or unicode
        :return:
            dictionary with info about counterparty
        :rtype:
            dict
        """
        return cls.send(method='getCounterpartyByEDRPOU', method_props={"CityRef": city_ref, 'EDRPOU': code})

    @classmethod
    def get_counterparty_addresses(cls, cp_ref, cp_type='Sender'):
        """
        Method for fetching counterparty's addresses.

        :example:
            ``Counterparty.get_counterparty_addresses('f70f1bee-55fd-11e5-8d8d-005056887b8d', cp_type='Recipient')``
        :param cp_ref:
            ID of the counterparty
        :type cp_ref:
            str or unicode
        :param cp_type:
            type of the counterparty: can be either `Sender` or `Recipient` (`Sender` used as default)
        :type cp_type:
            str or unicode
        :return:
            dictionary with info about counterparty's addresses
        """
        return cls.send(method='getCounterpartyAddresses',
                        method_props={'Ref': cp_ref, 'CounterpartyProperty': cp_type})

    @classmethod
    def get_counterparty_contact_persons(cls, cp_ref):
        """
        Method for fetching info about counterparty's contact persons.

        :example:
            ``Counterparty.get_counterparty_contact_persons('f70f1bee-55fd-11e5-8d8d-005056887b8d')``
        :param cp_ref:
            name of the counterparty
        :type cp_ref:
            str or unicode
        :return:
            dictionary with info about counterparty's contact persons
        """
        return cls.send(method='getCounterpartyContactPersons', method_props={'Ref': cp_ref})

    # @classmethod
    # def save_third_person(cls):
    #     """Not implemented due to contract lack, will be here in the future. Maybe :)"""
    #     return False

    @classmethod
    def get_counterparty_options(cls, cp_ref):
        """
        Method for getting counterparties options.

        :example:
            ``Counterparty.get_counterparty_options('342e8add-6953-11e5-ad08-005056801333')``
        :param cp_ref:
            ID of the counterparty
        :type:
            str or unicode
        :return:
            dictionary with counterparty's options
        """
        return cls.send(method='getCounterpartyOptions', method_props={'Ref': cp_ref})


@NovaPoshta.model
class Common(Model):
    """A class representing the `Common` model of Nova Poshta API.
    Used for parsing common (obviously) information, which represents different data (cargo, payment etc.).
    """

    @classmethod
    def get_types_of_payers(cls):
        """
        Method for fetching info about types of payers.

        :example:
            ``Common.get_types_of_payers()``
        :return:
            dictionary with info about types of payers
        """
        return cls.send(method='getTypesOfPayers')

    @classmethod
    def get_payment_forms(cls):
        """
        Method for fetching info about possible payment forms.

        :example:
            ``Common.get_payment_forms()``
        :return:
            dictionary with info about payment forms
        :rtype:
            dict
        """
        return cls.send(method='getPaymentForms')

    @classmethod
    def get_cargo_types(cls):
        """
        Method for fetching info about cargo types.

        :example:
            ``Common.get_cargo_types()``
        :return:
            dictionary with info about cargo types
        :rtype:
            dict
        """
        return cls.send(method='getCargoTypes')

    @classmethod
    def get_service_types(cls):
        """
        Method for fetching info about possible delivery methods.

        :example:
            ``Common.get_service_types()``
        :return:
            dictionary with info about possible delivery methods
        :rtype:
            dict
        """
        req = cls.send(method='getServiceTypes')
        return req

    @classmethod
    def get_cargo_description_list(cls, q=None):
        """
        Method for fetching the directory of cargo description.

        :example:
            ``Common.get_cargo_description_list()``
            ``Common.get_cargo_description_list("Абажур")``
        :param q:
            keyword for searching
        :return:
            list(Common objects)
        :rtype:
            list
        """
        props = {'FindByString': q} if q else {}
        return cls.send(method='getCargoDescriptionList', method_props=props)

    @classmethod
    def get_ownership_forms_list(cls):
        """
        Method for fetching info about ownership forms.

        :example:
            ``Common.get_ownership_forms_list()``
        :return:
            dictionary with info about ownership forms
        :rtype:
            dict
        """
        req = cls.send(method='getOwnershipFormsList')
        return req

    @classmethod
    def get_backward_delivery_cargo_types(cls):
        """
        Method for fetching info about backward delivery cargo types.

        :example:
            ``Common.get_backward_delivery_cargo_types()``
        :return:
            Dictionary with info about backward delivery cargo types.
        :rtype:
            dict
        """
        req = cls.send(method='getBackwardDeliveryCargoTypes')
        return req

    @classmethod
    def get_pallets_list(cls):
        """
        Method for fetching info about pallets for backward delivery.

        :example:
            ``Common.get_pallets_list()``
        :return:
            dictionary with info about pallets
        :rtype:
            dict
        """
        req = cls.send(method='getPalletsList')
        return req

    @classmethod
    def get_type_of_counterparties(cls):
        """
        Method for fetching info about types of counterparties.

        :example:
            ``Common.get_type_of_counterparties()``
        :return:
            dictionary with info about types of counterparties
        :rtype:
            dict
        """
        req = cls.send(method='getTypesOfCounterparties')
        return req

    @classmethod
    def get_type_of_payers_for_redelivery(cls):
        """
        Method for fetching info about types of payers for redelivery.

        :example:
            ``Common.get_type_of_payers_for_redelivery()``
        :return:
            dictionary with info about types of payers for redelivery
        :rtype:
            dict
        """
        req = cls.send(method='getTypesOfPayersForRedelivery')
        return req

    @classmethod
    def get_time_intervals(cls, city_ref, datetime):
        """
        Method for fetching info about time intervals (for ordering "time intervals" service).

        :example:
        ``Common.get_time_intervals(city_ref='udb5c896a-391c-11dd-90d9-001a92567626', datetime='2.10.2015')``
        :param city_ref:
            ID of the recipient's city
        :param datetime:
            date for getting info about time intervals ('dd.mm.yyyy' date format)
        :return:
            dictionary with info about time intervals
        :rtype:
            dict
        """
        req = cls.send(method='getTimeIntervals', method_props={'RecipientCityRef': city_ref, 'DateTime': datetime})
        return req

    @classmethod
    def get_tires_wheels_list(cls):
        """
        Method for fetching info about tires and wheels (if cargo is "tires-wheels").

        :example:
            ``Common.get_tires_wheels_list()``
        :return:
            dictionary with info about tires and wheels
        :rtype:
            dict
        """
        req = cls.send(method='getTiresWheelsList')
        return req

    @classmethod
    def get_trays_list(cls):
        """
        Method for fetching info about trays (if backward delivery is ordered).

        :example:
            ``Common.get_trays_list()``
        :return:
            dictionary with info about trays
        :rtype:
            dict
        """
        req = cls.send(method='getTraysList')
        return req

    @classmethod
    def get_document_statuses(cls):
        """
        Method for fetching info about statuses of documents.

        :example:
            ``Common.get_document_statuses()``
        :return:
            dictionary with info about statuses of documents
        :rtype:
            dict
        """
        req = cls.send(method='getDocumentStatuses')
        return req

    @classmethod
    def get_document_status(cls, state_id=None, group_id=None, state_name=None):
        """
        Method for fetching info about status of one document.
        Can be filtered by several params (one or many).
        Since there is no default values, at least one filter should be used.

        :example:
            ``common = Common()``
            ``common.get_document_status(state_id='1')
            ``common.get_document_status(group_id='1')``
            ``common.get_document_status(group_id='1')
            ``common.get_document_status(state_name='Замовлення в обробці')
            ``common.get_document_status(group_id='1', state_name='Замовлення в обробці')

        :param state_id:
            numeric ID of document status
        :type state_id:
            str or unicode
        :param group_id:
            numeric group ID of document status
        :type state_name:
            str or unicode
        :param state_name:
            name of the status
        :type:
            str or unicode
        :return:
            dict with info about status of one document
        """
        filter_by = {
            'StateId': state_id,
            'GroupId': group_id,
            'StateName': state_name
        }
        req = cls.send(method='getDocumentStatuses', method_props=filter_by)
        return req


@attr.s
class SavedDocument(object):
    Ref = attr.ib()
    IntDocNumber = attr.ib()
    TypeDocument = attr.ib()
    CostOnSite = attr.ib(converter=float)
    EstimatedDeliveryDate = attr.ib(converter=parse_date_dot)


@NovaPoshta.model
class InternetDocument(BaseActions, Model):
    test_url = "en/{method}/{format}/"
    result_cls = {
        "save": SavedDocument,
    }

    @classmethod
    def get_document_list(cls, **kwargs):
        return cls.send(
            method='getDocumentList', method_props=kwargs,
            test_url="en/{format}/{method}/",
        )


@NovaPoshta.model
class TrackingDocument(Model):

    convert_attrs = {
        "RecipientDateTime": parse_datetime_dot,
        "ScheduledDeliveryDate": parse_datetime_universal,
    }

    @classmethod
    def get_status_documents(cls, documents, language="UA"):
        return cls.send(
            method='getStatusDocuments', method_props={
                'Documents': list(map(cls._prepare_doc, documents)),
                'Language': language,
            },
        )

    @classmethod
    def _prepare_doc(cls, obj):
        if isinstance(obj, tuple):
            return dict(zip(["DocumentNumber", "Phone"], obj))
        return obj


@attr.s
@NovaPoshta.model
class ReturnRequest(BaseActions, Model):
    IntDocNumber = attr.ib()
    PaymentMethod = attr.ib()
    Reason = attr.ib()
    SubtypeReason = attr.ib()
    ReturnAddressRef = attr.ib()
    Note = attr.ib(default="")
    OrderType = attr.ib(default="orderCargoReturn")

    model_name = "AdditionalService"


@NovaPoshta.model
class AdditionalService(Model):
    """
    Возврат посылок
    https://devcenter.novaposhta.ua/docs/services/58ad7185eea27006cc36d649/operations/58b6cd6aeea2700d141ccae1
    """

    @classmethod
    def check_possibility_create_return(cls, ref):
        return cls.send(
            method='CheckPossibilityCreateReturn', method_props={
                'Number': ref,
            },
        )

    @classmethod
    def get_return_reasons(cls):
        return cls.send(
            method='getReturnReasons',
        )

    @classmethod
    def get_return_reason_subtypes(cls, ref):
        return cls.send(
            method='getReturnReasonsSubtypes', method_props={
                'ReasonRef': ref,
            }
        )

    @classmethod
    def get_return_orders_list(cls, **kwargs):
        return cls.send(method='getReturnOrdersList', method_props=kwargs)

    @classmethod
    def delete(cls, ref):
        return cls.send(method='delete', method_props={"Ref": ref})
