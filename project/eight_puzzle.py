#
# eight_puzzle.py (Final project)
#
# driver/test code for state-space search on Eight Puzzles   
#
# name: Adrian Rojas
# email: rojasa@bu.edu
#
# If you worked with a partner, put their contact info below:
# partner's name:
# partner's email:
#

from searcher import *
from timer import *

def create_searcher(algorithm, param):
    """ a function that creates and returns an appropriate
        searcher object, based on the specified inputs. 
        inputs:
          * algorithm - a string specifying which algorithm the searcher
              should implement
          * param - a parameter that can be used to specify either
            a depth limit or the name of a heuristic function
        Note: If an unknown value is passed in for the algorithm parameter,
        the function returns None.
    """
    searcher = None
    
    if algorithm == 'random':
        searcher = Searcher(param)
## You will uncommment the following lines as you implement
## other algorithms.
    elif algorithm == 'BFS':
        searcher = BFSearcher(param)
    elif algorithm == 'DFS':
        searcher = DFSearcher(param)
    elif algorithm == 'Greedy':
        searcher = GreedySearcher(param)
    elif algorithm == 'A*':
        searcher = AStarSearcher(param)
    else:  
        print('unknown algorithm:', algorithm)

    return searcher

def eight_puzzle(init_boardstr, algorithm, param):
    """ a driver function for solving Eight Puzzles using state-space search
        inputs:
          * init_boardstr - a string of digits specifying the configuration
            of the board in the initial state
          * algorithm - a string specifying which algorithm you want to use
          * param - a parameter that is used to specify either a depth limit
            or the name of a heuristic function
    """
    init_board = Board(init_boardstr)
    init_state = State(init_board, None, 'init')
    searcher = create_searcher(algorithm, param)
    if searcher == None:
        return

    soln = None
    timer = Timer(algorithm)
    timer.start()
    
    try:
        soln = searcher.find_solution(init_state)
    except KeyboardInterrupt:
        print('Search terminated.')

    timer.end()
    print(str(timer) + ', ', end='')
    print(searcher.num_tested, 'states')

    if soln == None:
        print('Failed to find a solution.')
    else:
        print('Found a solution requiring', soln.num_moves, 'moves.')
        show_steps = input('Show the moves (y/n)? ')
        if show_steps == 'y':
            soln.print_moves_to()


def process_file(filename, algorithm, param):
    """ opens the specified fileand processes the file one line at a time 
        obtaining the digit string on that line,takes the steps to solve the 
        eight puzzle for that digit string using the algorithm and reports the 
        number of moves in the solution, the number of states tested during 
        the search for the solution, number of puzzles solved, the average 
        number of moves in the solutions, and the average number of states 
        tested
    """
    file = open(filename, 'r')
    count = 0
    moves = []
    states = []
    for line in file:
        string = line[:-1]
        init_board = Board(string)
        init_state = State(init_board, None, 'init')
        searcher = create_searcher(algorithm, param)
        if searcher == None:
            return
        soln = None
        try:
            soln = searcher.find_solution(init_state)
        except KeyboardInterrupt:
            print('search terminated, ', end='')
        if soln == None:
            print('no solution')
        else:
            count +=1
            moves += [soln.num_moves]
            states += [searcher.num_tested]
            print(string + ':', soln.num_moves, 'moves,', searcher.num_tested, 'states tested')
    print()
    print('solved', count, 'puzzles')
    if count > 0:
        mavg = sum(moves)/len(moves)
        savg = sum(states)/len(states)
        print('averages:', mavg, 'moves,', savg, 'states tested')
    file.close()
