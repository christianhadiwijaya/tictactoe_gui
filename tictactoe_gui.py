import tkinter
import tictactoe


class TicTacToeGui:
    # Constants
    CANVAS_WIDTH = 420
    CANVAS_HEIGHT = 420
    CANVAS_BG_COLOR = "grey"
    CANVAS_GRID_COLOR = "black"
    CANVAS_GRID_WIDTH = 2
    INFO_FONT = "Verdana 14 bold"
    PLAYER_1_COLOR = "red"
    PLAYER_2_COLOR = "blue"
    PLAYER_MARK_WIDTH = 5

    def __init__(self):
        self.game_over = False

        # Initiate the core game
        self.tictactoe = tictactoe.TicTacToe()

        # Calculate tile width and height first, so that we don't have to do it many times
        self.tile_width = self.CANVAS_WIDTH / self.tictactoe.BOARD_SIZE
        self.tile_height = self.CANVAS_HEIGHT / self.tictactoe.BOARD_SIZE

        # Prepare the canvas
        self.master = tkinter.Tk()
        self.master.title("TicTacToe")
        self.canvas = tkinter.Canvas(self.master, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT,
                                     bg=self.CANVAS_BG_COLOR)
        self.canvas.pack()

        # Set mouse click listener to canvas
        self.canvas.bind("<Button-1>", self.mouse_clicked)

        # Draw the grid lines
        self.draw_grid()

        # Put in a label at the bottom for information: whose turn, whose win, etc.
        text = "Player " + str(self.tictactoe.turn) + " 's turn"
        self.info = tkinter.Label(self.master, text=text, font=self.INFO_FONT)
        self.info.pack()

    def draw_grid(self):
        # Draw vertical lines
        for i in range(self.tictactoe.BOARD_SIZE - 1):
            x1 = self.CANVAS_WIDTH * (i + 1) / self.tictactoe.BOARD_SIZE
            y1 = 0
            x2 = x1
            y2 = self.CANVAS_HEIGHT
            self.canvas.create_line(x1, y1, x2, y2,
                                    fill=self.CANVAS_GRID_COLOR, width=self.CANVAS_GRID_WIDTH)

        # Draw horizontal lines
        for i in range(self.tictactoe.BOARD_SIZE - 1):
            x1 = 0
            y1 = self.CANVAS_HEIGHT * (i + 1) / self.tictactoe.BOARD_SIZE
            x2 = self.CANVAS_WIDTH
            y2 = y1
            self.canvas.create_line(x1, y1, x2, y2,
                                    fill=self.CANVAS_GRID_COLOR, width=self.CANVAS_GRID_WIDTH)

    # Mouse click listener
    def mouse_clicked(self, event):
        # Get selected row and column
        row = int(event.y // self.tile_height)
        col = int(event.x // self.tile_width)

        self.process_player_move(row, col)

    def mark_tile(self, row, col):
        x1 = self.tile_width * col + self.PLAYER_MARK_WIDTH
        y1 = self.tile_height * row + self.PLAYER_MARK_WIDTH
        x2 = x1 + self.tile_width - self.PLAYER_MARK_WIDTH * 2
        y2 = y1 + self.tile_height - self.PLAYER_MARK_WIDTH * 2

        if self.tictactoe.turn == self.tictactoe.PLAYER1:
            # Player 1: draw circle
            self.canvas.create_oval(x1, y1, x2, y2, outline=self.PLAYER_1_COLOR, width=self.PLAYER_MARK_WIDTH)
        else:
            # Player 2: draw X
            # To draw an X, we need to draw 2 lines
            # First line
            self.canvas.create_line(x1, y1, x2, y2, fill=self.PLAYER_2_COLOR, width=self.PLAYER_MARK_WIDTH)
            # Second line: swap x1 and x2
            temp = x1
            x1 = x2
            x2 = temp
            self.canvas.create_line(x1, y1, x2, y2, fill=self.PLAYER_2_COLOR, width=self.PLAYER_MARK_WIDTH)

    def process_player_move(self, row, col):
        # Ignore player's input if game over
        if self.game_over:
            return

        # Ignore player's input if tile is already occupied
        if not self.tictactoe.is_empty(row, col):
            self.info["text"] = "Tile is already occupied!"
            return

        # Mark the tile as selected
        self.tictactoe.player_move(row, col)
        self.mark_tile(row, col)

        # Check winner
        if self.tictactoe.is_winning():
            self.info["text"] = "PLAYER " + str(self.tictactoe.turn) + " WIN!"
            self.game_over = True
            return

        # Check draw
        if self.tictactoe.is_draw():
            self.info["text"] = "DRAW!"
            self.game_over = True
            return

        # Next player
        self.tictactoe.change_turn()
        self.info["text"] = "Player " + str(self.tictactoe.turn) + "'s turn"


    def play(self):
        self.master.mainloop()


tictactoe_gui = TicTacToeGui()
tictactoe_gui.play()
