import math
import sys
from wave_helper import *


MAX = 32767
MIN = -32768


# A function that displays the main menu:
def main_menu():
    while True:
        dictionary = {"1": change_wav_file_menu, "2": compose, "3": sys.exit}
        options = dictionary.keys()
        print("1 change WAV file\n2 compose a melody in WAV format\n3 exit the program")
        choice = choose_from_menu(options)
        dictionary[choice]()


# A function that let's the user choose from a the current menu
def choose_from_menu(options):
    while True:
        num = input("Pick an option from the menu -> ")
        if num in options:
            return num
        else:
            print("This option is not on the menu, please try again")


# Displays the menu with the options to change the file
def change_wav_file_menu(filename=None):
    dictionary = {"1": reverse, "2": opposite_wave, "3": speed_up, "4": slow_down, "5": vol_up, "6": vol_down,
                  "7": low_pass_filter, '8': end_menu}
    options = dictionary.keys()
    if filename is None:
        # If a file is not already under work, open a new file.
        filename = input('Please enter the name of the wave file you wish to edit -> ')
        try:
            sample_rate, melody = load_wave(filename)
            filename = [sample_rate, melody]
        except:
            print('Something went wrong with opening the file, please check the name and try again.')
            change_wav_file_menu()
    print("1 reverse\n2 opposite wave\n3 speed up\n4 slow down\n5 volume up\n6 volume down\n7 filter\n8 end menu")
    num = choose_from_menu(options)
    if num == '8':
        end_menu(filename)
    else:
        filename[1] = dictionary[num](filename[1])
    change_wav_file_menu(filename)


# A function that composes a wave file using an instructions file
def compose():
    file_name = input('Please enter the name of the composing instructions file -> ')
    try:
        compose_file = get_compose_file(file_name)
    except:
        print('Something went wrong with opening the file, please check the name and try again.')
        compose()
    dictionary = {"A": 440, "B": 494, "C": 523, "D": 587, "E": 659, "F": 698, "G": 784, "Q": 2000}
    melody = []
    for note in compose_file:
        y = int(2000 * (note[1]*(1/16)))
        samples_per_cycle = 2000 / dictionary[note[0]]
        for j in range(y):
            value = int(MAX*math.sin(math.pi*2*(j/samples_per_cycle)))
            melody.append([value, value])
    filename = [2000, melody]
    change_wav_file_menu(filename)


# A function that retrieves the instruction file for composing.
def get_compose_file(filename):
    with open(filename, 'r') as f:
        r = f.read()
    lst = r.split()
    lst2 = [i.strip() for i in lst]
    new_lst = []
    for i in range(0, len(lst2), 2):
        new_lst.append([lst2[i], int(lst2[i+1])])
    return new_lst


# 7 functions for editing WAV file:
# A function that reverses the WAV file
def reverse(file_list):
    output = [note for note in reversed(file_list)]
    return output

def opposite_wave(file_list):
    output = file_list[:]
    for i in output:
        for j in range(2):
            if i[j] == MIN:
                i[j] = MAX
            else:
                i[j] = -1*(i[j])
    return output


# A function that speeds up the audio of the file by removing all odd indexes in the file
def speed_up(file_list):
    file_list = [file_list[i] for i in range(len(file_list)) if i % 2 == 0]
    return file_list


# A function that takes two indexes in the list of the file, n as the first index and m as the one after him
# and inserts between the two indexes an average of the values of the two indexes.
def slow_down(file_list):
    m = 1
    n = 0
    for i in range(len(file_list)-1):
        left = int((file_list[i+n][0]+file_list[i+n+1][0])/2)
        right = int((file_list[i+n][1]+file_list[i+n+1][1])/2)
        file_list.insert(i+m, [left, right])
        m += 1
        n += 1
    return file_list


# A function that raises the volume of the file while going above or below the Min Max values defined.
def vol_up(file_list):
    output = []
    for i in file_list:
        couple = []
        for num in range(2):
            if i[num] <= 0:
                if MIN <= 1.2 * i[num]:
                    couple.append(int(1.2 * i[num]))
                else:
                    couple.append(MIN)
            if i[num] > 0:
                if MAX >= 1.2 * i[num]:
                    couple.append(int(1.2 * i[num]))
                else:
                    couple.append(MAX)
        output.append(couple)
    return output


# A function that lowers the sound of the file
def vol_down(file_list):
    output = [[int(i[0]/1.2), int(i[1]/1.2)] for i in file_list]
    return output


# A function that applies the low_pass_filter to the audio file
def low_pass_filter(file_list):
    output = []
    if len(file_list) == 1:
        return file_list
    for i in range(len(file_list)):
        if i == 0:
            left = int((file_list[i][0] + file_list[i + 1][0]) / 2)
            right = int((file_list[i][1] + file_list[i + 1][1]) / 2)
        if i == len(file_list)-1:
            left = int((file_list[i][0] + file_list[i - 1][0]) / 2)
            right = int((file_list[i][1] + file_list[i - 1][1]) / 2)
        if 0 < i < len(file_list)-1:
            left = int((file_list[i][0] + file_list[i + 1][0] + file_list[i - 1][0]) / 3)
            right = int((file_list[i][1] + file_list[i + 1][1] + file_list[i - 1][1]) / 3)
        output.append([left, right])
    return output


# A function that saves a WAV file and returns the user to the main menu
def end_menu(filename):
    file_name = input('Please enter a name for the file to be saved as -> ')
    save_wave(filename[0], filename[1], file_name)
    main_menu()


if __name__ == "__main__":
    main_menu()
