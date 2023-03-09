from constants import infinity
from board2 import Board
import math
import random

class Minimax():
    
    def __init__(self, board):
        # inherits the board on which it will perform its decisions
        self.board = board
      

    
    def opposite_edge(self,player_number):
        """we will find the opposite corner for a particular player"""
        if player_number == 1:
            #return self.board.board_size -1, self.board.board_size -1
            return 7,7
        elif player_number == 2:
            return 0,0
    
    def field_strength(self,x1, y1, x2, y2):
        """We will calculate the field_strength between 2 points on the board"""
        return ((x1-x2)**2+ (y1-y2)**2)



    def evaluation_funct(self, board,player_number):
        """We will find the state's field strength from all the pegs as the evaluation function"""
        field = 0
        # we check if the game was won, then the function will return 0
        if board.game_won() == player_number:
            return 0

        #the function loops through all the positions
        for i in range(board.board_size):
            for j in range(board.board_size):
                # checks if the position has a player's peg
                if board.state[i][j] == player_number:
                    # add the field strength to the overall evaluation 
                    field_strength = self.field_strength(i,j,self.opposite_edge(player_number)[0], self.opposite_edge(player_number)[1])
                    field += field_strength

        return field
    
    def increase_position(self,x,y, z, t, player_number):
        """Analyse if a move brings a peg closer to the opposite edge"""
        if z+t >= x + y and player_number ==1:
            return True
        if z + t <= x + y and player_number == 2:
            return True
        return False


    def possible_moves(self, board, player_number):
        """The function returns a list of all the possible moves that a player has"""
        possible_moves =[]
        for i in range(board.board_size):
            for j in range(board.board_size):
                if board.state[i][j] == player_number:
                    """If a square has one of the player's peg, we consider all the moves that peg can do"""
                    if len(board.all_valid_moves(i,j)) != 0: 
                        valid_moves = board.all_valid_moves(i,j)

                        for x,y in valid_moves:
                            if self.increase_position(i,j,x,y,player_number):
                                """If this move, brings the player closer to the opposite corner, then we append it to the list"""
                                possible_moves.append((i,j,x,y))

                    
        return possible_moves


# doing the minimax for a particular state, maximizing one player and looking depth moves up front

    def minimax(self, board, depth, alpha, beta,  maximizing_player): 
        """we are doing the minimax algorithm on the game
           the function will return the evaluation of the board and also the best move available     
                """
        """adding an alpha and beta, that holds the current best position for the maximizing and minimizing"""

        # if we reach a leaf, then the function returns the board evaluation
        if depth == 0:
            return self.evaluation_funct(board,  int(maximizing_player)+1), None
        
        # the function searches the best move for the maximizing player
        if maximizing_player :
            # the best move will give the lowest board evaluation, therefore I set the initial minimum to be very big
            mn = infinity
            best_move =(None,None,None,None)
            # the function loops through all the possible moves
            for x,y,z,t in self.possible_moves(board,2):
                # the move is performed
                board.move(x,y,z,t,2)
                # if this move wins the game, then it will be returned with the evaluation 0
                if board.game_won() == 2:
                    board.move(z,t,x,y,2)
                    return 0, (x,y,z,t)
                #we search the best move we can get, if we did the (x,y,z,t) move, the depth will be decreased, and we will have the minimizing player
                value = self.minimax(board, depth-1, alpha, beta, not maximizing_player)[0]
                # the move will be reversed to not corrupt the board
                board.move(z,t,x,y,2)
                # if the value obtained from this branch is smaller than the minimum, it will become the minimum and the best move will be updated
                if  value <= mn:
                    mn = value
                    best_move =(x,y,z,t)
                #alpha will be updated
                alpha = max(alpha,mn)

                # if alpha is bigger than beta, then this branch will the dominated by the second player, therefore we will break and not look at other possible branches generated by the moves
                if beta <= alpha:
                    break

                
            # return the best always possible board evaluation after depth moves and the first move to ensure it will happen  
            return mn, best_move

        # the algorithm will find the maximum always adttainable minimum for the minimizing player 
        if not maximizing_player:
            #the innitial maximum will be very small
            mx = -infinity
            best_move =(None,None,None,None)
            # the function loops through all the possible moves
            for x,y,z,t in self.possible_moves(board,1):
                # the move is performed
                board.move(x,y,z,t,1)
                 # if this move wins the game, then it will be returned with the evaluation 0
                if board.game_won() == 1:
                    board.move(z,t,x,y,1)
                    return 0, (x,y,z,t)
                #we search the best move we can get, if we did the (x,y,z,t) move, the depth will be decreased, and we will have the maximizing player
                value = self.minimax(board, depth-1,alpha, beta, not maximizing_player)[0]
                # the move will be reversed to not corrupt the board
                board.move(z,t,x,y,1)
                # if the value obtained from this branch is bigger than the minimum, it will become the minimum and the best move will be updated
                if  value >= mx:
                    mx = value
                    best_move = (x,y,z,t)
                #beta will be updated
                beta = min(beta, mx)

                 # if alpha is bigger than beta, then this branch will the dominated by the other player, therefore we will break and not look at other possible branches generated by the moves
                if beta <= alpha:
                    break
            # return the best always possible board evaluation after depth moves and the first move to ensure it will happen  
            return mx, best_move


if __name__ == '__main__':
    b=Board(8)
    Mx= Minimax(b)

    b. state =[[2, 2, 2, 0, 0, 0, 0, 0], [2, 0, 0, 0, 0, 0, 0, 0], [0, 2, 0, 0, 0, 0, 0, 0], 
    [0, 2, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 1, 1, 1], 
    [0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0]]
    print(b.game_won())
    print(b.possible_moves(2))
    print(Mx.evaluation_funct(b,2))
    print(Mx.minimax(b, 4, -infinity, infinity, True))
