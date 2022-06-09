import tkinter as tk
from tkinter import messagebox
import boggle_board_randomizer as bg_rand
from ex12_utils import valid_steps

BOARD_SIZE = 4
BUTTON_STYLE = {'font': ('Courier', 30),
                'borderwidth': 1,
                'relief': tk.RAISED,
                'bg': 'snow',
                'activebackground': 'DarkOrchid2'}


class Board_gui:
    # the __init__ method for the Board_gui class
    def __init__(self, time, board_size, rand_board):
        self.__board = rand_board
        root = tk.Tk()
        root.resizable(False, False)
        self.root = root
        root.title('Boggle')
        self.ask_if_ready()
        self.__score = 0
        self.__time_left = time
        self.__keep_time_id = None
        self.__word_already_found_id = None

        # create frames in the root board
        self.__outer_frame = tk.Frame(root, bg='light blue')
        self.__outer_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.__right_side_frame = tk.Frame(self.__outer_frame, bg='snow')
        self.__right_side_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.__left_side_frame = tk.Frame(self.__outer_frame, bg='light green')
        self.__left_side_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.__lower_frame = tk.Frame(self.__outer_frame)
        self.__lower_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # create buttons in the frames
        self.__buttons = {}
        self.__buttons_location = {}
        self.__last_button_pressed = []
        self.__right_buttons = {}
        self.__pressed_buttons = []
        self.create_main_buttons(board_size, rand_board)
        self.create_extra()

    # A method that activates the gui side of the program only, made for tests.
    def run(self):
        self.keep_time()
        self.root.mainloop()

    # A method that creates the grid for the main game board and calls the make main button method.
    def create_main_buttons(self, size, rand_board):
        for col in range(size):
            tk.Grid.columnconfigure(self.__lower_frame, col, weight=1)
        for row in range(size):
            tk.Grid.rowconfigure(self.__lower_frame, row, weight=1)
        num_row = 0
        for row in rand_board:
            num_col = 0
            for letter in row:
                self._make_main_button(letter, num_row, num_col)
                num_col += 1
            num_row += 1

    # A method  that get a letter and a location and creates a button in the main game board
    def _make_main_button(self, letter, row, col):
        text_letter = letter
        button = tk.Button(self.__lower_frame, text=text_letter, width=3, **BUTTON_STYLE)
        button.config(command=lambda s=button: self.button_command(s))
        button.bind('<Button-3>', lambda loc=(row, col): self.release_last_button((row, col)))
        button.grid(row=row, column=col, rowspan=1, columnspan=1)
        self.__buttons[button] = letter
        self.__buttons_location[button] = (row, col)
        self.bind_entry_and_leave(button)
        return button

    # A method that receives a text a command a color and a location and creates a fitting button
    # In the right side frame of the screen
    def _make_right_button(self, text, command, color, row, col):
        button = tk.Button(self.__right_side_frame, text=text, command=command,
                           font=('Courier', 18), width=8, height='4', borderwidth=1, relief=tk.RAISED,
                           bg='snow',
                           activebackground=color)
        button.grid(row=row, column=col)
        self.__right_buttons[text] = button
        self.bind_entry_and_leave(button, color)
        return button

    # A method that creates more gui buttons and labels.
    def create_extra(self):
        # right side buttons
        for i in range(4):
            tk.Grid.columnconfigure(self.__right_side_frame, i, weight=1)
        self._make_right_button('check\nword', None, 'green', 1, 1)
        self._make_right_button('clear\nall', self.release_all_buttons, 'red', 2, 1)
        self._make_right_button('restart\ngame', None, 'red', 3, 1)
        self._make_right_button('hint', None, 'yellow', 4, 1)

        # labels lower frame
        self.__score_label = tk.Label(self.__lower_frame, text=str(self.__score), bg='snow',
                                      font=('Courier', 17, 'bold'), relief="ridge", width=11, height=2)
        self.__score_label.grid(row=6, column=0, columnspan=2)
        self.__score_label2 = tk.Label(self.__lower_frame, text="Score",
                                       font=('Courier', 17, 'bold'), relief="ridge", width=11, height=1, bg="yellow",
                                       fg="blue")
        self.__score_label2.grid(row=5, column=0, columnspan=2)
        self.__time_panel = tk.Label(self.__lower_frame, text=self.__time_left, bg='snow',
                                     font=('Courier', 17, 'bold'), relief="ridge", width=11, height=2)
        self.__time_panel.grid(row=6, column=2, columnspan=2)
        self.__time_panel2 = tk.Label(self.__lower_frame, text="Time Left",
                                      font=('Courier', 17, 'bold'), relief="ridge", width=11, height=1, bg="yellow",
                                      fg="blue")
        self.__time_panel2.grid(row=5, column=2, columnspan=2)
        # labels outer frame
        self.__headline = tk.Label(self.__outer_frame, text="Let's Boggle!", bg="yellow", fg="blue",
                                   font="Verdana 30 bold")
        self.__headline.pack(side=tk.TOP, fill=tk.BOTH)
        self.__word_screen_var = ''
        self.__word_label_var = ''
        self.__word_screen_label = tk.Label(self.__outer_frame, text=self.__word_screen_var, bg='snow',
                                            font=('Courier', '21', 'bold'), relief="ridge", height=2)
        self.__word_screen_label.pack(side=tk.TOP, fill=tk.BOTH)
        # labels left frame
        self.__words_found_label = tk.Label(self.__left_side_frame, text='Words found', bg='light green',
                                            font="Verdana 30 bold underline")
        self.__words_found_label.pack(side=tk.TOP)

        self.__words_found_list = []
        self.__words_label = tk.Label(self.__left_side_frame, font=('Courier', '10'), bg='light green')
        self.__words_label.pack()

    # A method that handles the button command and makes sure the button can't be used again until
    # it is released
    def button_command(self, button):
        if self.is_valid_button(button):
            button.unbind('<Enter>')
            button.unbind('<Leave>')
            button.config(relief=tk.SUNKEN)
            button['background'] = 'DarkOrchid2'
            button.config(command=self.none_func)
            letter = self.__buttons[button]
            self.__pressed_buttons.append(button)
            self.__last_button_pressed.append(button)
            self.__word_screen_var += letter
            self.__word_screen_label['text'] = self.__word_screen_var
        else:
            self.__word_screen_label['text'] = 'Invalid button!'

    # A method that returns None as a standby method for buttons who cannot be pressed.
    def none_func(self):
        return None

    # A method that checks if a pressed button is a valid button by rules of boggle
    def is_valid_button(self, button):
        if self.__last_button_pressed:
            steps = valid_steps(self.__buttons_location[self.__last_button_pressed[-1]], self.__board)
            if self.__buttons_location[button] in steps:
                return True  # valid button pressed
            else:
                return False  # invalid button pressed
        else:
            return True  # no pressed button on board

    # A method that releases a button only if it is the last one pressed.
    def release_last_button(self, location):
        if self.__last_button_pressed:
            if location == self.__buttons_location[self.__last_button_pressed[-1]]:
                button = self.__last_button_pressed.pop()
                self.bind_entry_and_leave(button)
                button['background'] = 'snow'
                button.config(relief=tk.RAISED)
                button.config(command=lambda s=button: self.button_command(s))
                if len(self.__buttons[button]) == 2:
                    self.__word_screen_var = self.__word_screen_var[:-2]
                else:
                    self.__word_screen_var = self.__word_screen_var[:-1]
                self.__word_screen_label['text'] = self.__word_screen_var

    # A method that releases all pressed buttons on screen and clears all variables related.
    def release_all_buttons(self):
        if self.__word_already_found_id is not None:
            self.root.after_cancel(self.__word_already_found_id)
        for button in self.__buttons.keys():
            if button['relief'] == tk.SUNKEN:
                self.bind_entry_and_leave(button)
                button['background'] = 'snow'
                button.config(relief=tk.RAISED)
                button.config(command=lambda s=button: self.button_command(s))
        self.__word_screen_var = ''
        self.__word_screen_label['text'] = self.__word_screen_var
        self.__pressed_buttons = []
        self.__last_button_pressed = []

    # A method that binds entry and leave events to a button
    def bind_entry_and_leave(self, button, color1='deep sky blue'):
        def _on_enter(event):
            button['background'] = color1

        def _on_leave(event):
            button['background'] = 'snow'

        button.bind('<Enter>', _on_enter)
        button.bind('<Leave>', _on_leave)

    # A method that adds score_add to the score variable and updates the score label
    def update_score(self, score_add):
        self.__score += score_add
        self.__score_label['text'] = self.__score

    # A getter for the score variable
    def get_score(self):
        return self.__score

    # A getter for the time left variable
    def get_time(self):
        return self.__time_left

    # A getter for the current word made up by the buttons pressed
    def get_word_on_screen(self):
        return self.__word_screen_var

    # A method that reduces time on the clock up to 0 every second.
    def keep_time(self):
        if self.__time_left > 0:
            self.__time_left -= 1
            self.__time_panel['text'] = self.__time_left
            self.__keep_time_id = self.root.after(1000, self.keep_time)

    # A method that returns the after_id of the next keep_time to be executed.
    def get_keep_time_id(self):
        return self.__keep_time_id

    # A method that asks if the player is ready.
    def ask_if_ready(self):
        tk.messagebox.showinfo(title='play?', message='Ready to play?')

    # A method that adds a word to the list of the words found and updates the gui.
    def add_word_to_words_found(self, word):
        self.__words_found_list.append(word)
        if len(self.__words_found_list) == 0:
            self.__word_label_var += word
        else:
            self.__word_label_var += '\n'
            self.__word_label_var += word
        self.__words_label['text'] = self.__word_label_var

    # A method that returns a dictionary with all the buttons in the gui, with the button being
    # The key and the letter representing the button the value
    def get_buttons_dict(self):
        return self.__buttons

    # A method that returns a dictionary with the locations of all the buttons in the grid,
    # with the buttons being the key and the location the value.
    def get_buttons_locations(self):
        return self.__buttons_location

    # A method that returns a list of all the buttons pressed in reverse order.
    # (meaning the last button pressed is the last item on the list)
    def get_pressed_buttons(self):
        return self.__pressed_buttons

    # A method that returns a dictionary of the operating buttons on the right side of the screen,
    # With the keys being the text representing the button and the button being the value.
    def get_right_buttons(self):
        return self.__right_buttons

    # A method that handles the gui side of a word already found.
    def word_already_found(self, word):
        self.__word_screen_label.config(text=f'{word}\nalready found')
        self.__word_already_found_id = self.root.after(2000, self.update_word_screen_label)

    # A method that returns the word screen to the variable and releases all buttons.
    def update_word_screen_label(self):
        self.release_all_buttons()
        self.__word_screen_label.config(text=self.__word_screen_var)


if __name__ == '__main__':
    board = Board_gui(181, 4, bg_rand.randomize_board(bg_rand.LETTERS))
    board.run()
