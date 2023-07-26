from tourism_api.objects.position import Position


class PositionTest:

    def position_longitude_getter_test(self):
        expected_val =3
        pos_instance = Position( longitude=3)
        assert pos_instance.longitude == expected_val

    def position_longitude_setter_test(self):
        expected_val =3
        pos_instance = Position()
        pos_instance.longitude=3
        assert pos_instance.longitude == expected_val

    def position_longitude_setter2_test(self):

        pos_instance = Position()
        pos_instance.longitude=300
        assert pos_instance.longitude is None

    def position_longitude_setter3_test(self):
        pos_instance = Position()
        pos_instance.longitude=-190
        assert pos_instance.longitude is None

    def position_latitude_getter_test(self):
        expected_val =3
        pos_instance = Position( latitude=3)
        assert pos_instance.latitude == expected_val

    def position_latitude_setter_test(self):
        expected_val =3
        pos_instance = Position()
        pos_instance.latitude=3
        assert pos_instance.latitude == expected_val

    def position_latitude_setter2_test(self):

        pos_instance = Position()
        pos_instance.latitude=120
        assert pos_instance.latitude is None

    def position_latitude_setter3_test(self):
        pos_instance = Position()
        pos_instance.latitude=-95
        assert pos_instance.latitude is None

    def position_test_init(self):
        latitude = 67.12
        longitude = 43.1
        position_instance = Position( latitude=latitude, longitude=longitude )
        assert position_instance.latitude == latitude
        assert position_instance.longitude == longitude

    def position_test_init2(self):
        position_instance = Position()
        assert position_instance.latitude is None
        assert position_instance.longitude is None


    def position_test_init3(self):
        latitude = 185.12
        longitude = -430.1
        position_instance = Position( latitude=latitude, longitude=longitude )
        assert position_instance.latitude is None
        assert position_instance.longitude is None

    def position_to_dict_test(self):
        latitude = 67.12
        longitude = 43.1

        position_instance = Position( latitude=latitude, longitude=longitude )
        dict_instance = position_instance.to_dict()
        assert position_instance.longitude == dict_instance['latitude'] and \
               position_instance.latitude == dict_instance['longitude']


    def position_distance_to_test(self):
        pos1 = Position(67.12,43.1)
        pos2 = Position(69.12, 45.1)
        distance = pos1.distance_to(pos2)
        expected_distance = 23737
        #calculated by internet
        # https://www.meridianoutpost.com/resources/etools/calculators/calculator-latitude-longitude-distance.php?
        assert distance == expected_distance

