from tourism_api.objects.place import Place
from tourism_api.objects.position import Position
from tourism_api.objects.address import Address
import pandas as pd


class Hotel( Place ):
    KEYS = {
        'hotelId': 'hotelId', 'name': 'hotelName', 'stars': 'stars', 'price': 'price',
        'address': Address.KEYS, 'position': Position.KEYS
    }

    _PRIMARY_KEY = []

    def __init__(self, id: int, name: str = None, stars: float=None, price: float=None, address: Address=None, position: Position=None):
        Place.__init__( self, address, position )
        self.hotel_id = id
        self.name = name
        self.stars = stars
        self.price = price

    @property
    def hotel_id(self):
        return self.__hotel_id

    @hotel_id.setter
    def hotel_id(self, value):
        self.__hotel_id = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def stars(self):
        return self.__stars

    @stars.setter
    def stars(self, value):
        if value is None:
            self.__stars = None
        else:
            self.__stars = value if value > 0 and value <=5 else None

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if value is None:
            self.__price = None
        else:
            self.__price = value if value > 0 else None

    def to_dict(self, nested = True):
        output = {Hotel.KEYS['hotelId']: self.hotel_id, Hotel.KEYS['name']: self.name,
                  Hotel.KEYS['stars']: self.stars,
                  Hotel.KEYS['price']: self.price}
        if nested:
            output['address'] = self.address.to_dict()
            output['position'] = self.position.to_dict()
        else:
            output.update( Address.to_dict( self.address ) )
            output.update( Position.to_dict( self.position ) )
        return output


    @classmethod
    def dict_to_cls(cls,hotel, nested=True):
        # Define if the list is nested stored and which level have to consider
        # for the field search.
        address_level = cls._nested_helper( hotel, "address", nested )
        position_level = cls._nested_helper( hotel, "position", nested )
        output = cls( id=cls._parse_int( hotel[cls.KEYS['hotelId']] ), name=hotel[cls.KEYS['name']],
                        stars=cls._parse_float( hotel[cls.KEYS['stars']] ), price=cls._parse_float( hotel[cls.KEYS['price']] ),
                        address=Address(
                            country=address_level[cls.KEYS['address']['countryName']],
                            code=address_level[cls.KEYS['address']['countryCode']],
                            city=address_level[cls.KEYS['address']['cityName']],
                            street=address_level[cls.KEYS['address']['street']]
                        ),
                        position=Position(
                            latitude=cls._parse_float( position_level[cls.KEYS['position']['latitude']] ),
                            longitude=cls._parse_float( position_level[cls.KEYS['position']['longitude']] ) )
                        )
        return output

    @staticmethod
    def _parse_int(value):
        if value is None:
            return None
        return int(value)

    @staticmethod
    def _parse_float(value):
        if value is None:
            return None
        return float(value)

    def cls_to_pandas(self):
        output = pd.DataFrame()
        output = output.append( self.to_dict(nested=False), ignore_index=True )
        return output

    @staticmethod
    def _nested_helper(hotel, field, nested):
        # hotel['address'] is for data stored in nested dictionaries (mongoDB), hotel is for plain database such csv.
        return hotel[field] if nested else hotel

    def __repr__(self) -> str:
        return str( self.to_dict() )
