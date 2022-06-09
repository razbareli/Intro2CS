import boggle_gui
import boggle_controller
import ex12_utils
import boggle_board_randomizer as bg_rand
from tkinter import messagebox

SIZE = 4


class Boggle:

    # The __init__ method for the Boggle class
    def __init__(self, board, words_dict):
        self.__game_time = 181  # The gui removes 1 second upon initializing so add one more second than intended
        self.__words_dict = words_dict
        self.__gui = boggle_gui.Board_gui(self.__game_time, SIZE, board)
        self.__controller = boggle_controller.Boggle_controller(board, self.__words_dict, self.__gui)
        self.__buttons = self.__gui.get_buttons_dict()
        self.check_time_id = None

    # a method that restarts the game and cancels any commands waiting for the tkinter.after method
    def start_new_game(self):
        self.__gui.root.after_cancel(self.check_time_id)
        self.__gui.root.after_cancel(self.__gui.get_keep_time_id())
        self.__gui.root.destroy()
        board = bg_rand.randomize_board(bg_rand.LETTERS)
        self.__gui = boggle_gui.Board_gui(self.__game_time, SIZE, board)
        self.__controller = boggle_controller.Boggle_controller(board, self.__words_dict, self.__gui)
        self.__buttons = self.__gui.get_buttons_dict()
        self.run()

    # A method that checks if the timer of the game has reached 0 and if it has offers to start the game again.
    def check_time(self):
        if self.__gui.get_time() <= 1:
            MsgBox = messagebox.askquestion(title='Out of time', message="Time's up! You have earned " +
                                                                         str(self.__gui.get_score()) +
                                                                         " points - WOW!\nPlay again?")
            if MsgBox == 'yes':
                self.start_new_game()
            else:
                self.__gui.root.destroy()
        else:
            return self.__gui.root.after(self.__game_time * 1000, self.check_time)

    # A method that binds the restart command to the restart game button.
    def config_restart_game_button(self):
        right_buttons = self.__gui.get_right_buttons()
        button = right_buttons['restart\ngame']
        button.config(command=self.start_new_game)

    # A method that runs the whole game.
    def run(self):
        self.__gui.keep_time()
        self.check_time_id = self.check_time()
        self.__controller.config_check_button()
        self.config_restart_game_button()
        self.__controller.config_hint_button()
        self.__controller.gui_controller_match_command()
        self.__gui.root.mainloop()


if __name__ == '__main__':
    rand_board = bg_rand.randomize_board(bg_rand.LETTERS)
    words = ex12_utils.load_words_dict('boggle_dict.txt')
    game = Boggle(rand_board, words)
    game.run()
