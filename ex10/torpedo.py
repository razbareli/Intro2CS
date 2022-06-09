class Torpedo:

    def __init__(self, location_x, location_y, speed_y, speed_x, direction):
        self.__location_x = location_x
        self.__speed_x = speed_x
        self.__location_y = location_y
        self.__speed_y = speed_y
        self.__direction = direction
        self.__radius = 4
        self.__life_span = 0

    def get_life_span(self):
        return self.__life_span

    def add_to_life_span(self):
        self.__life_span += 1

    def get_radius(self):
        return self.__radius

    def get_direction(self):
        return self.__direction

    def get_location_x(self):
        return self.__location_x

    def get_location_y(self):
        return self.__location_y

    def get_speed_x(self):
        return self.__speed_x

    def get_speed_y(self):
        return self.__speed_y

    def set_location_x(self, location):
        self.__location_x = location

    def set_location_y(self, location):
        self.__location_y = location

    def set_speed_x(self, speed):
        self.__speed_x = speed

    def set_speed_y(self, speed):
        self.__speed_y = speed
