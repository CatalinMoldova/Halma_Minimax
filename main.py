from board2 import Board
from GUI2 import Display

if __name__ == '__main__':
    b=Board(8)
    b.new_table()
    display = Display(b)
    display.mainloop()

