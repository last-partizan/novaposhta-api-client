# coding: utf-8
from .api import queries

class NovaPoshtaApi(object):
    """A base API class, that holds shared methods and settings for other models.
    Creates basic query object and provide `apiKey` and API endpoint configuration.
    """
    # api path for testapi
    test_url = "{format}/{cls}/{method}/"

    def __init__(self, **params):
        self.__dict__.update(params)

    def __repr__(self):
        return "<{}: {}>".format(self.__class__.__name__, str(self))

    @classmethod
    def send(cls, method=None, method_props=None, test_url=None):
        """
        Primary method for API requests and data fetching.
        It uses `urllib2` and `json` libs for requests to API through `HTTP` protocol.
        Modifies API template and then makes request to API endpoint.

        :param method:
            name of the API method, should be passed for every request
        :type method:
            str or unicode
        :param method_props:
            additional params for API methods.
        :type method_props:
            dict
        :return:
            dictionary with fetched info
        :rtype:
            dict
        """
        return queries.send(cls, method, method_props, test_url)


class Address(NovaPoshtaApi):
    """A class representing the `Address` model of Nova Poshta API.
    Used for parsing `geodata` (like cities, streets etc.).
    """
    test_url="{format}/Address/{method}"

    def __str__(self):
        return self.Description

    @classmethod
    def get_cities(cls, find=None):
        """
        Method for fetching info about all cities.

        :example:
            ``address = Address()``
            ``address.get_cities()``
            ``address.get_cities(find='Здолбунів')``
        :return:
            list(dictionary)
        :rtype:
            list
        """
        props = {} if not find else {'FindByString': find}
        return cls.send(method='getCities', method_props=props)

    @classmethod
    def get_streets(cls, city_ref, find=None):
        """
        Method for fetching info about streets in desired city.

        :example:
            ``address = Address()``
            ``address.get_streets(city_ref='0006560c-4079-11de-b509-001d92f78698')``
            ``address.get_streets(city_ref='0006560c-4079-11de-b509-001d92f78698', find='Незалежності')``
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
            ``address = Address()``
            ``address.get_warehouses(city='0006560c-4079-11de-b509-001d92f78698')``
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
            ``address = Address()``
            ``address.get_warehouse_types()``
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
            ``address = Address()``
            ``address.get_areas()``
        :return:
            parsed dictionary with info about areas
        :rtype:
            dict
        """
        return cls.send(method='getAreas')

    @classmethod
    def save(cls, from_data=None, cp_ref=None, str_ref=None, build_num=None, flat=None, note=None):
        """
        Method for saving counterparty's address

        :example:
            ``address = Address()``
            ``address.save(cp_ref='5953fb16-08d8-11e4-8958-0025909b4e33',``
            ``str_ref='d8364179-4149-11dd-9198-001d60451983', build_num='20',``
            ``flat='10')``
            or:
            ``address = Address()``
            ``data = {
            ``        cp_ref='5953fb16-08d8-11e4-8958-0025909b4e33',``
            ``        str_ref='d8364179-4149-11dd-9198-001d60451983',
            ``        build_num='20',``
            ``        flat='10'}``
            ``address.save(from_data=data)``
        :param from_data:
            dictionary with all required data, will be used instead of passing each keyword separately
        :type from_data:
            dict
        :param cp_ref:
            ID of the counterparty
        :type cp_ref:
            str or unicode
        :param str_ref:
            ID of the street
        :type str_ref:
            str or unicode
        :param build_num:
            building number
        :type build_num:
            str or unicode
        :param flat:
            flat number
        :type flat:
            str or unicode
        :param note:
            comment
        :type:
            str or unicode
        :return:
            dictionary with info about saved address
        :rtype:
             dict
        """
        if from_data:
            props = from_data
        else:
            props = {
                'CounterpartyRef': cp_ref,
                'StreetRef': str_ref,
                'BuildingNumber': build_num,
                'Flat': flat,
                'Note': note
            }
        return cls.send(method='save', method_props=props)

    @classmethod
    def update(cls, from_data=None, cp_ref=None, add_ref=None, str_ref=None, build_num=None, flat=None, note=None):
        """
        Method for updating counterparty's address

        :param from_data:
            dictionary with all required data, will be used instead of passing each keyword separately
        :type from_data:
            dict
        :param cp_ref:
            ID of the counterparty
        :type cp_ref:
            str or unicode
        :param add_ref:
            ID of the address, that need to be updated
        :type add_ref:
            str or unicode
        :param str_ref:
            ID of the street
        :type str_ref:
            str or unicode
        :param build_num:
            building number
        :type build_num:
            str or unicode
        :param flat:
            flat number
        :type flat:
            str or unicode
        :param note:
            comment
        :type:
            str or unicode
        :return:
            dictionary with info about saved address
        :rtype:
             dict
        """
        if from_data:
            props = from_data
        else:
            props = {
                'CounterpartyRef': cp_ref,
                'Ref': add_ref,
                'StreetRef': str_ref,
                'BuildingNumber': build_num,
                'Flat': flat,
                'Note': note
            }
        return cls.send(method='update', method_props=props)

    @classmethod
    def delete(cls, add_ref):
        """
        Method for deleting saved address
        :param add_ref:
            ID of the address, that need to be deleted
        :type add_ref:
            str or unicode
        :return:
            dict with info about deleted address

        """
        props = {
            'Ref': add_ref
        }
        return cls.send(method='delete', method_props=props)


class Counterparty(NovaPoshtaApi):
    """
    A class representing the `Counterparty` model of Nova Poshta API.
    Used for interact with counterpart's info.
    """
    test_url = "Counterparty/{format}/{method}/"

    @classmethod
    def get_counterparties(cls, cp_type='Sender'):
        """
        Method for fetching all information about counterparties.

        :example:
            ``counterparty = Counterparty()``
            ``counterparty.get_counterparties(cp_type='Recipient')``
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
            ``counterparty = Counterparty()``
            ``counterparty.get_counterparties(name='Талісман', cp_type='Recipient')``
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
        req = cls.send(method='getCounterparties',
                        method_props={"CounterpartyProperty": cp_type, 'FindByString': name})
        return req

    @classmethod
    def get_counterparty_by_edrpou(cls, city_ref, code):
        """
        Method for fetching info about counterparty by `EDRPOU` - National State Registry
        of Ukrainian Enterprises and Organizations (8-digit code).

        :example:
            ``counterparty = Counterparty()``
            ``counterparty.get_counterparty_by_edrpou(city_ref='0006560c-4079-11de-b509-001d92f78698', code='12345678')``
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
        req = cls.send(method='getCounterpartyByEDRPOU', method_props={"CityRef": city_ref, 'EDRPOU': code})
        return req

    @classmethod
    def get_counterparty_addresses(cls, cp_ref, cp_type='Sender'):
        """
        Method for fetching counterparty's addresses.

        :example:
            ``counterparty = Counterparty()``
            ``counterparty.get_counterparty_addresses('f70f1bee-55fd-11e5-8d8d-005056887b8d', cp_type='Recipient')``
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
        req = cls.send(method='getCounterpartyAddresses',
                        method_props={'Ref': cp_ref, 'CounterpartyProperty': cp_type})
        return req

    @classmethod
    def get_counterparty_contact_persons(cls, cp_ref):
        """
        Method for fetching info about counterparty's contact persons.

        :example:
            ``counterparty = Counterparty()``
            ``counterparty.get_counterparty_contact_persons('f70f1bee-55fd-11e5-8d8d-005056887b8d')``
        :param cp_ref:
            name of the counterparty
        :type cp_ref:
            str or unicode
        :return:
            dictionary with info about counterparty's contact persons
        """
        req = cls.send(method='getCounterpartyContactPersons', method_props={'Ref': cp_ref})
        return req

    @classmethod
    def save(cls,  # TODO: Default values!
             from_data=None,
             city_ref=None,
             first_name=None,
             mid_name=None,
             last_name=None,
             phone=None, email=None,
             cp_type=None,
             cp_prop=None):
        """
        Method for saving counterparty.
        Named arguments can be used or it is possible to save pre-parsed dictionary with counterparty info.

        :example:
            ``counterparty = Counterparty()``
            ``counterparty.save(city_ref='db5c88d7-391c-11dd-90d9-001a92567626', first_name='Фелікс',``
            ``mid_name='Едуардович', last_name='Ковальчук', phone='0937979489',``
            ``email='myemail@my.com', cp_type='PrivatePerson', cp_prop='Recipient')``
            or:
            ``counterparty = Counterparty()``
            ``data = {``
            ``       'CityRef' : 'db5c88d7-391c-11dd-90d9-001a92567626',``
            ``       'CounterpartyProperty' : 'Recipient',``
            ``       'CounterpartyType' : 'PrivatePerson',``
            ``       'Email' : '',``
            ``       'FirstName' : 'Андрій',``
            ``       'LastName' : 'Яковлєв',``
            ``       'MiddleName' : 'Адуардович',``
            ``       'Phone' : '0997979789' }``
            ``counterparty.save(from_data=data)``

        :param from_data:
            dictionary with all required data, will be used instead of passing each keyword separately
        :param city_ref:
            ID of the counterparty's city
        :type city_ref:
            str or unicode
        :param first_name:
            first name of the counterparty
        :type:
            str or unicode
        :param mid_name:
            middle name of the counterparty
        :type:
            str or unicode
        :param last_name:
            last name of the counterparty
        :type:
            str or unicode
        :param phone:
            phone number of the counterparty
        :type:
            str or unicode
        :param email:
            e-mail address of the counterparty
        :type:
            str or unicode
        :param cp_type:
            type of the counterparty (`PrivatePerson` etc.)
        :type:
            str or unicode
        :param cp_prop:
            counterparty property (can be either `Sender` or `Recipient`)
        :type:
            str or unicode
        :return:
            dictionary with info about saved counterparty
        :rtype:
            dict
        """
        if from_data:
            props = from_data
        else:
            props = {
                'CityRef': city_ref,
                'FirstName': first_name,
                'MiddleName': mid_name,
                'LastName': last_name,
                'Phone': phone,
                'Email': email,
                'CounterpartyType': cp_type,
                'CounterpartyProperty': cp_prop
            }
        req = cls.send(method='save', method_props=props)
        return req

    # TODO: API requires all fields to be passed. Maybe we can pre-fetch data from API and use if no need to update it
    @classmethod
    def update(cls,
               from_data=None,
               cp_ref=None,
               city_ref=None,
               first_name=None,
               mid_name=None,
               last_name=None,
               phone=None,
               email=None,
               cp_type=None,
               cp_prop=None,
               own_form=None):
        """
        Method for updating counterparty. All fields are required
        Named arguments can be used or it is possible to update pre-parsed dictionary with counterparty info.

        :example:
            ``counterparty = Counterparty()``
            ``counterparty.update(ref='db5c88d7-391c-11dd-90d9-001a92567626',``
            ``city_ref='db5c88d7-391c-11dd-90d9-001a92567626', first_name='Фелікс',``
            ``mid_name='Едуардович', last_name='Ковальчук', phone='0937979489',``
            ``email='myemail@my.com', cp_type='PrivatePerson', cp_prop='Recipient', own_form='')``
            or:
            ``counterparty = Counterparty()``
            ``data = {'Ref': 'db5c88d7-391c-11dd-90d9-001a92567626',``
            ``       'CityRef' : 'db5c88d7-391c-11dd-90d9-001a92567626',``
            ``       'CounterpartyProperty' : 'Recipient',``
            ``       'CounterpartyType' : 'PrivatePerson',``
            ``       'Email' : '',``
            ``       'FirstName' : 'Андрій',``
            ``       'LastName' : 'Яковлєв',``
            ``       'MiddleName' : 'Едуардович',``
            ``       'Phone' : '0997979789',``
            ``       'OwnershipForm': '' }``
            ``counterparty.update(from_data=data)``

        :param from_data:
            dictionary with all required data, will be used instead of passing each keyword separately
        :type from_data:
            dict
        :param city_ref:
            ID of the counterparty's city
        :type city_ref:
            str or unicode
        :param first_name:
            first name of the counterparty
        :type:
            str or unicode
        :param mid_name:
            middle name of the counterparty
        :type:
            str or unicode
        :param last_name:
            last name of the counterparty
        :type:
            str or unicode
        :param phone:
            phone number of the counterparty
        :type:
            str or unicode
        :param email:
            e-mail address of the counterparty
        :type:
            str or unicode
        :param cp_type:
            type of the counterparty (`PrivatePerson` etc.)
        :type:
            str or unicode
        :param cp_prop:
            counterparty property (can be either `Sender` or `Recipient`)
        :type:
            str or unicode
        :param own_form:
            ownership form of the counterparty.
            if needed, `get_ownership_forms_list`method from Common class can be used to get possible values
        :type own_form:
            str or unicode
        :return:
            dictionary with info about saved counterparty
        :rtype:
            dict
        """
        if from_data:
            props = from_data
        else:
            props = {
                'Ref': cp_ref,
                'CityRef': city_ref,
                'FirstName': first_name,
                'MiddleName': mid_name,
                'LastName': last_name,
                'Phone': phone,
                'Email': email,
                'CounterpartyType': cp_type,
                'CounterpartyProperty': cp_prop,
                'OwnershipForm': own_form
            }
        req = cls.send(method='update', method_props=props)
        return req

    @classmethod
    def delete(cls, cp_ref):
        """
        Method for deleting counterparties.
        Due to restrictions, only `Recipient` counterparty type can be deleted.

        :example:
            ``counterparty = Counterparty()``
            ``counterparty.delete('342e8add-6953-11e5-ad08-005056801333')``
        :param cp_ref:
            ID of the counterparty
        :type cp_ref:
            str or unicode
        :return:
            dictionary with ID of deleted counterparty
        """
        req = cls.send(method='delete', method_props={'Ref': cp_ref})
        return req

    # @classmethod
    #def save_third_person(cls):
    #     """Not implemented due to contract lack, will be here in the future. Maybe :)"""
    #     return False

    @classmethod
    def get_counterparty_options(cls, cp_ref):
        """
        Method for getting counterparties options.

        :example:
            ``counterparty = Counterparty()``
            ``counterparty.get_counterparty_options('342e8add-6953-11e5-ad08-005056801333')``
        :param cp_ref:
            ID of the counterparty
        :type:
            str or unicode
        :return:
            dictionary with counterparty's options
        """
        req = cls.send(method='getCounterpartyOptions', method_props={'Ref': cp_ref})
        return req


class Common(NovaPoshtaApi):
    """A class representing the `Common` model of Nova Poshta API.
    Used for parsing common (obviously) information, which represents different data (cargo, payment etc.).
    """

    @classmethod
    def get_types_of_payers(cls):
        """
        Method for fetching info about types of payers.

        :example:
            ``common = Common()``
            ``common.get_types_of_payers()``
        :return:
            dictionary with info about types of payers
        """
        req = cls.send(method='getTypesOfPayers')
        return req

    @classmethod
    def get_payment_forms(cls):
        """
        Method for fetching info about possible payment forms.

        :example:
            ``common = Common()``
            ``common.get_payment_forms()``
        :return:
            dictionary with info about payment forms
        :rtype:
            dict
        """
        req = cls.send(method='getPaymentForms')
        return req

    @classmethod
    def get_cargo_types(cls):
        """
        Method for fetching info about cargo types.

        :example:
            ``common = Common()``
            ``common.get_cargo_types()``
        :return:
            dictionary with info about cargo types
        :rtype:
            dict
        """
        req = cls.send(method='getCargoTypes')
        return req

    @classmethod
    def get_service_types(cls):
        """
        Method for fetching info about possible delivery methods.

        :example:
            ``common = Common()``
            ``common.get_service_types()``
        :return:
            dictionary with info about possible delivery methods
        :rtype:
            dict
        """
        req = cls.send(method='getServiceTypes')
        return req

    @classmethod
    def get_cargo_description_list(cls):
        """
        Method for fetching the directory of cargo description.

        :example:
            ``common = Common()``
            ``common.get_cargo_description_list()``
        :return:
            dictionary with cargo descriptions
        :rtype:
            dict
        """
        req = cls.send(method='getCargoDescriptionList')
        return req

    @classmethod
    def search_cargo_description_list(cls, keyword):
        """
        Method for fetching cargo description by keyword.
        In general, it is extended version of `get_cargo_description_list` with `FindByString` API's methods param.
        :example:
            ``common = Common()``
            ``common.search_cargo_description_list('Абажур')``
        :param keyword:
            keyword for searching
        :type keyword:
            str or unicode
        :return:
            dictionary with cargo descriptions
        :rtype:
            dict
        """
        req = cls.send(method='getCargoDescriptionList', method_props={'FindByString': keyword})
        return req

    @classmethod
    def get_ownership_forms_list(cls):
        """
        Method for fetching info about ownership forms.

        :example:
            ``common = Common()``
            ``common.get_ownership_forms_list()``
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
            ``common = Common()``
            ``common.get_backward_delivery_cargo_types()``
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
            ``common = Common()``
            ``common.get_pallets_list()``
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
            ``common = Common()``
            ``common.get_type_of_counterparties()``
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
            ``common = Common()``
            ``common.get_type_of_payers_for_redelivery()``
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
        ``common = Common()``
        ``common.get_time_intervals(city_ref='udb5c896a-391c-11dd-90d9-001a92567626', datetime='2.10.2015')``
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
            ``common = Common()``
            ``common.get_tires_wheels_list()``
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
            ``common = Common()``
            ``common.get_trays_list()``
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
            ``common = Common()``
            ``common.get_document_statuses()``
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


class ContactPerson(NovaPoshtaApi):
    """A class representing the `ContactPerson` model of Nova Poshta API.
    Used for manipulating contact person data.
    :NOTE: All counterpart details must be only in Ukrainian.
    """

    @classmethod
    def save(cls, cp_ref=None, from_data=None, first_name=None, mid_name=None, last_name=None, phone=None):
        if from_data:
            props = from_data
        else:
            props = {
                'CounterpartyRef': cp_ref,
                'FirstName': first_name,
                'LastName': last_name,
                'MiddleName': mid_name,
                'Phone': phone,
            }
        req = cls.send(method='save', method_props=props)
        return req

    @classmethod
    def update(cls, cp_ref=None, ref=None, from_data=None, first_name=None, mid_name=None, last_name=None, phone=None):
        if from_data:
            props = from_data
        else:
            props = {
                'CounterpartyRef': cp_ref,
                'Ref': ref,
                'FirstName': first_name,
                'LastName': last_name,
                'MiddleName': mid_name,
                'Phone': phone,
            }
        req = cls.send(method='update', method_props=props)
        return req

    @classmethod
    def delete(cls, cp_ref=None):
        props = {
            'Ref': cp_ref
        }
        req = cls.send(method='delete', method_props=props)
        return req


class InternetDocument(NovaPoshtaApi):
    test_url="en/{method}/{format}/"

    @classmethod
    def get_document_list(cls, **kwargs):
        return cls.send(
            method='getDocumentList', method_props=kwargs,
            test_url="en/{format}/{method}/",
        )

    @classmethod
    def save(cls, **kwargs):
        return cls.send(method="save", method_props=kwargs)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
