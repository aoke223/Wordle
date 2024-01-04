import streamlit as st
import requests


import random
from utils import*
from WordleGUI import*
from printTest import*

st.markdown('# Oke Wordle')

class Wordle:
    __slots__=('_solution','_allowed_words','_num_guesses', '_wordle_gui', '_solution_words')

    
    def __init__(self, solutions_fname: str, allowed_words_fname: str) -> None:
        '''This function sets the instance variables
        parameters: solutions_fname - file with list of solution words
        allowed_words_fname - file with list of allowed words   '''
        self._solution="" 
        self._num_guesses=0
        self._wordle_gui= None
        with open(solutions_fname, "r") as f:
            self._solution_words=f.read().split()
        with open(allowed_words_fname, "r") as g:
            self._allowed_words=g.read().split()
        self._allowed_words=mergeSort(self._allowed_words)
        self._solution_words= mergeSort(self._solution_words)
        self.newGame()

    def setGUI(self,gui:'WordleGUI') -> None:
        '''This function sets the wordle gui
        paraters: gui'''
        self._wordle_gui=gui
        
    
    def pickRandomSolution(self) ->None:
        '''This function picks a random solution'''
        idx=random.randint(0,(len(self._solution_words)-1))
        self._solution= self._solution_words[idx]
        print(self._solution)
        

    def newGame(self, debug: bool=False) -> None:
        '''This function starts a new game'''
        self.pickRandomSolution()
        self._num_guesses=0
        if debug == True:
            print(self._solution)

    #make histogram of the solution letters using a dictionary
    def checkGuess(self, guess: str, debug: bool = False) -> tuple[list[int], list[int]] :
        '''This function checks the users guesses
        parameters: guess - users guess 
        debug- boolean
        returns: a list with the list of the indeces of the characters
        in the right spot, and a list of the the indeces of the characters 
        that are just in the solution'''
        correct=[]
        almost=[]
        d={}
        letters=[]
        for i in range (len(guess)):
            letters.append(self._solution[i])
        for i in range (len(letters)):
            if letters[i] in (d.keys()):
                d[letters[i]]+=1
            else: 
                d[letters[i]]=1
        print(d)
        for i in range (len(guess)):
            if guess[i]== self._solution[i]:
                correct.append(i)
                d[letters[i]] -= 1
            elif guess[i] in list(d.keys()) and d[letters[i]] !=0 :
                almost.append(i)
                d[letters[i]] -= 1
        self._num_guesses +=1
        return [correct,almost]



    def processGuess(self, guess: str, debug: bool = True) -> tuple[list[int], list[int]] | None:
        '''Ending Sceanarios 
        parameters: guess - users guess 
        debug- boolean'''
        if self._num_guesses > 6:
            self._wordle_gui.setFinalMessage("Out of Guesses :(") 
        if debug == True:
            print(self.checkGuess(guess))
        if binarySearch(guess, self._allowed_words) == False:
            return None
        elif guess == self._solution:
            self._wordle_gui.setFinalMessage("You Win!!! ;)") 
            return self.checkGuess(guess)
        else:
            return self.checkGuess(guess)
       
        
        

        
def main() ->None:
    #guess= "blank"
    #solution= "bleak"
    #e=wordle(guess)
    #printTest(e.checkGuess, guess, expected=[0,1,4][2])
    wordle = Wordle('wordle-answers.txt', 'wordle-allowed-guesses.txt')
    gui = WordleGUI(wordle.processGuess, wordle.newGame)
    wordle.setGUI(gui)
    gui.start()



if __name__ == "__main__":
    main()

