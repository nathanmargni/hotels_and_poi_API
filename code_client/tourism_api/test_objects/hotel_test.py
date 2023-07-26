from tourism_api.objects.place import Place
from tourism_api.objects.position import Position
from tourism_api.objects.address import Address
import pandas as pd
from tourism_api.objects.hotel import Hotel
import pytest


class HotelTest():

    def hotel_id_getter_test(self):
        expected_id = 1
        hotel_instance = Hotel(id=1)
        assert hotel_instance.hotel_id == expected_id

    def hotel_id_setter_test(self):
        expected_id = 2
        hotel_instance = Hotel(id=1)
        hotel_instance.hotel_id = 2
        assert hotel_instance.hotel_id == expected_id

    def hotel_name_getter_test(self):
        expected_name ="A"
        hotel_instance = Hotel( id=1, name="A" )
        assert hotel_instance.name == expected_name

    def hotel_name_setter_test(self):
        expected_name ="B"
        hotel_instance = Hotel( id=1 )
        hotel_instance.name = "B"
        assert hotel_instance.name == expected_name

    def hotel_stars_getter_test(self):
        expected_val =3
        hotel_instance = Hotel( id=1, stars=3 )
        assert hotel_instance.stars == expected_val

    def hotel_stars_setter_test(self):
        expected_stars =4.9
        hotel_instance = Hotel( id=1)
        hotel_instance.stars = 4.9
        assert hotel_instance.stars == expected_stars

    def hotel_stars_setter2_test(self):
        hotel_instance = Hotel( id=1)
        hotel_instance.name = 7
        assert hotel_instance.stars is None

    def hotel_stars_setter3_test(self):
        hotel_instance = Hotel( id=1)
        hotel_instance.name = -2
        assert hotel_instance.stars is None

    def hotel_price_getter_test(self):
        expected_val = 30
        hotel_instance = Hotel( id=1, price=30 )
        assert hotel_instance.stars == expected_val

    def hotel_price_setter_test(self):
        expected_val = 51
        hotel_instance = Hotel( id=1 )
        hotel_instance.price = 51
        assert hotel_instance.price == expected_val

    def hotel_price_setter2_test(self):
        hotel_instance = Hotel( id=1 )
        hotel_instance.price = -7
        assert hotel_instance.price is None


    def hotel_test_init(self):
        country = 'Switzerland'
        code = "CH"
        city = "Lugano"
        street = "Via Stazione 44"
        latitude = 67.12
        longitude = 43.1
        hotel_id = 1
        name = "hotelName"
        stars = 3.4
        price = 400
        address = Address( country=country, code=code,
                                    city=city, street= street)
        position = Position( latitude=latitude, longitude=longitude )

        hotel_instance = Hotel( id=hotel_id, name=name, stars=stars, price=price,
                   address=address, position=position)

        assert hotel_instance.hotel_id == hotel_id
        assert hotel_instance.name == name
        assert hotel_instance.stars == stars
        assert hotel_instance.price == price
        assert hotel_instance.address.country == country and \
               hotel_instance.address.country_code == code and \
               hotel_instance.address.city == city and \
               hotel_instance.address.street == street
        assert hotel_instance.position.longitude == longitude and \
               hotel_instance.position.latitude == latitude


    def hotel_test_init2(self):
        hotel_id = 1
        hotel_instance = Hotel(id=hotel_id)
        assert hotel_instance.hotel_id == hotel_id
        assert hotel_instance.name is None
        assert hotel_instance.stars is None
        assert hotel_instance.price is None
        assert hotel_instance.address.country is None and \
               hotel_instance.address.country_code is None and \
               hotel_instance.address.city is None and \
               hotel_instance.address.street is None
        assert hotel_instance.position.longitude is None and \
               hotel_instance.position.latitude is None

    def hotel_test_init3(self):
        country = 'Switzerland'
        code = "CH"
        city = "Lugano"
        street = "Via Stazione 44"
        latitude = 67.12
        longitude = 43.1
        hotel_id = 1
        name = "hotelName"
        stars = 34
        price = -4
        address = Address( country=country, code=code,
                                    city=city, street= street)
        position = Position( latitude=latitude, longitude=longitude )

        hotel_instance = Hotel( id=hotel_id, name=name, stars=stars, price=price,
                   address=address, position=position)

        assert hotel_instance.hotel_id == hotel_id
        assert hotel_instance.name == name
        assert hotel_instance.stars is None
        assert hotel_instance.price is None
        assert hotel_instance.address.country == country and \
               hotel_instance.address.country_code == code and \
               hotel_instance.address.city == city and \
               hotel_instance.address.street == street
        assert hotel_instance.position.longitude == longitude and \
               hotel_instance.position.latitude == latitude

    def hotel_to_dict_plain_test(self):
        country = 'Switzerland'
        code = "CH"
        city = "Lugano"
        street = "Via Stazione 44"
        latitude = 67.12
        longitude = 43.1
        hotel_id = 1
        name = "hotelName"
        stars = 34
        price = -4
        address = Address( country=country, code=code,
                           city=city, street=street )
        position = Position( latitude=latitude, longitude=longitude )

        hotel_instance = Hotel( id=hotel_id, name=name, stars=stars, price=price,
                                address=address, position=position )
        dict_instance = hotel_instance.to_dict(nested=False)
        assert hotel_instance.hotel_id == dict_instance['hotelId']
        assert hotel_instance.name == dict_instance['hotelName']
        assert hotel_instance.stars == dict_instance['stars']
        assert hotel_instance.price == dict_instance['price']
        assert hotel_instance.address.country == dict_instance['countryName'] and \
               hotel_instance.address.country_code == dict_instance['countryCode'] and \
               hotel_instance.address.city == dict_instance['cityName'] and \
               hotel_instance.address.street == dict_instance['street']
        assert hotel_instance.position.longitude == dict_instance['latitude'] and \
               hotel_instance.position.latitude == dict_instance['longitude']

    def hotel_to_dict_nested_test(self):
        country = 'Switzerland'
        code = "CH"
        city = "Lugano"
        street = "Via Stazione 44"
        latitude = 67.12
        longitude = 43.1
        hotel_id = 1
        name = "hotelName"
        stars = 34
        price = -4
        address = Address( country=country, code=code,
                           city=city, street=street )
        position = Position( latitude=latitude, longitude=longitude )

        hotel_instance = Hotel( id=hotel_id, name=name, stars=stars, price=price,
                                address=address, position=position )
        dict_instance = hotel_instance.to_dict( nested=True )
        assert hotel_instance.hotel_id == dict_instance['hotelId']
        assert hotel_instance.name == dict_instance['hotelName']
        assert hotel_instance.stars == dict_instance['stars']
        assert hotel_instance.price == dict_instance['price']
        assert hotel_instance.address.country == dict_instance['address']['countryName'] and \
               hotel_instance.address.country_code == dict_instance['address']['countryCode'] and \
               hotel_instance.address.city == dict_instance['address']['cityName'] and \
               hotel_instance.address.street == dict_instance['address']['street']
        assert hotel_instance.position.longitude == dict_instance['position']['latitude'] and \
               hotel_instance.position.latitude == dict_instance['position']['longitude']

    def hotel_dict_to_cls(self):
        pass