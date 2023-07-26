class Address:
    KEYS = {'countryName': 'countryName', 'countryCode': 'countryCode', 'cityName': 'cityName',
            'street': 'street'}

    def __init__(self, country: str='Switzerland', city: str=None,code: str = None, street: str = None):
        self.country = country
        self.country_code = code
        self.city = city
        self.street = street

    @property
    def country(self) -> str:
        return self.__country

    @country.setter
    def country(self, value: str):
        self.__country = value

    @property
    def country_code(self) -> str:
        return self.__country_code

    @country_code.setter
    def country_code(self, value: str):
        self.__country_code = value

    @property
    def city(self) -> str:
        return self.__city

    @city.setter
    def city(self, value: str):
        self.__city = value

    @property
    def street(self) -> str:
        return self.__street

    @street.setter
    def street(self, value: str):
        self.__street = value

    def to_dict(self):
        return {
            Address.KEYS['countryName']: self.country,
            Address.KEYS['countryCode']: self.country_code,
            Address.KEYS['cityName']: self.city,
            Address.KEYS['street']: self.street
        }
