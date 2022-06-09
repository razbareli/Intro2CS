from car import Car

class Board:
    """
    Add a class description here.
    Write briefly about the purpose of the class
    """

    def __init__(self):
        # Note that this function is required in your Board implementation.
        # However, is not part of the API for general board types.
        self.cells = [(i, j) for i in range(7) for j in range(7)]
        self.cells.insert(28, (3, 7))
        self.cars_on_board = set()
        self.cars_name_space = dict()


    def __str__(self):
        """
        This function is called when a board object is to be printed.
        :return: A string of the current status of the board
        """
        #The game may assume this function returns a reasonable representation
        #of the board for printing, but may not assume details about it.
        temp = ""
        for i in range(7):
            for j in range(7):
                if (i, j) not in self.taken_places_on_board():
                    temp += "  .  "
                else:
                    for k in self.cars_name_space:
                        if (i,j) in self.cars_name_space[k]:
                            temp += '  '+k[0].upper()+'  '
                            break

            if (i, j) == ((self.target_location()[0], self.target_location()[1]-1)):
                temp += "WIN"+"\n"
            else:
                temp += "#"+"\n"
        return temp

    def cell_list(self):
        """ This function returns the coordinates of cells in this board
        :return: list of coordinates
        """
        #In this board, returns a list containing the cells in the square
        #from (0,0) to (6,6) and the target cell (3,7)
        temp = self.cells[:]
        return temp

    def possible_moves(self):
        """ This function returns the legal moves of all cars in this board
        :return: list of tuples of the form (name,movekey,description) 
                 representing legal moves
        """
        #From the provided example car_config.json file, the return value could be
        #[('O','d',"some description"),('R','r',"some description"),('O','u',"some description")]
        temp = []
        for i in self.cars_on_board:
            Car.possible_moves(i)
            for j in i.possible_moves():
                t = i.movement_requirements(j)[0]
                y = self.taken_places_on_board()
                if t in self.cells and t not in y:
                    temp.append((i.get_name(), j, i.possible_moves()[j]))
        return temp

    def target_location(self):
        """
        This function returns the coordinates of the location which is to be filled for victory.
        :return: (row,col) of goal location
        """
        #In this board, returns (3,7)
        return (3, 7)

    def cell_content(self, coordinate):
        """
        Checks if the given coordinates are empty.
        :param coordinate: tuple of (row,col) of the coordinate to check
        :return: The name of the car in coordinate, None if empty
        """
        for i in self.cars_name_space:
            if coordinate in self.cars_name_space[i]:
                return i
        return None

    def add_car(self, car):
        """
        Adds a car to the game.
        :param car: car object of car to add
        :return: True upon success. False if failed
        """
        #Remember to consider all the reasons adding a car can fail.
        #You may assume the car is a legal car object following the API.
        # implement your code and erase the "pass"
        temp = self.taken_places_on_board()
        for i in car.car_coordinates():
            if i in temp or i not in self.cells:
                return False
        if car.get_name() in self.cars_name_space:
            return False
        else:
            self.cars_name_space[car.get_name()] = car.car_coordinates()
            self.cars_on_board.add(car)
            return True


    def move_car(self, name, movekey):
        """
        moves car one step in given direction.
        :param name: name of the car to move
        :param movekey: Key of move in car to activate
        :return: True upon success, False otherwise
        """
        temp = self.possible_moves()
        for i in temp:
            if (name, movekey) == ((i[0], i[1])):
                for j in self.cars_on_board:
                    if j.get_name() == name:
                        Car.move(j, movekey)
                        self.cars_name_space[name] = Car.car_coordinates(j)
                        return True
        return False

    # functions I have added:

    def taken_places_on_board(self):
        """:returns a set of all the unavailable coordinates on the board"""
        temp = {j for i in self.cars_name_space for j in self.cars_name_space[i]}
        return temp
