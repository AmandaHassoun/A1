# Copyright 2013, 2014 Gary Baumgartner, Danny Heap, Dustin Wehr
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
TOAHModel:  Model a game of Towers of Anne Hoy
Cheese:   Model a cheese with a given (relative) size
IllegalMoveError: Type of exceptions thrown when an illegal move is attempted
MoveSequence: Record of a sequence of (not necessarily legal) moves. You will 
need to return MoveSequence object after solving an instance of the 4-stool 
Towers of Anne Hoy game, and we will use that to check the correctness of your
algorithm.
"""


class TOAHModel:
    """Model a game of Towers Of Anne Hoy.

    Model stools holding stacks of cheese, enforcing the constraint
    that a larger cheese may not be placed on a smaller one.

    fill_first_stool - put an existing model in the standard starting config
    move - move cheese from one stool to another
    add - add a cheese to a stool        
    cheese_location - index of the stool that the given cheese is on
    number_of_cheeses - number of cheeses in this game
    number_of_moves - number of moves so far
    number_of_stools - number of stools in this game
    get_move_seq - MoveSequence object that records the moves used so far
     
    """
    
    def __init__(self: 'TOAHModel', amount_of_stools: int=4) -> None:
        """
        Initializes new TOAHModel.
        """

        self.amount_of_stools = amount_of_stools
        self.cheese_model = {}
        self._move_seq = MoveSequence([])
        
        for i in range(self.amount_of_stools):
            self.cheese_model[i] = []
            
    def fill_first_stool(self: 'TOAHModel', number_of_cheeses: int) -> None:
        """
        Put number_of_cheeses cheeses on the first (i.e. 0-th) stool,
        in order of size, with a cheese of size == number_of_cheeses
        on bottom and a cheese of size == 1 on top.        
        """
        
        self.cheese_amount = number_of_cheeses

        for i in range(self.cheese_amount, 0, -1):
            self.cheese_model[0].append(Cheese(i))

    def move(self: 'TOAHModel', from_stool: int, stool_index: int) -> None:
        """
        Move cheese from from_stool to stool_index.

        """
        
        self.from_stool = from_stool
        self.stool_index = stool_index

        if self.from_stool > self.amount_of_stools or (self.stool_index >
           self.amount_of_stools):
            raise IllegalMoveError('Stool out of range')
        elif from_stool == stool_index:
            raise IllegalMoveError('Same stool!')
        elif self.cheese_model[stool_index] != [] and \
             (self.cheese_model[stool_index][-1].size 
              < self.cheese_model[from_stool][-1].size):
            raise IllegalMoveError('Cheese is too big for this stool!')
        elif len(self.cheese_model[self.from_stool]) == 0:
            raise IllegalMoveError("Stool is empty !")
        else:
            top_cheese = self.cheese_model[from_stool].pop(-1)
            self.cheese_model[stool_index].append(top_cheese)
            self._move_seq.add_move(from_stool, stool_index)

    def add(self: 'TOAHModel', stool_index: int, cheese: 'Cheese') -> None:
        """
        Add cheese to stool_index.

        """

        if isinstance(cheese, Cheese):
            if self.cheese_model[stool_index] != [] and \
               self.cheese_model[stool_index][-1].size < cheese.size:
                raise IllegalMoveError('Cheese is too big for this stool!')
            else:
                self.cheese_model[stool_index].append(cheese)
        else:
            raise IllegalMoveError('You need to add a Cheese!')
            
    def cheese_location(self: 'TOAHModel', cheese: 'Cheese') -> int:
        """
        Return index of stool that cheese is on.

        >>> T = TOAHModel(4)
        >>> T.fill_first_stool(4)
        >>> T.move(0, 3)
        >>> T.cheese_location(Cheese(1))
        3
        """

        for stool_num in self.cheese_model:
            if cheese in self.cheese_model[stool_num]:
                return stool_num
        else:
            raise IllegalMoveError('Cheese size does not exist')

    def number_of_cheeses(self: 'TOAHModel') -> int:
        """
        Return number of cheeses on stools.
        
        >>> T = TOAHModel(4)
        >>> T.fill_first_stool(12)
        >>> T.number_of_cheeses()
        12
        """
        cheese_num = 0
        
        for stool_num in self.cheese_model:
            cheese_num += len(self.cheese_model[stool_num])

        return cheese_num      

    def number_of_stools(self: 'TOAHModel') -> int:
        """
        Return number of stools in cheese_model.

        >>> T = TOAHModel(5)
        >>> T.number_of_stools()
        5
        """

        return self.amount_of_stools

    def number_of_moves(self: 'TOAHModel') -> int:
        """
        Return number of moves.

        >>> T = TOAHModel(6)
        >>> T.fill_first_stool(9)
        >>> T.move(0,1)
        >>> T.move(0,2)
        >>> T.move(2,4)
        >>> T.number_of_moves()
        3
        """

        return self._move_seq.length()

    def top_cheese(self: 'TOAHModel', stool_index: int) -> 'Cheese':
        """
        Return top cheese at stool_index.

        >>> M = TOAHModel(4)
        >>> M.fill_first_stool(5)
        >>> M.move(0,1)
        >>> M.add(2, Cheese(6))
        >>> M.top_cheese(3)
        >>>
        """

        if self.cheese_model[stool_index] != []:
            return self.cheese_model[stool_index][-1]
        else:
            return None

    def _cheese_at(self: 'TOAHModel', stool_index: int,
                   stool_height: int) -> 'Cheese':
        """
        If there are at least stool_height+1 cheeses 
        on stool_index then return the (stool_height)-th one.
        Otherwise return None.
        
        >>> M = TOAHModel(4)
        >>> M.fill_first_stool(5)
        >>> M._cheese_at(0,3).size
        2
        >>> M._cheese_at(0,0).size
        5
        """
        self.stool_height = stool_height

        if len(self.cheese_model[stool_index]) >= stool_height + 1:
            return self.cheese_model[stool_index][stool_height]
        else:
            return None

    def get_move_seq(self: 'TOAHModel') -> 'MoveSequence':
        """
        Return MoveSequence of the current TOAHModel.
        """
        
        return self._move_seq    
                
    def __eq__(self: 'TOAHModel', other: 'TOAHModel') -> bool:
        """
        We're saying two TOAHModels are equivalent if their current 
        configurations of cheeses on stools look the same. 
        More precisely, for all h,s, the h-th cheese on the s-th 
        stool of self should be equivalent the h-th cheese on the s-th 
        stool of other.
        
        >>> m1 = TOAHModel(4)
        >>> m1.fill_first_stool(7)
        >>> m1.move(0,1)
        >>> m1.move(0,2)
        >>> m1.move(1,2)
        >>> m2 = TOAHModel(4)
        >>> m2.fill_first_stool(7)
        >>> m2.move(0,3)
        >>> m2.move(0,2)
        >>> m2.move(3,2)
        >>> m1 == m2
        True
        """
        
        return self.cheese_model == other.cheese_model

    def same_strategy(self: 'TOAHModel', other: 'TOAHModel') -> bool:
        """
        REQuirement: self and other have legal move sequences, and were 
        initialized in the standard way using TOAHModel.fill_first_stool. 
        It doesn't matter what your method does when self and other do not 
        satisfy this requirement.
        **This is a BONUS problem.**
        Insert this method in TOAHModel if you intend to attempt it.
        
        same_strategy is an equivalence relation that compares the entire move 
        sequences of the two models, but ignores superficial differences in 
        them. It is only defined when both models have legal move sequences, 
        so you can assume that is the case. 
        self and other are equivalent as strategies iff both of the 
        following are true:    
        (1) they have the same number of moves, stools, and cheeses
        (2) in the i-th cheese configurations C1 and C2 of self and 
            other, respectively, it's possible to permute the order of C2's 
            stools in such a way that they look the same as C1's stools (i.e.
            two TOAHModels with current configurations C1 and C2 would be 
            judged equivalent according to TOAHModel.__eq__)
        >>> m1 = TOAHModel(4)
        >>> m1.fill_first_stool(7)
        >>> m1.move(0,1)
        >>> m1.move(0,2)
        >>> m1.move(1,2)
        >>> m2 = TOAHModel(4)
        >>> m2.fill_first_stool(7)
        >>> m2.move(0,3)
        >>> m2.move(0,2)
        >>> m2.move(3,2)
        >>> m1.same_strategy(m2)
        True
        >>> m1.move(0,1)
        >>> m2.move(0,3)
        >>> m1.same_strategy(m2)
        True
        """
        if self.number_of_moves() == other.number_of_moves() \
           and self.amount_of_stools == other.amount_of_stools \
           and self.number_of_cheeses() == other.number_of_cheeses():
            self_stool_list = []
            other_stool_list = []
            for self_stool in self.cheese_model:
                self_stool_list.append(self.cheese_model[self_stool])
            for other_stool in other.cheese_model:
                other_stool_list.append(other.cheese_model[other_stool])
            for self_stool in self_stool_list:
                for other_stool in other_stool_list:
                    if other_stool == self_stool:
                        other_stool_list.remove(other_stool)
            if other_stool_list == []:
                return True
        return False
    
    def __str__(self: 'TOAHModel') -> str:       
        """
        Depicts only the current state of the stools and cheese.
        """
        all_cheeses = []
        for height in range(self.number_of_cheeses()):
            for stool in range(self.number_of_stools()):   
                if self._cheese_at(stool,height) is not None:
                    all_cheeses.append(self._cheese_at(stool,height))        
        max_cheese_size = max([c.size for c in all_cheeses]) \
                            if len(all_cheeses) > 0 else 0
        stool_str = "="*(2*max_cheese_size + 1)
        stool_spacing = "  "
        stools_str = (stool_str + stool_spacing) * self.number_of_stools()
        
        def cheese_str(size: int):            
            if size == 0:
                return " " * len(stool_str)
            cheese_part = "-" + "--" * (size - 1)
            space_filler = " " * int((len(stool_str) - len(cheese_part)) / 2)
            return space_filler + cheese_part + space_filler
        
        lines = ""
        for height in range(self.number_of_cheeses() - 1, -1, -1):
            line = ""
            for stool in range(self.number_of_stools()):
                c = self._cheese_at(stool, height)
                if isinstance(c, Cheese):
                    s = cheese_str(int(c.size))
                else:
                    s = cheese_str(0)
                line += s + stool_spacing
            lines += line + "\n"
        lines += stools_str
        
        return lines
    

class Cheese:
    def __init__(self: 'Cheese', size: int):
        """
        Initialize a Cheese to diameter size.

        >>> c = Cheese(3)
        >>> isinstance(c, Cheese)
        True
        >>> c.size
        3
        """
        self.size = size

    def __repr__(self: 'Cheese') -> str:
        """
        Representation of this Cheese
        """
        return "Cheese(" + str(self.size) + ")"

    def __eq__(self: 'Cheese', other: 'Cheese') -> bool:
        """Is self equivalent to other? We say they are if they're the same 
        size."""
        return isinstance(other, Cheese) and self.size == other.size
    
       
class IllegalMoveError(Exception):
    pass

       
class MoveSequence(object):
    def __init__(self: 'MoveSequence', moves: list):
        # moves - a list of integer pairs, e.g. [(0,1),(0,2),(1,2)]
        self._moves = moves
            
    def get_move(self: 'MoveSequence', i: int):
        # Exception if not (0 <= i < self.length)
        return self._moves[i]
        
    def add_move(self: 'MoveSequence', src_stool: int, dest_stool: int):
        self._moves.append((src_stool, dest_stool))
        
    def length(self: 'MoveSequence') -> int:
        return len(self._moves)
    
    def generate_TOAHModel(self: 'MoveSequence', number_of_stools: int, 
                           number_of_cheeses: int) -> 'TOAHModel':
        """
        An alternate constructor for a TOAHModel. Takes the two parameters for
        the game (number_of_cheeses, number_of_stools), initializes the game
        in the standard way with TOAHModel.fill_first_stool(number_of_cheeses),
        and then applies each of the moves in move_seq.
        """
        model = TOAHModel(number_of_stools)
        model.fill_first_stool(number_of_cheeses)
        for move in self._moves:
            model.move(move[0], move[1])
        return model
        
    def __repr__(self: 'MoveSequence') -> str:
        return "MoveSequence(" + repr(self._moves) + ")"


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
