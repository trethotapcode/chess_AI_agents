
class Piece:
    def __init__(self, piece_type, color, position):
        self.piece_type = piece_type  # six types.
        self.color = color            # black / white
        self.position = position

    def move(self, new_position):
        self.position = new_position

    def __str__(self):
        # example: white queen at (0, 3)
        return f"{self.color} {self.piece_type} at {self.position}"

    # debug
    def __repr__(self):
        return self.__str__()


# test_piece
if __name__ == "__main__":
    queen = Piece("Queen", "black", (0, 3))
    print(queen)             # white Queen at (0, 3)
    queen.move((4, 3))
    print(queen)             # white Queen at (4, 3)
