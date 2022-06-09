from car import Car
from board import Board
import sys
import helper

class Game:
    """
    created the game Rush Hour with specific rules
    """
    NAMES = "YBOWGR"
    LENGTHS = "234"
    ORIENTATIONS = "01"
    DIRECTIONS = "udlr"
    def __init__(self, board):
        """
        Initialize a new Game object.
        :param board: An object of type board
        """
        #You may assume board follows the API
        self.board = Board()

    def __single_turn(self):
        """
        runs a single turn in the game
        """
        if self.choose_car_dir() == 2:
            return 2
        else:
            if self.board.cell_content(self.board.target_location()) != None:
                return 1
            return 0

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        temp = []
        for i in j:
            k = 0
            globals()["car" + str(i)] = Car(i, j[i][0], (j[i][1][0], j[i][1][1]), j[i][2])
            temp.append(globals()["car" + str(i)])
            k += 1
        for i in temp:
            self.board.add_car(i)
        print(self.board)
        if self.board.cell_content(self.board.target_location()) != None:
            print("a car was placed at the winning target")
            return
        while True:
            stat = self.__single_turn()
            if stat == 2:
                return
            if stat == 0:
                continue
            if stat == 1:
                print('you won the game')
                return

    #functions I've added:

    def load_json_file(self, filename):
        """:param a string on the json file name
        :return dictionary with cars as keys, and the values are list with length, location and orientation"""
        return helper.load_json(filename)

    def choose_car_dir(self):
        """checks if the car and direction chosen by the user are valid"""
        while True:
            inp = input("select car and direction")
            if inp == '!':
                print("game aborted by user")
                return 2
            if len(inp) == 3 and inp[0] in Game.NAMES and inp[2] in Game.DIRECTIONS:
                temp = self.board.move_car(inp[0], inp[2])
                if temp:
                    print("the car has moved")
                    print(self.board)
                    return
                else:
                    print("car not in game or can't move in direction")
                    continue
            else:
                print("input not valid")


if __name__== "__main__":
    #All access to files, non API constructors, and such must be in this
    #section, or in functions called from this section.
    b = Board()
    g = Game(b)
    j = helper.load_json(sys.argv[1])
    g.play()




