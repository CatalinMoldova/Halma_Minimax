from board2 import Board
import tkinter as tk
from tkinter import Radiobutton
from minimax import Minimax
from constants import infinity
from board2 import Board
import threading
from PIL import Image
from tkinter import RIGHT, Scrollbar, Listbox, ttk
class Display(tk.Tk):

    #the board parameters
    WIDTH = 960
    HEIGHT = 480
    EXT_RADIUS = 6

    def __init__(self, board) :
        tk.Tk.__init__(self)
        self.board = board

        # Set window traits.
        self.geometry('635x500')
        self.resizable(False, False)
        # create the canvas on which methods will operate
        self.canvas = tk.Canvas(self, width=Display.WIDTH, height=Display.HEIGHT, bg ="light grey")
        self.canvas.grid()
        
        # a variable for maintaining if we have clicked on a peg
        self.clicked = False
        # variable for keeping trakc of the current player
        self.player_number = 1

        # variable of the peg which will move
        self.peg_to_move = (None,None)
        # variable of the next position of the peg
        self.next_pos = (None,None)

        # variable to check if the first move has been performed
        self.first_move = False

        # variable for the type of opponent
        self.CPU_player = tk.StringVar()

        # initialization of the new game button
        self.New_Game = tk.Button(self.canvas, text='New Game', command = self.new_game, state = "disabled")
        self.New_Game.place(x= 500, y= 100)

        # button for opening the rules
        rules_button = tk.Button(self.canvas, width=10, height=2, text ='Rules', command=lambda: self.rules_window())
        rules_button.place(x=500, y=400)
        
        # bind the click with the function
        self.canvas.bind("<Button-1>", self.peg_click)

        # showing information about the game
        bt0 =tk.Label(self.canvas, text= f"Player 1 is red \nPlayer 2 is blue", font=('Helvetica 12 underline'))
        bt0.pack(pady=20)
        bt0.place(x=488, y=30)

        # showing opponent information
        bt1 = tk.Label(self.canvas, text= f"Select opponent", font=('Helvetica 12 underline'))
        bt1.pack(pady=20)
        bt1.place(x=488, y=160)

        #defining radio button for the opponent selection
        self.CPU_player.set(0)
        self.rb_CPU_1 = tk.Radiobutton(self.canvas, text = 'Human', value=0, variable=self.CPU_player)
        self.rb_CPU_1.place(x=500, y= 200)
        self.rb_CPU_1 = tk.Radiobutton(self.canvas, text = 'CPU', value=1, variable=self.CPU_player)
        self.rb_CPU_1.place(x=500, y= 225)

        #draw the cells of the table
        self.draw_cells()

    def draw_cells(self):
        # the colours which will be in the squares
        colours = {0:'white', 1: 'red', 2:'blue'}
        side = Display.HEIGHT / len(self.board.state)
        for i,row in enumerate(self.board.state):
            for j, state in enumerate(row):
                self.draw_rectangle( j * side, i*side, side,'white')
                self.draw_circle( j * side + side//2,  i*side + side//2, side//2 - self.EXT_RADIUS, colours[state])

    def draw_circle(self, x, y, r, color):       
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill = color)
        
    def draw_rectangle(self, x, y, side, fill):        
        self.canvas.create_rectangle(x, y, x+side, y+side, fill=fill)
    
    def new_game(self):
        self.New_Game.config(state="disabled")
        print("End game")
        # set the game to the innitial player
        self.player_number = 1 
        # move all the pegs to their innitial position
        self.board.new_table()
        # draw the peggs in their respective place
        self.draw_cells()

    # this function prints on the display which player has won the game
    def you_win(self, player_number):
        self.canvas.create_text(240, 240, text=f'Player {player_number} Wins!', fill="black", font=('Helvetica 30 bold'), )
    

        # ends the current move   
    def end_move(self, board):
        if board.game_won() == (1 or 2):
            print(f'Player{board.game_won()} won')
            #prints the board label
            self.you_win(board.game_won())
        # changes the player number    
        self.player_number = 3 - self.player_number 
        self.clicked = False
        print(f'The current player is {self.player_number}')
        # change between players 1 and 2

    # this function draws a black dot on the selected peg
    def selected_peg_black_dot(self, event):
        side = Display.HEIGHT / len(self.board.state)
        if event[1] < 480:
            self.draw_circle(event[1], event[0], 2*self.EXT_RADIUS, 'black')
    
     # this function draws an yellow dot on a peg's possible moves
    def possible_pegs_yellow_dot(self, peg_r, peg_c):
        for row, col in self.board.all_valid_moves(peg_r, peg_c):
            self.draw_circle(60*col+30, 60*row+30, 2*self.EXT_RADIUS, 'yellow')
            print(row, col, self.board.state[row][col])
    
        # the function that does the computer moves
    def CPU_peg_move(self):
        # innitialise the algorithm
        M =Minimax(self.board.board_size)
        # check if the CPU player is moving
        if self.player_number == 2 :
            # gets the best move and does it
            best_move = M.minimax(self.board, 4, -infinity, infinity,  True)[1]
            x,y,z,t = best_move
            self.board.move(x,y,z,t,2)
            self.draw_cells()
            self.end_move(self.board)
    
    # get the integer coordinates
    def get_coordinates(self, event):
        return (event.y//60, event.x//60)

    # return the middle of a square
    def middle(self, event):
        return int(event.y//60)*60+30, int(event.x//60)*60+30 
    
    def spawn(self):
        thread = threading.Thread(target=self.CPU_peg_move())
        thread.start()

    def peg_click(self, event):
        
        # checks if the game is still in play
        if self.board.game_won() != None:
            return None

        # code which helped the debugging
        print(f'DEBUG: GUI.canvas_click called {event.x=} {event.y=}')


        # if player is human
        #get the coordinates of the mouse click
        row, col = self.get_coordinates(event)
        if (self.player_number == 1 or int(self.CPU_player.get()) == 0) and row <=7 and col <=7:
            if self.clicked == False:
                # if the player chooses his own peg
                if self.board.state[row][col] == self.player_number :
                    # the value of the peg that will be moved is updated
                    self.peg_to_move = (row,col)            
                    self.selected_peg_black_dot(self.middle(event))
                    # draw the possible final states
                    self.possible_pegs_yellow_dot(row, col)
                    #code for debugging
                    print(f'Selected peg is {self.peg_to_move}')
                    # there is a clicked peg, therefore clicked is true
                    self.clicked = True
                
                else:
                    # If the player does not choose his own peg, nothing will happen
                    print("Press your peg")
                    print(self.clicked)
                
            elif  self.clicked == True:
                
                # the clicked peg will be thenext position of the previously selected peg
                self.next_pos = self.get_coordinates(event)
                # the following lines reselect the peg that will be moved
                if self.board.state[self.next_pos[0]][ self.next_pos[1]] == self.player_number :
                    row, col = self.next_pos[0],  self.next_pos[1]
                    self.peg_to_move = (row, col)
                    self.draw_cells()
                    self.selected_peg_black_dot(self.middle(event))
                    self.possible_pegs_yellow_dot(row, col)

                # if the user tries to do an invalid move, then it will be denied
                elif self.next_pos not in self.board.all_valid_moves(self.peg_to_move[0], self.peg_to_move[1]):
                    print('Press an available square')

                #the move will happen
                else:
                    # the board's state will be updated
                    self.board.move(self.peg_to_move[0], self.peg_to_move[1], self.next_pos[0], self.next_pos[1], self.player_number)
                    self.first_move = True
                    self.New_Game.config(state="normal")
                    print(f'peg moved to{self.next_pos}')
                    self.draw_cells()
                    self.end_move(self.board)
        
        # if it is the computer's move    
        if self.player_number == 2 and int(self.CPU_player.get()) == 1:
            #thread to perform the CPU move
            if self.board.game_won() == None:
                self.spawn()
        
        #show the congratulations message
        if self.board.game_won() != None:
            self.you_win(self.board.game_won())
    
    def rules_window(self):
        # create the new root for the rules
        self.root = tk.Toplevel()
        root = self.root
        #set the root's properties
        root.geometry("800x800")
        root.config(bg='tan')
        root.resizable(False, False)
        root.title('Rules Page')
        image = tk.PhotoImage(file="Halma_Rules.gif")
        # subsampling, shrinking the image size in half
        image = image.subsample(2)
        newcanvas = tk.Canvas(root, height = 800, width = 800)
        newcanvas.create_image(500,1500,image=image)
        # the command links the scroll bar action to the scrolling action of the canvas
        scroll = tk.Scrollbar(root, orient="vertical", command=newcanvas.yview)
        #puts the scroll on the right
        scroll.pack(side="right",fill=tk.Y)
        # the scroll region converts the canvas into scrollable canvas
        newcanvas.config(yscrollcommand = scroll.set, scrollregion=newcanvas.bbox(tk.ALL))
        newcanvas.pack()

        root.mainloop()
        """
        tk.Label(root, image=image).pack(side = "bottom", fill = "both", expand = "yes")
        """

        
        """canvas =tk.canvas(root,bg="blue", height=800, width=1000)
        img = tk.PhotoImage(file="Halma_Rules.gif")
        canvas.create_image(0,0,image=img, anchor="nw")
        canvas.config(scrollregion=canvas.bbox(tkinter.ALL))

       
        #tk.Label(root, image=image).pack(side = "left", fill = "both", expand = "yes")

        scroll_bar = Scrollbar(root)
  
        scroll_bar.pack( side = RIGHT,fill = Y )
   
        mylist = Listbox(root, yscrollcommand = scroll_bar.set )
        
        mylist.insert(0,)
        scroll_bar.config( command = mylist.yview )
    """
    """    


class RulesWindow():
    #window that displays the rules of the game
    
    def __init__(self):
        self.root = tk.Toplevel()
        root = self.root
        root.geometry("2481x3508")
        root.config(bg='tan')
        root.resizable(False, False)
        root.title('Rules Page')
        
        image = tk.PhotoImage(file="Halma_Rules.gif")
        tk.Label(root, image=image).pack(side = "bottom", fill = "both", expand = "yes")

        scroll_bar = Scrollbar(root)
  
        scroll_bar.pack( side = RIGHT,fill = Y )
   
        mylist = Listbox(root, yscrollcommand = scroll_bar.set )
        
        scroll_bar.config( command = mylist.yview )

        resize_image = image.resize((800, 1000))
        img = ImageTk.PhotoImage(resize_image)
        
        tk.Label(root, image=image).pack(side = "bottom", fill = "both", expand = "yes")
        label1 = Label(image=img)
        label1.image = img
        label1.pack()
        root.mainloop()
"""