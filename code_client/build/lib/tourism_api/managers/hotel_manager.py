import json
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import gmplot
import pandas as pd

from tourism_api.objects.hotel import Hotel
from tourism_api.objects.hotel_list import HotelList
class HotelManager:

    def __init__(self):
        pass

    @staticmethod
    def get_hotels(params=None,sort_by=None, direction=1):
        if params is None:
            params = {}
        if sort_by is not None:
            params['sort_by'] = ('-' if direction == -1 else "+") + sort_by
        url = 'http://127.0.0.1:5000/hotels/'
        session = requests.Session()
        retry = Retry( connect=3, backoff_factor=0.5 )
        adapter = HTTPAdapter( max_retries=retry )
        session.mount( 'http://', adapter )
        session.mount( 'https://', adapter )
        response = session.get( url, params=params)
        return HotelList.dicts_to_cls(response.json())

    @classmethod
    def get_hotels_by_country(cls,country : str, sort_by=None, direction=1):
        return cls.get_hotels( {'address.countryName':country},sort_by, direction)

    @classmethod
    def get_hotels_by_city(cls, city : str, sort_by=None, direction=1):
        return cls.get_hotels({'address.cityName': city}, sort_by, direction)

    @classmethod
    def get_hotel_by_name(cls, name: str, sort_by=None, direction=1):
        return cls.get_hotels({'hotelName': name}, sort_by, direction )

    @classmethod
    def get_hotels_by_stars_range(cls, start=None, end=None, sort_by=None, direction=1, params=None):
        if params is None:
            params = {}
        params['start'] = start
        params['end'] = end
        params['between'] = 'stars'
        return cls.get_hotels(params ,sort_by, direction)


    @classmethod
    def get_hotels_by_price_range(cls, start=None, end=None, sort_by=None, direction=1, params=None):
        if params is None:
            params = {}
        params['start'] = start
        params['end'] = end
        params['between'] = 'price'
        return cls.get_hotels(params,sort_by, direction )

    @staticmethod
    def add_hotel(hotel : Hotel):
        url = f'http://127.0.0.1:5000/hotels/'
        session = requests.Session()
        retry = Retry( connect=3, backoff_factor=0.5 )
        adapter = HTTPAdapter( max_retries=retry )
        session.mount( 'http://', adapter )
        session.mount( 'https://', adapter )
        response = session.post( url, json=json.dumps( hotel.to_dict() ), timeout=5 )
        return response.text

    @staticmethod
    def update_hotel(hotel : Hotel):
        url = f'http://127.0.0.1:5000/hotels/{hotel.hotel_id}'
        session = requests.Session()
        retry = Retry( connect=3, backoff_factor=0.5 )
        adapter = HTTPAdapter( max_retries=retry )
        session.mount( 'http://', adapter )
        session.mount( 'https://', adapter )
        response = session.put( url, json=json.dumps( hotel.to_dict() ), timeout=5 )
        return response.text


    @staticmethod
    def get_hotel_by_id(hotel_id : int):
        url = f'http://127.0.0.1:5000/hotels/{hotel_id}'
        session = requests.Session()
        retry = Retry( connect=3, backoff_factor=0.5 )
        adapter = HTTPAdapter( max_retries=retry )
        session.mount( 'http://', adapter )
        session.mount( 'https://', adapter )
        response = session.get( url )
        if "error" in response.json().keys():
            return response.json()["error"]
        else:
            return Hotel.dict_to_cls(response.json())


    @staticmethod
    def delete_hotel_by_id(hotel_id : int):
        url = f'http://127.0.0.1:5000/hotels/{hotel_id}'
        session = requests.Session()
        retry = Retry( connect=3, backoff_factor=0.5 )
        adapter = HTTPAdapter( max_retries=retry )
        session.mount( 'http://', adapter )
        session.mount( 'https://', adapter )
        response = session.delete( url, timeout=5 )
        return response.text


    @staticmethod
    def save_map(hotellist: HotelList, filename: str=None, get_string = False):

        df = hotellist.cls_to_pandas()
        lat = 46.8
        lon = 8.3

        apikey = "AIzaSyDyj9f9lYTrfwqrs0vdMNtmgCU2cnH9h4Y"
        map_styles = [{"featureType": "poi", "stylers": [{"Visibility": "off"}]}]
        gmap = gmplot.GoogleMapPlotter(lat, lon,8, radius=40, scale_control=False, apikey=apikey, title="Hotels")

        for i, row in df.iterrows():
            gmap.marker(row['latitude'], row['longitude'], title=row["hotelName"], info_window=" Name: " +
                                row["hotelName"] + " stars: " + str(row["stars"]) + " price: " + str(row["price"]))

        if filename is None or  get_string is True:
            return gmap.get()
        else:
            gmap.draw(filename)


if __name__ == '__main__':

    HotelManager.save_map(hotellist=HotelManager.get_hotels(), filename="map.html")