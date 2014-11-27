# Copyright 2013, 2014 Gary Baumgartner, Danny Heap, Dustin Wehr
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 1, CSC148, Fall 2013.
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

from TOAHModel import TOAHModel
from TOAHModel import MoveSequence

import time


def tour_of_four_stools(model: TOAHModel, delay_btw_moves: float=0.5, 
                        console_animate: bool=False):
    """Move a tower of cheeses from the first stool in model to the fourth.

       model - a TOAHModel with a tower of cheese on the first stool
                and three other empty stools
       console_animate - whether to animate the tour in the console
       delay_btw_moves - time delay between moves in seconds IF 
                         console_animate == True
                         no effect if console_animate == False
    """
    
    n = model.number_of_cheeses()
    list_of_moves = moves_list(n, 0, 1, 2, 3)

    if console_animate:
        for move in list_of_moves:
            TOAHModel.move(model, move[0], move[1])
            print(model)
            print('Moving top cheese from {} to {}'.format(move[0], move[1]))
            time.sleep(delay_btw_moves)
    else:
        for move in list_of_moves:
            TOAHModel.move(model, move[0], move[1])
            print('Moving top cheese from {} to {}'.format(move[0], move[1]))
        
        
#helper functions
        
def moves_list(n: int, source: int=0, intermediate_left: int=1,
               intermediate_right: int=2, destination: int=3) -> list:
    """
    Return list of moves to move n cheeses from srouce to destination.
    """
    moves_lst = []
    move_with_four(moves_lst, n, source, intermediate_left,
                   intermediate_right, destination)
    MoveSequence.__init__(MoveSequence, moves_lst)

    return moves_lst


def move_with_three(moves_lst: list, n: int, source: int=0,
                    intermediate: int=1, destination: int=2) -> None:
    """
    Create list of moves required to move n cheeses from source to destination
    using three stools. 
    """

    if n > 1:
        move_with_three(moves_lst, n - 1, source, destination, intermediate)
        move_with_three(moves_lst, 1, source, intermediate, destination)
        move_with_three(moves_lst, n - 1, intermediate, source, destination)
    else:
        moves_lst.append((source, destination))


def move_with_four(moves_lst: list, n: int, source: int=0, 
                   intermediate_left: int=1,
                   intermediate_right: int=2, destination: int=3) -> None:
    """
    Create list of moves required to move n cheeses from source to destination
    using four stools. 
    """
    i = M(n)[1]
    
    if n > i and i != 0:
        move_with_four(moves_lst, n - i, source,
                       intermediate_right, destination, intermediate_left)
        move_with_three(moves_lst, i, source,
                        intermediate_right, destination)
        move_with_four(moves_lst, n - i, intermediate_left,
                       source, intermediate_right, destination)
    else:
        moves_lst.append((source, destination))
        
        
def M(n: int) -> tuple:
    """
    Return tuple with min number of moves required to move n cheeses at index 0
    and approprite i value at index 1. 
    """
    lst = []
    
    if n == 1:
        lst.append((1, 0))
    else:
        for i in range(1, n):
            lst.append((2 * M(n - i)[0] + 2 ** i - 1, i))
            
    return min(lst)


if __name__ == '__main__':
    NUM_CHEESES = 8
    DELAY_BETWEEN_MOVES = .5
    CONSOLE_ANIMATE = False
   
    # DO NOT MODIFY THE CODE BELOW.
    four_stools = TOAHModel(4)
    four_stools.fill_first_stool(number_of_cheeses=NUM_CHEESES)
    tour_of_four_stools(four_stools, console_animate=CONSOLE_ANIMATE,       
                                   delay_btw_moves=DELAY_BETWEEN_MOVES)
   
    print(four_stools.number_of_moves()) 
