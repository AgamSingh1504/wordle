import tkinter as tk
from tkinter import messagebox
import word_game
import random_word_generator as wordlist

# Position indicating colours
GREEN = "#078215"
YELLOW = "#ded821"
GRAY = "#8a897c"

# Widget colours
WINDOW_BG = "#f3d7f7"
KEYBOARD_BG = "#dab1e0"
BUTTON_PRESS = "#bb8cc2"

# Game Settings
WORD_LENGTH = 5
MAX_TRIES = 6

labels = []
buttons = []
row = 0
col = 0
trial_word = ""
complete = False

# Print letters onto the labels
def print_label(key):
    global row
    global col
    global trial_word

    active_label = labels[row][col]
    active_label.config(text = key)
    trial_word += key

    col += 1
    if col == WORD_LENGTH:
        for i, button_row in enumerate(buttons):
            for button in button_row:
                if button != buttons[i][-1]:
                    button['state'] = "disabled"
    return

# Enter button. Submits guessed word for evaluation
def enter():
    global row, col, trial_word, complete

    if col != WORD_LENGTH:
        return
    
    if trial_word in wordlist.valid_word_set:
        output = word_game.evaluate_guess(trial_word)
        change_label_bg(output)
        if output == "BBBBB":
            complete_True()
            popup(output, word_game.correct_word)
            return
    else:
        messagebox.showerror("Invalid Word","Word not in dictionary")
        return
    
    trial_word = ""
    row += 1
    col = 0

    if row == MAX_TRIES:
        complete_True()
        popup(output, word_game.correct_word)
        row = 0
        col = 0
    
    for i, button_row in enumerate(buttons):
        for button in button_row:
            if button != buttons[i][-1]:
                button['state'] = "normal"

# Backspace button. Deletes recently entered letter
def backspace():
    global col, trial_word

    if col == 0:
        return
    
    if col == WORD_LENGTH:
        for i, button_row in enumerate(buttons):
            for button in button_row:
                if button != buttons[i][-1]:
                    button['state'] = "normal"
    
    trial_word = trial_word[:-1]
    col -= 1
    active_label = labels[row][col]
    active_label.config(text = "")
    return

# Clear button. Clears entire row
def clear():
    global col, trial_word

    trial_word = ""

    if col == WORD_LENGTH:
        for i, button_row in enumerate(buttons):
            for button in button_row:
                if button != buttons[i][-1]:
                    button['state'] = "normal"
    
    while col >= 0:
        col -= 1
        active_label = labels[row][col]
        active_label.config(text = "")
    
    col = 0
    return

# Change colours of the keys
def change_key_bg(letter, bg_colour):
    for button_row in buttons:
        for guessed_key in button_row:
            if letter == guessed_key['text']:
                if bg_colour == GREEN:
                        guessed_key.config(bg = bg_colour)
                elif bg_colour == YELLOW:
                    if guessed_key['bg'] != GREEN:
                        guessed_key.config(bg = bg_colour)
                elif bg_colour == GRAY:
                    if guessed_key['bg'] != GREEN and guessed_key['bg'] != YELLOW:
                        guessed_key.config(bg = bg_colour)
    return

# Change the colours of the labels
def change_label_bg(result):
    for i, char in enumerate(result):
        letter = trial_word[i]
        if char == 'B':
            bg_colour = GREEN
            labels[row][i].config(bg = bg_colour)
            change_key_bg(letter, bg_colour)
        
        elif char == 'C':
            bg_colour = YELLOW
            labels[row][i].config(bg = bg_colour)
            change_key_bg(letter, bg_colour)
        
        elif char == 'X':
            bg_colour = GRAY
            labels[row][i].config(bg = bg_colour)
            change_key_bg(letter, bg_colour)
    return

# End of game popup
def popup(result, word):
    pop = tk.Toplevel(root)
    x = root.winfo_x()
    y = root.winfo_y()
    pop.geometry("300x100+{0}+{1}".format(x+75,y+175))
    pop.resizable(0,0)
    pop.wm_transient(root)
    
    if result == "BBBBB":
        pop.title("Game Won")
        pop_label = tk.Label(pop, text = "Congrats! You guessed the word {0} correctly.".format(word))
        pop_label.pack(pady = 20)
    else:
        pop.title("Game Over")
        pop_label = tk.Label(pop, text = "You exhausted the maximum number of tries.\nThe correct word was {0}".format(word))
        pop_label.pack(pady = 10)
    
    pop_button = tk.Button(pop, text = "OK", command = lambda : [pop.destroy(), complete_True(), new_game()])
    pop_button.pack()
    return

def exit_game():
    end = messagebox.askyesno("Exit Game","Do you really wish to quit?")
    if end:
        root.destroy()
    return

def display_help():
    top = tk.Toplevel(root)
    top.title("How to Play")
    x = root.winfo_x()
    y = root.winfo_y()
    top.geometry("650x250+{0}+{1}".format(x+75,y+175))
    top.resizable(0,0)
    top.wm_transient(root)

    topFrame = tk.Frame(top)
    topFrame.pack(side = 'top', fill = 'both', expand = 1, padx = 10, pady = 10, ipadx = 10, ipady = 10)
    topLabel = tk.Label(topFrame)
    topLabel.pack(side = 'left', fill = 'both', expand = 1, padx = 2)
    msg = """Guess the word in six tries using virtual keyboard.
    
    Each guess must be a valid five-letter word. Hit the Enter key to submit. 
    The Backspace and Clear keys can be used to edit or clear your guess.
    
    After submitting, the colour of the tiles will change to show how close your guess was to the word.
    
    Green indicates correct letter in correct spot.
    Yellow indicates correct letter in wrong spot.
    Gray indicates incorrect letter.

    Game ends when correct word is guessed or user exhausts maximum number of tries.
    """
    topLabel.config(text = msg)
    return

def complete_True():
    global complete
    complete = True
    for button_row in buttons:
            for button in button_row:
                button['state'] = "disabled"
    return

# menubar
def menubar(parent):
    menubar = tk.Menu(parent)
    options_menu = tk.Menu(menubar, tearoff = 0)
    options_menu.add_command(label = "New Game", command = new_game)
    options_menu.add_command(label = "Exit", command = exit_game)
    menubar.add_cascade(label = "Options", menu = options_menu)

    help_menu = tk.Menu(menubar, tearoff = 0)
    help_menu.add_command(label = "How to Play", command = display_help)
    menubar.add_cascade(label = "Help", menu = help_menu)

    parent.config(menu = menubar)
    return

# main window layout
def window(parent):
    mainFrame = tk.Frame(parent, bg = WINDOW_BG)
    mainFrame.pack(side = 'top', fill = 'both', expand = 1, padx = 10, pady = 10, ipadx = 10, ipady = 10)

    for label_row in range(MAX_TRIES):        # max tries = 6
        row_frame = tk.Frame(mainFrame, bg = WINDOW_BG)
        row_frame.pack(side = 'top', fill = 'y', expand = 1, pady = 2)
        label_row = []
        for label_col in range(WORD_LENGTH):    # 5-lettered words
            letter_label = tk.Label(row_frame, fg = "black", bg = "white", height = 2, width = 4)
            label_row.append(letter_label)
            letter_label.config(font = ("Arial Bold" , 10))
            letter_label.pack(side = 'left', fill = 'both', expand = 1, padx = 2)
        labels.append(label_row)
    #print(labels)
    return

# keyboard layout
def keyboard(parent):
    keyboardFrame = tk.Frame(parent, bg = WINDOW_BG)
    keyboardFrame.pack(side = 'bottom', fill = 'both', expand = 1, padx = 10, pady = 10, ipadx = 10, ipady = 10)
    keys = [
            ('q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'clear'),
            ('a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'backspace'),
            ('z', 'x', 'c', 'v', 'b', 'n', 'm', 'enter')
        ]

    for key_group in keys:
        group_frame = tk.Frame(keyboardFrame)
        group_frame.pack(side = 'top', fill = 'both', expand = 1)
        
        button_row = []
        for key in key_group:
            key = key.capitalize()
            if len(key) == 1:                                                   # All alphabet keys
                key_button = tk.Button(group_frame, text = key, bg = KEYBOARD_BG, activebackground = BUTTON_PRESS)
                key_button['command'] = lambda q = key.upper() : print_label(q)                 
            else:                                                               # Clear, Backspace, Enter keys
                key_button = tk.Button(group_frame, text = key, bg = KEYBOARD_BG, activebackground = BUTTON_PRESS)
                if key == "Enter":
                    key_button['command'] = enter
                elif key == "Backspace":
                    key_button['command'] = backspace
                elif key == "Clear":
                    key_button['command'] = clear
            key_button.pack(side = 'left', fill = 'both', expand = 1)
            button_row.append(key_button)
        buttons.append(button_row)
        #print(buttons)
    return

# Starts the game. Resets all global variables.
def start_game():
    global labels, buttons, row, col, letter, trial_word, complete, root

    complete = False
    labels = []
    buttons = []
    row = 0
    col = 0
    letter = ""
    trial_word = ""

    root = tk.Tk()
    root.title("Word Game")
    pos_right = int(root.winfo_screenwidth()/2 - 450/2)
    pos_down = int(root.winfo_screenheight()/2 - 450/2)
    root.geometry("450x450+{0}+{1}".format(pos_right, pos_down))
    root.config(bg = WINDOW_BG)
    root.resizable(0,0)

    menubar(root)
    window(root)
    keyboard(root)
    root.mainloop()
    return

# Starts a new game
def new_game():
    global root
    if complete == False:
        new = messagebox.askyesno("New Game", "Do you wish to quit the current game and start a new one?")
        if not new:
            return
    elif complete == True:
        new = messagebox.askyesno("New Game","Do you wish to start a new game?")
        if not new:
            root.destroy()
            return
    word_game.correct_word = wordlist.mystery_word()
    root.destroy()
    root = start_game()
    return

root = start_game()