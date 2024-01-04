from enum import Enum
from PIL import ImageTk, Image
import time
import tkinter as tk
import tkinter.ttk as ttk
from typing import Callable
import string

###########################################################################
# Class:         WordleGUI
# Author:        Barry Lawson
# Last modified: 23 Mar 2023
#

###########################################################################
class LetterBox(tk.Button):
    ''' Class to wrap a tk.Button, representing a letter in the Wordle grid.
        The class provides the ability to clear the letter, or to mark as
        correct (green), incorrect (gray), or misplaced (gold).
    '''
    __slots__ = ("_font", "_is_key", "_marked")

    class Marked(Enum):
        UNMARKED  = 0
        CORRECT   = 1
        INCORRECT = 2
        MISPLACED = 3

    def __init__(self, 
                 window : tk.Tk, 
                 image  : ImageTk.PhotoImage = None, 
                 text   : str = "",
                 font   : tuple = ('Arial', 40, 'bold')) -> None:
        ''' initializer for a LetterBox object
        Parameters:
            window: the root tk.Tk window for the Wordle GUI
            image:  the ImageTk.PhotoImage to use as background
            text:   text to display, if any
            font:   the font to use for the box (tuple of family, size)
        '''
        super().__init__(window, \
            image = WordleGUI._img_blank if image is None else image, \
            compound = "center", \
            text = text, font = font, \
            disabledforeground = "black", state = "disabled")
        self._font   = font
        self._is_key = False
        self._marked = LetterBox.Marked.UNMARKED

    def getLetter(self) -> str:
        ''' getter to return the letter inside this LetterBox '''
        return self.cget("text")

    def setLetter(self, letter: str) -> None:
        ''' setter to update the letter inside this LetterBox '''
        self.config(text = "" if len(letter) == 0 else letter[0])

    def clear(self) -> None:
        ''' method to clear this LetterBox, reverting to no letter
            and empty background '''
        self.config(disabledforeground = "black")
        image = WordleGUI._img_blank if not self._is_key else WordleGUI._img_available_key
        text  = "" if not self._is_key else self.getLetter()
        self.config(image = image)
        self.config(text = text)
        self._marked = LetterBox.Marked.UNMARKED

    def markCorrect(self) -> None:
        ''' method to mark this LetterBox as correct (white on green) '''
        self.config(disabledforeground = "white")
        image = WordleGUI._img_correct if not self._is_key else WordleGUI._img_correct_key
        self.config(image = image)
        self._marked = LetterBox.Marked.CORRECT

    def markIncorrect(self) -> None:
        ''' method to mark this LetterBox as incorrect (white on gray) '''
        if self._marked in [LetterBox.Marked.CORRECT, LetterBox.Marked.MISPLACED]: return
        self.config(disabledforeground = "white")
        image = WordleGUI._img_incorrect if not self._is_key else WordleGUI._img_incorrect_key
        self.config(image = image)
        self._marked = LetterBox.Marked.INCORRECT

    def markMisplaced(self) -> None:
        ''' method to mark this LetterBox as out of place (white on gold) '''
        if self._marked in [LetterBox.Marked.CORRECT]: return
        self.config(disabledforeground = "white")
        image = WordleGUI._img_misplaced if not self._is_key else WordleGUI._img_misplaced_key
        self.config(image = image)
        self._marked = LetterBox.Marked.MISPLACED

    def markInvalid(self) -> None:
        ''' method to mark this LetterBox as invalid (black on red) '''
        self.config(disabledforeground = "black")
        self.config(image = WordleGUI._img_invalid)

###########################################################################
class KeyBox(LetterBox):
    ''' Class to wrap a tk.Button, representing a letter in the keyboard.
        Child of LetterBox, simply using different font and image.
    '''
    __slots__ = ("_is_marked")
    def __init__(self, window : tk.Tk, text: str) -> None:
        ''' initializer for a LetterBox object for the keyboard
        Parameters:
            window: the root tk.Tk window for the Wordle GUI
            text:   the key's displayed text
        '''
        super().__init__(window, text = text, font = ('Arial',20,'bold'),  \
            image = WordleGUI._img_available_key)
        self._is_key    = True

###########################################################################
class GameState(Enum):
    ACTIVE = 0
    WIN    = 1
    LOSE   = 2

###########################################################################
class WordleGUI:
    __slots__ = ("_current_row", "_current_col", "_letters", "_keyboard", \
                 "_handler_function", "_reset_function", "_game_state", \
                 "_window", "_word_canvas", "_keyboard_canvas", \
                 "_menubar", "_file_menu", "_final_msg")

    # class-level variables
    _MAX_WORD_LEN  : int = 5
    _MAX_GUESSES   : int = 6
    _INVALID_PAUSE : float = 1.25 # time to pause showing invalid in red
    _INVALID_DELAY : float = 0.1  # time to delay between invalid rollbacks
    _UPDATE_DELAY  : float = 0.1  # time to delay b/w correct/incorrect reveals
    _DANCE_DELAY   : float = 0.08 # time between letter dance on win

    # these are updated once the root tk.Tk window is created in __init__
    _img_blank         : ImageTk.PhotoImage = None
    _img_correct       : ImageTk.PhotoImage = None
    _img_incorrect     : ImageTk.PhotoImage = None
    _img_misplaced     : ImageTk.PhotoImage = None
    _img_invalid       : ImageTk.PhotoImage = None

    _img_available_key : ImageTk.PhotoImage = None
    _img_correct_key   : ImageTk.PhotoImage = None
    _img_incorrect_key : ImageTk.PhotoImage = None
    _img_misplaced_key : ImageTk.PhotoImage = None

    _img_final_msg     : ImageTk.PhotoImage = None

    ####################################################################################
    def __init__(self, handler_function: Callable, new_game_function: Callable) -> None:
        ''' initializer for the Wordle GUI, setting up the window for game play
        Parameters:
            handler_function: student-written function to call that process a
                word entered by the player
            new_game_function: student-written function to call to let student
                know that the player has started a new game (for resetting)
        '''
        # create the overall tkinter window, with menus
        self._window = tk.Tk()
        self._window.configure(bg = "#ececec")
        self._window.geometry("660x720")
        self._window.title("Wordle")
        self._menubar = self._createMenu()
        self._window.config(menu = self._menubar)

        self._window.bind("<Key>", self._handleLetter)
        self._window.bind("<Return>", self._handleReturn)

        # create the class-level images to be used as backgrounds
        # (must occur after the root window has been created)
        WordleGUI._img_blank         = ImageTk.PhotoImage(Image.open('images/blank.png'))
        WordleGUI._img_correct       = ImageTk.PhotoImage(Image.open('images/correct.png'))
        WordleGUI._img_incorrect     = ImageTk.PhotoImage(Image.open('images/incorrect.png'))
        WordleGUI._img_misplaced     = ImageTk.PhotoImage(Image.open('images/misplaced.png'))
        WordleGUI._img_invalid       = ImageTk.PhotoImage(Image.open('images/invalid.png'))

        WordleGUI._img_available_key = ImageTk.PhotoImage(Image.open('images/key_available.png'))
        WordleGUI._img_correct_key   = ImageTk.PhotoImage(Image.open('images/key_correct.png'))
        WordleGUI._img_incorrect_key = ImageTk.PhotoImage(Image.open('images/key_incorrect.png'))
        WordleGUI._img_misplaced_key = ImageTk.PhotoImage(Image.open('images/key_misplaced.png'))

        WordleGUI._img_final_msg     = ImageTk.PhotoImage(Image.open('images/final.png'))

        # create a grid of LetterBox objects (tkButton wrappers) corresponding
        # to game grid entry boxes
        self._letters : list[LetterBox] = []
        self._word_canvas, self._letters = self._newLetterBoxes()
        self._word_canvas.pack(anchor = tk.N, pady = 10)

        # create a grid of LetterBox objects corresponding to the keyboard
        self._keyboard : dict[str, LetterBox] = {}
        self._keyboard_canvas, self._keyboard = self._newKeyboard()
        self._keyboard_canvas.pack(anchor = tk.S, pady = 10)

        # plop the window in the center of the screen
        self._window.eval('tk::PlaceWindow . center')

        self._current_row: int = 0
        self._current_col: int = 0
        self._game_state:  GameState = GameState.ACTIVE

        self._handler_function: Callable = handler_function
        self._reset_function:   Callable = new_game_function

        self._final_msg = tk.Button(image = WordleGUI._img_final_msg, text = "", \
            compound = "center", disabledforeground = "white", state = "disabled",
            font = ('Arial', 16, 'bold'))

        '''# and then start listening for keypress events
        self._window.mainloop()'''

    ################################################
    def start(self) -> None:
        ''' method to make window start listening for keypress events '''
        self._window.mainloop()

    ################################################
    def setFinalMessage(self, message: str) -> None:
        ''' method to allow the user to set the final message displayed at
            the end of the game
        Parameters:
            message: the string to display (15 chars or less)
        '''
        self._final_msg.config(text = message[0:15].upper())

    ################################################
    def _handleLetter(self, event: tk.Event) -> None:
        ''' listener method called whenever the Tk window detects a key press
        Parameters:
            event: a tk.Event, which if not an alphabetic charcter is ignored
        '''
        # if the game is already over, ignore
        if self._game_state != GameState.ACTIVE: return

        r = self._current_row;  c = self._current_col
        if 'A' <= event.char.upper() <= 'Z' and c < WordleGUI._MAX_WORD_LEN:
            # update the grid with the entered letter
            self._letters[r][c].setLetter(event.char.upper())
            self._current_col += 1 
        elif event.keysym == "BackSpace" and c >= 0:
            # just clear the previous LetterBox if the user presses backspace
            c -= 1
            self._letters[r][c].clear()
            self._current_col = max(c, 0)

    ################################################
    def _handleReturn(self, event: tk.Event) -> None:
        ''' listener method called whenever the Tk window detects a return
        Parameters:
            event: a tk.Event (should only be <Return>)
        '''
        # if the game is already over, ignore
        if self._game_state != GameState.ACTIVE: return

        # call the student's code to process the entered word
        word = "".join(box.getLetter() for box in self._letters[self._current_row])
        if len(word) < WordleGUI._MAX_WORD_LEN: return
        result = self._handler_function(word.lower())

        r = self._current_row
        if result is None:
            # invalid guess -- marke the word as invalid (black on red),
            # pause, then roll back leter by leter
            for c in range(0, WordleGUI._MAX_WORD_LEN):
                self._letters[r][c].markInvalid()
            self._word_canvas.update()
            time.sleep(WordleGUI._INVALID_PAUSE)
            for c in range(WordleGUI._MAX_WORD_LEN - 1, -1, -1):
                self._letters[r][c].setLetter("")
                self._letters[r][c].clear()
                self._word_canvas.update()
                time.sleep(WordleGUI._INVALID_DELAY)
            self._current_col = 0
        else:
            # valid guess -- exact_matches should be a list of indices
            # where letters are correct and in place;  misplaced should be
            # a list of indices where letters are correct but out of plac
            #
            (exact_matches, misplaced) = result
            for c in range(0, WordleGUI._MAX_WORD_LEN):
                # color each letter as correct, misplaced, or incorrect
                if c in exact_matches:
                    self._letters[r][c].markCorrect()
                elif c in misplaced:
                    self._letters[r][c].markMisplaced()
                else:
                    self._letters[r][c].markIncorrect()
                time.sleep(WordleGUI._UPDATE_DELAY)
                self._word_canvas.update()

            # now update the keyboard... make sure to go in order of
            # (a) correct, (b) misplaced, then (c) incorrect because
            # of checks for previously-marked keys (even though inefficient)
            for c in range(0, WordleGUI._MAX_WORD_LEN):
                letter = self._letters[r][c].getLetter().lower()
                if c in exact_matches: self._keyboard[letter].markCorrect()
            for c in range(0, WordleGUI._MAX_WORD_LEN):
                letter = self._letters[r][c].getLetter().lower()
                if c in misplaced:     self._keyboard[letter].markMisplaced()
            for c in range(0, WordleGUI._MAX_WORD_LEN):
                letter = self._letters[r][c].getLetter().lower()
                if c not in exact_matches and c not in misplaced:
                    self._keyboard[letter].markIncorrect()
            self._word_canvas.update()

            if len(exact_matches) == WordleGUI._MAX_WORD_LEN:
                self._game_state = GameState.WIN
                r = self._current_row
                for c in range(WordleGUI._MAX_WORD_LEN):
                    shift = r - 1 if r > 0 else r
                    self._letters[r][c].lift()
                    self._letters[r][c].grid(column=c,row=shift,rowspan=2)
                    self._word_canvas.update()
                    time.sleep(WordleGUI._DANCE_DELAY)
                    self._letters[r][c].grid(column=c,row=r,rowspan=1)
                    self._word_canvas.update()
                self._final_msg.place(x = 250, y = 0)
                self._word_canvas.update()
            else:
                self._current_row += 1
                self._current_col = 0
                if self._current_row >= WordleGUI._MAX_GUESSES:
                    self._game_state = GameState.LOSE
                    self._final_msg.place(x = 250, y = 0)

    #######################################
    def _newKeyboard(self) -> tk.Canvas:
        ''' private helper method to construct a tk.Canvas containing
            a keyboard of LetterBox objects
        Returns:
            a tk.Canvas object containing objects for displaying the keyboard
        '''
        # use a tk.Canvas for holding the keyboard
        canvas = tk.Canvas(self._window)
        keyboard = {}
        font = ('Arial', 20, 'bold')

        def plopRow(letters: str, row: int, last_row: bool = False) -> None:
            col = 0
            span = 1 if row == 0 else 2
            if last_row: 
                box = KeyBox(canvas, text = "⏎")
                #box.state(["disabled"])
                box.grid(column = col, row = row, padx = 0, pady = 0, columnspan = span)
                col += 1
            for letter in letters:
                keyboard[letter] = KeyBox(canvas, text = letter.upper())
                #keyboard[letter].state(["disabled"])
                keyboard[letter].grid(column = col, row = row, padx = 0, pady = 0, columnspan = span)
                col += 1
            if last_row: 
                box = KeyBox(canvas, text = "⌫")
                #box.state(["disabled"])
                box.grid(column = col, row = row, padx = 0, pady = 0, columnspan = span)
                col += 1

        letters = "qwertyuiop"
        plopRow(letters, row = 0)
        letters = "asdfghjkl"
        plopRow(letters, row = 1)
        letters = "zxcvbnm"
        plopRow(letters, row = 2, last_row = True)

        return canvas, keyboard


    #######################################
    def _newLetterBoxes(self) -> tk.Canvas:
        ''' private helper method to construct a tk.Canvas containing
            a grid (typically 6x5) of LetterBox objects
        Returns:
            a tk.Canvas object containing all LetterBox objects for display
        '''
        # use a tk.Canvas for holding the grid of rows
        canvas = tk.Canvas(self._window)

        letters = []
        for row in range(6):
            letters_row = []
            for col in range(5):
                letter_box = LetterBox(canvas)
                letter_box.grid(column = col, row = row, padx = 0, pady = 0)
                letters_row.append(letter_box)
            letters.append(letters_row)

        return canvas, letters


    ##############################
    def _createMenu(self) -> None:
        ''' private helper method to create the 'New Game' | 'Quit' menu '''
        # the overall menubar for the window
        self._menubar  = tk.Menu(self._window)

        # The file menu (consisting of New Game, Quit) within the menubar.
        # Note that 'command' sets the callback method for a given menu option.
        # Those callack methods are defined elsewhere in this class.
        self._file_menu = tk.Menu(self._menubar, tearoff=0)
        self._file_menu.add_command(label = "New Game", command = self._newGame)
        self._file_menu.add_separator()
        self._file_menu.add_command(label = "Quit", command = self._window.quit)

        # add the file menu as a cascading menu to the menubar
        self._menubar.add_cascade(label = "File", menu = self._file_menu)

        return self._menubar

    ###########################
    def _newGame(self) -> None:
        ''' private helper method to reset to a new Wordle game '''
        for r in range(WordleGUI._MAX_GUESSES):
            for c in range(WordleGUI._MAX_WORD_LEN):
                self._letters[r][c].clear()
        for char in string.ascii_lowercase:
            self._keyboard[char].clear() 
        self._current_row = 0
        self._current_col = 0
        self._game_state = GameState.ACTIVE
        self._final_msg.place_forget()
        self._word_canvas.update()
        # and let the student's code know that a new game has been started
        self._reset_function()

###################
def main() -> None:
    def processWord(guess: str) -> None: print(guess)
    def newGame() -> None: pass

    window = WordleGUI(processWord, newGame)
    window.start()

if __name__ == "__main__":
    main()
