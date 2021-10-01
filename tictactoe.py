import re


class TicTacToe:
    # Constants
    BOARD_SIZE = 3
    EXIT = -1
    EMPTY = 0
    PLAYER1 = 1
    PLAYER2 = 2

    # The symbols:
    # . is empty.
    # O is player 1's choice
    # X is player 2's choice
    # We can change the symbols in this tuple but not the order, if wanted
    TILE_SYMBOL = ('.', 'O', 'X')

    def __init__(self):
        # Create the board as 2d list
        self.board = [[self.TILE_SYMBOL[self.EMPTY] for i in range(self.BOARD_SIZE)] for j in range(self.BOARD_SIZE)]

        # Turn is alternating between 1 and 2 to represent player's turn
        self.turn = self.PLAYER1

        # Map numbers to each tile with dictionary
        # Tile number 1 is board[0][0]
        # Tile number 2 is board[0][1]
        # Tile number 3 is board[0][2]
        # Tile number 4 is board[1][0]
        # and so on...
        self.tiles = {}
        tile_number = 1
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                self.tiles[tile_number] = [i, j]
                tile_number += 1

    def display_board(self):
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                print(self.board[i][j], end="  ")
            print("\n")

    # Get actual position in board by tile number
    def tile_number_to_position(self, tile_number):
        return self.tiles[tile_number]

    def is_valid(self, player_input):
        # Make sure input is in integer type
        pattern = "^[-+]?[0-9]+$"
        if not (re.match(pattern, player_input)):
            print("Invalid input!")
            return False

        player_input = int(player_input)

        # For exit
        if player_input == self.EXIT:
            return True

        # Make sure correct tile number by checking if key is in dictionary
        if player_input not in self.tiles:
            print("Invalid input!")
            return False

        # Make sure the selected tile is empty
        selected_position = self.tile_number_to_position(player_input)
        row = selected_position[0]
        col = selected_position[1]
        if not (self.board[row][col] == self.TILE_SYMBOL[self.EMPTY]):
            print("Invalid move. Tile already occupied!")
            return False

        return True

    def player_move(self, row, col):
        self.board[row][col] = self.TILE_SYMBOL[self.turn]

    def change_turn(self):
        if self.turn == self.PLAYER1:
            self.turn = self.PLAYER2
        else:
            self.turn = self.PLAYER1

    def player_move_by_tile_number(self, tile_number):
        selected_position = self.tile_number_to_position(tile_number)
        row = selected_position[0]
        col = selected_position[1]
        self.player_move(row, col)

    def is_winning(self):
        players_symbol = self.TILE_SYMBOL[self.turn]

        # Check each row
        for i in range(self.BOARD_SIZE):
            occurrence = self.board[i].count(players_symbol)
            if occurrence == self.BOARD_SIZE:
                return True

        # Check each column
        for i in range(self.BOARD_SIZE):
            occurrence = 0
            for j in range(self.BOARD_SIZE):
                if self.board[j][i] == players_symbol:
                    occurrence += 1

            if occurrence == self.BOARD_SIZE:
                return True

        # Check diagonal 1: From bottom left to top right
        row = self.BOARD_SIZE - 1  # Bottom
        col = 0  # Left
        occurrence = 0
        for i in range(self.BOARD_SIZE):
            if self.board[row][col] == players_symbol:
                occurrence += 1
            row -= 1  # Go up
            col += 1  # Go right

        if occurrence == self.BOARD_SIZE:
            return True

        # Check diagonal 2: From top left to bottom right
        row = 0  # Top
        col = 0  # Left
        occurrence = 0
        for i in range(self.BOARD_SIZE):
            if self.board[row][col] == players_symbol:
                occurrence += 1
            row += 1  # Go down
            col += 1  # Go right

        if occurrence == self.BOARD_SIZE:
            return True

        return False

    # If only an empty tile exists, then it is not a draw
    def is_draw(self):
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                if self.board[i][j] == self.TILE_SYMBOL[self.EMPTY]:
                    return False

        return True

    # Check if a tile is empty
    def is_empty(self, row, col):
        if self.board[row][col] == self.TILE_SYMBOL[self.EMPTY]:
            return True
        else:
            return False

    # Call this method to start the game
    def play(self):
        game_over = False

        # Keep looping until a player wins or draw or player choose to exit the game
        while True:
            self.display_board()
            print("Player " + str(self.turn) + "'s turn")
            choice = input("Choice (1-" + str(len(self.tiles)) + ", " + str(self.EXIT) + " to exit the game): ")

            # Validate input
            if not (self.is_valid(choice)):
                # Just give a pause to let the player know about the invalid input
                input()
                continue

            # Should be safe to convert into int now
            choice = int(choice)

            # Player exits the game
            if choice == self.EXIT:
                break

            # Proceeds with player's move
            self.player_move_by_tile_number(choice)

            # Check winning conditions
            if self.is_winning():
                self.display_board()
                print("PLAYER " + str(self.turn) + " WINS!")
                break

            # Check if DRAW: all tiles occupied but no winner yet
            if self.is_draw():
                print("DRAW!")
                break

            # Move to next player
            self.change_turn()


if __name__ == "__main__":
    tictactoe = TicTacToe()
    tictactoe.play()
