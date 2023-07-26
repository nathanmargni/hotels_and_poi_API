from tourism_api.objects.address import Address
import pytest

class AddressTest:

    def address_country_getter_test(self):
        expected_val = "A"
        address_instance = Address( country="A" )
        assert address_instance.stars == expected_val

    def address_country_setter_test(self):
        expected_val = "A"
        address_instance = Address()
        address_instance.country = "A"
        assert address_instance.country == expected_val

    def address_country_code_getter_test(self):
        expected_val = "A"
        address_instance = Address( code="A" )
        assert address_instance.country_code == expected_val

    def address_country_code_setter_test(self):
        expected_val = "A"
        address_instance = Address()
        address_instance.country_code = "A"
        assert address_instance.country_code == expected_val

    def address_city_getter_test(self):
        expected_val = "A"
        address_instance = Address( city="A" )
        assert address_instance.city == expected_val

    def address_city_setter_test(self):
        expected_val = "A"
        address_instance = Address()
        address_instance.city = "A"
        assert address_instance.city == expected_val

    def address_street_getter_test(self):
        expected_val = "A"
        address_instance = Address( street="A" )
        assert address_instance.street == expected_val

    def address_street_setter_test(self):
        expected_val = "A"
        address_instance = Address()
        address_instance.street = "A"
        assert address_instance.street == expected_val

    def address_test_init(self):
        country = 'Switzerland'
        code = "CH"
        city = "Lugano"
        street = "Via Stazione 44"
        address_instance = Address( country=country, code=code,
                           city=city, street=street )
        assert address_instance.country == country
        assert address_instance.country_code == code
        assert address_instance.city == city
        assert address_instance.street == street

    def address_test_init2(self):

        address_instance = Address()
        assert address_instance.country == 'Switzerland'
        assert address_instance.country_code is None
        assert address_instance.city is None
        assert address_instance.street is None

    def address_to_dict_test(self):
        country = 'Switzerland'
        code = "CH"
        city = "Lugano"
        street = "Via Stazione 44"
        address_instance = Address( country=country, code=code,
                           city=city, street=street )

        dict_instance = address_instance.to_dict()

        assert address_instance.country == dict_instance['countryName'] and \
               address_instance.country_code == dict_instance['countryCode'] and \
               address_instance.city == dict_instance['cityName'] and \
               address_instance.street == dict_instance['street']
