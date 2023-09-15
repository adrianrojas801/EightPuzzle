#
# searcher.py (Final project)
#
# classes for objects that perform state-space search on Eight Puzzles  
#
# name: Adrian Rojas
# email: rojasa@bu.edu
#
# If you worked with a partner, put their contact info below:
# partner's name:
# partner's email:
#

import random
from state import *

class Searcher:
    """ A class for objects that perform random state-space
        search on an Eight Puzzle.
        This will also be used as a superclass of classes for
        other state-space search algorithms.
    """
    ### Add your Searcher method definitions here. ###
    def __init__(self, depth_limit):
        """ constructs a new Searcher object
        """
        self.states = []
        self.num_tested = 0 
        self.depth_limit = depth_limit


    def add_state(self, new_state):
        """ takes a single State object called new_state and adds it 
            to the Searcher‘s list of untested states
        """
        self.states += [new_state]
        
    
    def should_add(self, state):
        """ takes a State object and returns True if the called Searcher 
            should add state to its list of untested states, and False 
            otherwise
        """
        if self.depth_limit != -1:
            if state.num_moves > self.depth_limit:
                return False
        if state.creates_cycle() == True:
            return False
        else:
            return True


    def add_states(self, new_states):
        """ takes a list State objects and processes the elements of 
            new_states one at a time to see if a given state should be added 
            to the Searcher‘s list of untested states and if a given state 
            should not be added to the Searcher object’s list of states
        """
        for s in new_states:
            if self.should_add(s) == True:
                self.add_state(s)


    def next_state(self):
        """ chooses the next state to be tested from the list of 
            untested states, removing it from the list and returning it
        """
        s = random.choice(self.states)
        self.states.remove(s)
        return s
    
    
    def find_solution(self, init_state):
        """ performs a full search that begins at the specified initial state, 
            init_state, and ends when the goal state is found, returning the state,
            or when the Searcher runs out of untested states, returning None,
        """
        self.add_state(init_state)
        while self.states != []:
            s = self.next_state()
            self.num_tested += 1
            if s.is_goal() == True:
                return s
            else:
                self.add_states(s.generate_successors())
        return None


    def __repr__(self):
        """ returns a string representation of the Searcher object
            referred to by self.
        """
        # You should *NOT* change this method.
        s = type(self).__name__ + ': '
        s += str(len(self.states)) + ' untested, '
        s += str(self.num_tested) + ' tested, '
        if self.depth_limit == -1:
            s += 'no depth limit'
        else:
            s += 'depth limit = ' + str(self.depth_limit)
        return s


### Add your BFSeacher and DFSearcher class definitions below. ###
class BFSearcher(Searcher):
    """ Class that performs breadth-first search (BFS)
    """
    def next_state(self):
        """ follow first-in first-out ordering by choosing the state that 
            has been in the list the longest and removes it from the 
            untested states and returns it
        """
        s = self.states[0]
        self.states.remove(s)
        return s
    
    
class DFSearcher(Searcher):
    """ Class that performs depth-first search (DFS)
    """
    def next_state(self):
        """ follow last-in first-out ordering by choosing the state that 
            has been in the list the shortest and removes it from the 
            untested states and returns it
        """
        s = self.states[-1]
        self.states.remove(s)
        return s


def h0(state):
    """ a heuristic function that always returns 0 """
    return 0

### Add your other heuristic functions here. ###
def h1(state):
    """ a heuristic function that computes and returns an estimate of how 
        many additional moves are needed to get from state to the goal state
    """
    return state.board.num_misplaced()

def h2(state):
    """ a heuristic function that computes and returns an estimate of how 
        far away the misplaced tiles are from their goal state. 
    """
    return state.board.how_far()

class GreedySearcher(Searcher):
    """ A class for objects that perform an informed greedy state-space
        search on an Eight Puzzle.
    """
    ### Add your GreedySearcher method definitions here. ### 
    def __init__(self, heuristic):
        """ constructs a new GreedySearcher object
        """
        super().__init__(-1)
        self.heuristic = heuristic


    def priority(self, state):
        """ computes and returns the priority of the specified state,
            based on the heuristic function used by the searcher
        """
        return -1 * self.heuristic(state)
    
    
    def add_state(self, state):
        """ adds a sublist that is a pairing of each state with its priority
            to states list
        """
        pair = [self.priority(state), state]
        self.states += [pair]
        
        
    def next_state(self):
        """ chooses one of the states with the highest priority, returning 
            the state component of the sublist
        """
        s = max(self.states)
        self.states.remove(s)
        return s[1]


    def __repr__(self):
        """ returns a string representation of the GreedySearcher object
            referred to by self.
        """
        # You should *NOT* change this method.
        s = type(self).__name__ + ': '
        s += str(len(self.states)) + ' untested, '
        s += str(self.num_tested) + ' tested, '
        s += 'heuristic ' + self.heuristic.__name__
        return s


### Add your AStarSeacher class definition below. ###
class AStarSearcher(GreedySearcher):
    """ A class for objects that perform an informed priority state-space
        search on an Eight Puzzle
    """
    def priority(self, state):
        """ computes and returns the priority of the specified state,
            based on the heuristic function used by the searcher and 
            takes into account the number of moves to that state
        """
        return -1 * (self.heuristic(state) + state.num_moves)
