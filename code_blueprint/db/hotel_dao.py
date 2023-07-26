from typing import List

from mongo import Collection

from db.mongo_db import MongoDb
from objects.hotel import Hotel
from objects.hotel_list import HotelList


class HotelDao:

    def __init__(self):
        db = MongoDb().db
        self.__hotels: Collection = db['hotels']

    def add_hotel(self, hotel: Hotel):
        print("check exists id insert:", hotel.hotel_id)
        print("result:",self.it_exists(hotel.hotel_id))
        if self.it_exists(hotel.hotel_id):
            print("400 db")
            return False
        data = hotel.to_dict()
        self.__hotels.insert_one(data)
        print("")
        return data

    def put_hotel(self, hotel: Hotel, id : int):
        data = hotel.to_dict()
        if self.it_exists(id):
            print("update:",data)
            filter = {'hotelId': HotelDao._parse_int(id)}
            newvalues = {"$set": data} #dict, need to be tested
            self.__hotels.update_one( filter, newvalues)
            print(self.get_hotel(id))
            return data
        print("Hotel Not Found")
        return False

    def get_hotel(self, hotel_id :int):
        print("id searching:", hotel_id)
        hotel = self.__hotels.find_one( {'hotelId': HotelDao._parse_int(hotel_id)})
        if hotel is not None:
            return Hotel.dict_to_cls(hotel)
        return False

    def delete_hotel(self, id):
        if self.it_exists(id):
            self.__hotels.delete_one({'hotelId': HotelDao._parse_int(id)})
            return True
        return False

    def it_exists(self, hotel_id : int):
        return self.__hotels.find_one({'hotelId': HotelDao._parse_int(hotel_id)})

    @staticmethod
    def _parse_int(value):
        if value is None:
            return None
        return int(value)

    def add_hotels(self, hotels):
        for h in hotels.values:
            self.add_hotel(h)

    #not directly implemented, used only internally.
    def _delete_hotels(self, condition):
        self.__hotels.delete_many({condition})

    def get_hotels(self, parameters : dict, sort_by :str=None, direction :int=1):
        if sort_by is None:
            return HotelList.dicts_to_cls( list( self.__hotels.find( parameters )))

        return HotelList.dicts_to_cls(list(self.__hotels.find(parameters).sort(sort_by, direction)))

    def get_hotels_by_range(self, parameter : str, start : float=None, end : float=None, sort_by :str=None, direction :int=1):
        rng_filter = {}
        if start is not None:
            rng_filter.update({'$gte': float(start)})
        if end is not None:
            rng_filter.update({'$lte': float(end)})
        if sort_by is None:

            return HotelList.dicts_to_cls(
                list( self.__hotels.find( {parameter: rng_filter} ) ) )
        return HotelList.dicts_to_cls( list( self.__hotels.find({parameter:rng_filter}).sort(sort_by, direction)))


hd = HotelDao()
h_l1 = hd.get_hotels_by_range("price",sort_by='price', start=1000)
print(h_l1)