class Board():

    def __init__(self, board_size):
        """We initialise the board size, and set the state as a square matrix of length board_size"""
        self.board_size = board_size
        self.state = [[0 for i in range(self.board_size)] for j in range(self.board_size)]

    
    def new_table(self):
        """We inititialize the starting position of the game"""
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.state[i][j] = 0
        """We set the initial arrangement of pegs on the edges"""
        for i in range(self.board_size):
            for j in range(self.board_size):
                if i + j <= self.board_size//3 and i <= self.board_size//3 and j <= self.board_size//3:
                    self.state[i][j] = 1
                    """We use symmetry to arrange the opposite pegs"""
                    self.state[self.board_size-1-i][self.board_size-1-j] = 2

        
    def move(self, peg_r, peg_c, nextpos_r, nextpos_c, player_number):
        """we define a move by changing the value of the a position in the matrix to the player_number, indicating we have a peg"""
        self.state[peg_r][peg_c] = 0
        self.state[nextpos_r][nextpos_c] = player_number

    def after_jump(self, r1, c1, r2, c2):
        """The function returns the postion of the peg who started at (r1,c1) after it jumped over (r2,c2)"""
        """The next two return the position for a vertical jump"""
        if r1 == r2 and c1+1 == c2 and c1<self.board_size-2:
            return (r1,c1+2)
        if r1 == r2 and c1-1 == c2 and c1 > 1:
            return (r1,c1-2)
        """The next two return the position for a horizontal jump"""
        if r1+1 == r2 and c1 == c2 and r1 < self.board_size-2:
            return (r1+2,c1) 
        if r1-1 == r2 and c1 == c2 and r1 >1 and c1 < self.board_size-1:
            return (r1-2,c1)
        """The next two return the position for a diagonal jump"""
        if r1+1 == r2 and c1+1 == c2 and c1 < self.board_size-2 and r1 < self.board_size-2:
            return (r1+2,c1+2) 
        if r1-1 == r2 and c1+1 == c2 and c1 < self.board_size-2 and r1 > 1:
            return (r1-2,c1+2)
        if r1+1 == r2 and c1-1 == c2 and r1 < self.board_size-2 and c1 > 1:
            return (r1+2,c1-2) 
        if r1-1 == r2 and c1-1 == c2 and r1 > 1 and c1 > 1:
            return (r1-2,c1-2)
        
        return None

    def adjacent_positions (self, peg_r, peg_c):
        """This function returns the list of all adjacent squares to (peg_r, peg_c)"""
        self.peg_r = peg_r
        self.peg_c = peg_c
        """We will store all the adjacent positions in a list"""
        adjacent_set = []

        """If (peg_r,peg_c) neighbour is on the board, it will append it to the list"""

        """The next 2 IF clauses check the horizontal neighbours"""
        if self.peg_r > 0:
            adjacent_set.append((self.peg_r-1,self.peg_c))

        if self.peg_r < self.board_size-1 :
            adjacent_set.append((self.peg_r+1,self.peg_c))

        """The next 2 IF clauses check the horizontal neighbours"""
        if self.peg_c > 0:
            adjacent_set.append((self.peg_r,self.peg_c-1))

        if self.peg_c < self.board_size-1:
            adjacent_set.append((self.peg_r,self.peg_c+1))

        """The next 4 IF clauses check the diagonal neighbours"""
        if self.peg_r > 0 and self.peg_c > 0:
            adjacent_set.append((self.peg_r-1,self.peg_c-1))

        if self.peg_r < self.board_size-1  and self.peg_c > 0:
            adjacent_set.append((self.peg_r+1,self.peg_c -1))

        if self.peg_r > 0 and self.peg_c < self.board_size-1:
            adjacent_set.append((self.peg_r-1,self.peg_c +1))

        if self.peg_r < self.board_size-1 and self.peg_c < self.board_size-1:
            adjacent_set.append((self.peg_r+1,self.peg_c +1))
        
        return adjacent_set


    def available_simple_moves(self, peg_r, peg_c):
        """The function returns a list of the simple moves that a peg can move"""
        available_set = []
        """I will loop through all the neighbours and append the ones which are free"""
        for x, y in self.adjacent_positions(peg_r, peg_c):
            if self.state[x][y] == 0 :
                available_set.append((x,y))
        return available_set
    
    def available_jump_moves(self, peg_r, peg_c):
        """The function returns a list of the jumps move that peg can make"""
        available_set = []

        """We will loop through the peg's neighbor squares"""
        for x, y in self.adjacent_positions(peg_r, peg_c):
            
            """We will check if the neigboring square has a peg"""
            if self.state[x][y] != 0  and self.after_jump(peg_r,peg_c,x,y) !=None:
                a, b = self.after_jump(peg_r,peg_c,x,y) 
                """If the after_jump is empty, then the peg can perform this jump move"""
                if self.state[a][b] == 0:
                    available_set.append((a, b))
        
        return available_set
    
    def get_jumps(self, position, jumps, last_position):
        """This function receives a list jumps, with position and last_position, 
        and return the jumps list with all the available jumps we can perform
        from position   and returns it with the other available jump moves
        """

        """We look what jumps we can make from our current position"""
        available_jumps = self.available_jump_moves(position[0], position[1])

        """We remove the last position of the jumps, because it already is in the jumps list"""
        try:
            available_jumps.remove((last_position[0],last_position[1]))
        except:
            pass
        
        if (len(available_jumps) ==  0):
            return jumps
        else:
            #we iterate through the available Jumps
            for i in range (len(available_jumps)):
                # we can perform this jump, therefore if it is not in jumps, we append it to jumps
                if available_jumps[i] not in jumps:
                    jumps.append(available_jumps[i])
                    #we recursively search the available jumps from this new position
                    self.get_jumps(available_jumps[i], jumps, position)
        return jumps

    def all_valid_moves(self, peg_r, peg_c):
        """The function returns all the valid moves for the peg at position(peg_r, peg_c)"""
        # Available_positions is initialized as a list with the available simple moves
        # The other available moves will be appended to available_positions
        available_positions = self.available_simple_moves(peg_r, peg_c)
        #available_jumps is the first set I use for generating all the final jump positions
        available_jumps = self.available_jump_moves(peg_r, peg_c)

        """We will append the final positions of the jump moves to the available_position list, by using the function get_jumps"""

        """We append each jump in available_jumps to the available_positions"""
        if len(available_jumps) > 0:
            for i in range(len(available_jumps)):
                #every element in available_jumps will be added to the available_positions
                # as available_positions is a list, we need to check if the position is already in a list
                if available_jumps[i] not in available_positions:
                    available_positions.append(available_jumps[i])
                """the get_jumps function will return the final position of all the jump moves
                after performing these jumps
                """
                jumps =[]
                self.get_jumps(available_jumps[i], jumps, (peg_r,peg_c))
                if len(jumps) > 0 :
                    for i in range (len(jumps)):
                        # we will append every position in jumps to the available_positions list
                        if jumps[i] not in available_positions:
                            available_positions.append(jumps[i])
                            
        return available_positions 





    def game_won(self): 
        """This function checks if the game has been won"""
        # we initialise 2 variables which will change two false if the statement is wrong
        player_1_won = True
        player_2_won = True
        #we will check if all the corner pegs are of the opposite color, if not then the won variable will be false
        for i in range(self.board_size):
            for j in range(self.board_size):
                if i + j <= self.board_size//3 and i <= self.board_size//3 and j <= self.board_size//3:
                    if self.state[i][j] != 2:
                        player_2_won = False
                    if self.state[self.board_size-1-i][self.board_size-1-j] != 1:
                        player_1_won = False
        # if a player has won, the function will return the player number, else None
        if player_1_won:
            return 1
        if player_2_won:
            return 2
        return None

    """def possible_moves(self, player_number):
        #The function returns a list of all the possible moves that a player has
        possible_moves =[]
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.state[i][j] == player_number:
                    #If a square has one of the player's peg, we consider all the moves that peg can do
                    if len(self.all_valid_moves(i,j)) != 0: 
                        valid_moves = self.all_valid_moves(i,j)

                        for x,y in valid_moves:
                            if self.increase_position(i,j,x,y,player_number):
                                #If this move, brings the player closer to the opposite corner, then we append it to the list
                                possible_moves.append((i,j,x,y))

                    
        return possible_moves


    def increase_position(self,x,y, z, t, player_number):
        #Analyse if a move brings a peg closer to the opposite edge
        if z+t >= x + y and player_number ==1:
            return True
        if z + t <= x + y and player_number == 2:
            return True
        return False"""
    

"""class Move(Board):

    def __init__(self):
        self.path= 
        self.dest = 
        pass
"""
if __name__ == '__main__':

    B = Board(8)
    B.new_table()
    
    print(B.get_jumps((1,1),[],None))
    #print(B.after_jump(0,0,1,0))
    print(B.state)
    
