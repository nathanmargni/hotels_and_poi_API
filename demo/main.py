from tourism_api.objects.address import Address
from tourism_api.objects.hotel import Hotel
from tourism_api.managers.hotel_manager import HotelManager
from tourism_api.objects.point_of_interest import PointOfInterest
from tourism_api.managers.poi_manager import PoiManager
from tourism_api.objects.position import Position


def test_poi_manager_get():
    print("category",PoiManager.get_pois_by_category(category='BUSINESS', sort_by=PointOfInterest.KEYS['poiId'], direction=-1))
    print("----------------------------------------------------------")
    print("----------------------------------------------------------")

    print("subcategory",PoiManager.get_pois_by_subcategory(subcategory='BANK', sort_by=PointOfInterest.KEYS['name'], direction=-1))


def test_get_hotels():
    print(15 * "* ", "Listing all hotels:", 15 * "* ")
    print(HotelManager.get_hotels())


def test_insert_update_delete_hotel():
    h: Hotel = HotelManager.get_hotel_by_id(197922)
    h.hotel_id = -1
    h.name = "TESTPOSTCLIENT"
    HotelManager.add_hotel(h)
    print(15 * "* ", "Getting a new added hotel:", 15 * "* ")
    print(HotelManager.get_hotel_by_id(-1))
    h.hotel_id = -2
    h.name = "TESTPOSTCLIENT2MODIFIED2"
    response = HotelManager.update_hotel(h)
    print(15 * "* ", "Updating a non existent hotel (id) returns:", 15 * "* ")
    print(response)
    h.hotel_id = -1
    HotelManager.update_hotel(h)
    print(15 * "* ", "Hotel after MODIFIED:", 15 * "* ")
    print(HotelManager.get_hotel_by_id(-1))
    print(15 * "* ", "Deleting that hotel:", 15 * "* ")
    print(HotelManager.delete_hotel_by_id(-1))
    print(15 * "* ", "Getting the deleted hotel by id:", 15 * "* ")
    print(HotelManager.get_hotel_by_id(-1))

def test_hotel_manager_get():
    print("city",HotelManager.get_hotels_by_city('Lugano', sort_by=Hotel.KEYS['price'], direction=-1))
    print("----------------------------------------------------------")
    print("----------------------------------------------------------")

    print("price range",HotelManager.get_hotels_by_price_range(end=100, sort_by=Hotel.KEYS['name']))


def test_get_pois():
    print(15 * "*", "Listing all pois: ", 15 * "*")
    print(PoiManager.get_pois())


def test_insert_update_delete_poi():
    p: PointOfInterest = PoiManager.get_poi_by_id(3)
    p.poi_id = -1
    p.name = "TESTPOSTCLIENT"
    PoiManager.add_poi(p)
    print(15 * "* ", "Getting by id the new poi added:", 15 * "* ")
    print(PoiManager.get_poi_by_id(-1))
    p.poi_id = -2
    p.name = "TESTPOSTCLIENT2MODIFIED2"
    response = PoiManager.update_poi(p)
    print(15 * "* ", "Updating a non existent poi (id) returns:", 15 * "* ")
    print(response)
    p.poi_id = -1
    PoiManager.update_poi(p)
    print(15 * "* ", "Poi after MODIFIED:", 15 * "* ")
    print(PoiManager.get_poi_by_id(-1))
    print(15 * "* ", "Delete that poi:", 15 * "* ")
    print(PoiManager.delete_poi_by_id(-1))
    print(15 * "* ", "Getting the deleted poi by id:", 15 * "* ")
    print(PoiManager.get_poi_by_id(-1))


if __name__ == '__main__':

    test_insert_update_delete_hotel()
    test_insert_update_delete_poi()
    hotellist = HotelManager.get_hotels_by_stars_range(start = 5)
    HotelManager.save_map(hotellist, filename="hotel_map.html")
    poilist = PoiManager.get_pois_by_subcategory("POLICE")
    PoiManager.save_map(poilist, filename="poi_map.html")
