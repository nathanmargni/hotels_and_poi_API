from typing import List

import pandas as pd
from tourism_api.objects.position import Position
from tourism_api.objects.address import Address
from tourism_api.objects.point_of_interest import PointOfInterest


class PoiList:

    def __init__(self, pois: List[PointOfInterest]):
        self.values = pois

    @property
    def values(self):
        return self.__values

    @values.setter
    def values(self, values):
        self.__values = values

    # initial method for obtaining data from the first csv.
    @staticmethod
    def pandas_to_cls(df_pois):
        return PoiList.dicts_to_cls([row for idx, row in df_pois.iterrows()], nested=False)

    # initial method for obtaining data from the first csv.
    @staticmethod
    def dicts_to_cls(pois: List[dict], nested=True):
        pois_list = []
        for p in pois:
            pois_list.append(
                PointOfInterest.dict_to_cls(p, nested = nested)
            )
        return PoiList(pois_list)

    def to_json(self) -> List[dict]:
        return [h.to_dict() for h in self.values]

    def cls_to_pandas(self):
        output = pd.DataFrame()
        output = output.append( [h.to_dict(nested=False) for h in self.values], ignore_index=True )
        return output

    def __repr__(self):
        return str([p for p in self.values])



