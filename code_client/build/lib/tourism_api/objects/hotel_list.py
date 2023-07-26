from typing import List
from tourism_api.objects.hotel import Hotel
import pandas as pd

class HotelList:

    def __init__(self, hotels: List[Hotel]):
        self.values = hotels

    @property
    def values(self):
        return self.__values

    @values.setter
    def values(self, values):
        self.__values = values

    # initial method for obtaining data from the first csv.
    @staticmethod
    def pandas_to_cls(df_hotel):
        return HotelList.dicts_to_cls([row for idx, row in df_hotel.iterrows()], nested=False)

    # initial method for obtaining data from the first csv.
    @staticmethod
    def dicts_to_cls(hotels: List[dict], nested=True):
        hotels_list = []
        for h in hotels:
            hotels_list.append(
                Hotel.dict_to_cls(h, nested=nested)
            )
        return HotelList(hotels_list)

    def to_json(self) -> List[dict]:
        return [h.to_dict() for h in self.values]

    def cls_to_pandas(self):
        output = pd.DataFrame()
        output = output.append( [h.to_dict(nested=False) for h in self.values], ignore_index=True )
        return output

    def __repr__(self):
        return str([h for h in self.values])

