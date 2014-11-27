# Copyright 2014 Dustin Wehr
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 1, CSC148, Winter 2014.
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.
"""
ConsoleController: User interface for manually solving Anne Hoy's problems 
from the console.

move: Apply one move to the given model, and print any error message 
to the console. 
"""

from TOAHModel import TOAHModel, Cheese, IllegalMoveError


def move(model: TOAHModel, origin: int, dest: int) -> None:
    '''
    Module method to apply one move to the given model, and print any
    error message to the console. 
    
    model - the TOAHModel that you want to modify
    origin - the stool number (indexing from 0!) of the cheese you want 
             to move
    dest - the stool number that you want to move the top cheese 
            on stool origin onto.
    '''

    try:
        model.move(origin, dest)
    except IllegalMoveError:
        print('Invalid move! Try again')
        

class ConsoleController:
    
    def __init__(self: 'ConsoleController', 
                 number_of_cheeses: int, number_of_stools: int) -> None:
        """
        Initialize a new 'ConsoleController'.
        """
        
        TOAHModel.__init__(self, number_of_stools)
        TOAHModel.fill_first_stool(self, number_of_cheeses) 
        self.cheese_model = TOAHModel(number_of_stools)
        self.number_of_stools = number_of_stools
        self.cheese_model.fill_first_stool(number_of_cheeses)

    def play_loop(self: 'ConsoleController') -> None:
        '''    
        Console-based game. 
        TODO:
        -Start by giving instructions about how to enter moves (which is up to
        you). Be sure to provide some way of exiting the game, and indicate
        that in the instructions.
        -Use python's built-in function input() to read a potential move from
        the user/player. You should print an error message if the input does
        not meet the specifications given in your instruction or if it denotes
        an invalid move (e.g. moving a cheese onto a smaller cheese).
        You can print error messages from this method and/or from
        ConsoleController.move; it's up to you.
        -After each valid move, use the method TOAHModel.__str__ that we've 
        provided to print a representation of the current state of the game.
        '''
        instructions = input("In order to make a move, you must insert the \
initial_stool number and the final_stool number seperated by a comma. If you \
wish to exit the game, input 'exit' and answer'yes'. Press enter to begin!")
            
        prompt = input('Your move (initial_stool, final_stool):')
        while prompt != 'exit':
            new_list = prompt.split(sep=',')
            move_list = []
            try:
                int(new_list[0]) or int(new_list[1])
            except ValueError:
                print('Invalid entry! Try again')
                prompt = input('Your move (initial_stool, final_stool):')

            move_list.append(int(new_list[0]))
            move_list.append(int(new_list[1]))
            move(self.cheese_model, move_list[0], move_list[1])
            print(self.cheese_model.__str__())
            prompt = input('Your move (initial_stool, final_stool):')
          
        else:
            exit()

if __name__ == '__main__':
    ConsoleController(6, 4).play_loop()
