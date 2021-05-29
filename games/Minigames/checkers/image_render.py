import os
from PIL import Image
import io

# 0 | b pawn
# 1 | w pawn
# 2 | b queen
# 3 | w queen

nb_to_image = {0: "pieces_00.png", 1: "pieces_01.png", 2: "pieces_02.png", 3: "pieces_03.png"}
rel_abs_pos = {1: [0, 1], 2: [0, 3], 3: [0, 5], 4: [0, 7], 5: [1, 0], 6: [1, 2], 7: [1, 4], 8: [1, 6], 9: [2, 1],
               10: [2, 3], 11: [2, 5], 12: [2, 7], 13: [3, 0], 14: [3, 2], 15: [3, 4], 16: [3, 6], 17: [4, 1],
               18: [4, 3], 19: [4, 5], 20: [4, 7], 21: [5, 0], 22: [5, 2], 23: [5, 4], 24: [5, 6], 25: [6, 1],
               26: [6, 3], 27: [6, 5], 28: [6, 7], 29: [7, 0], 30: [7, 2], 31: [7, 4], 32: [7, 6]}


board_image = "board_00.png"
subdirectory = "Minigames/checkers/images/"

def render(game):
    img = Image.open(os.path.join(os.path.abspath(''),  subdirectory + board_image))
    for piece in game.board.pieces:
        if piece.captured:
            continue
        n = 0
        if piece.player == 1:
            n = 0
            if piece.king:
                n = 2
        elif piece.player == 2:
            n = 1
            if piece.king:
                n = 3
        p = piece.position
        x, y = rel_abs_pos[p]
        piece = Image.open(os.path.join(os.path.abspath(''), subdirectory + nb_to_image[n]))
        img.paste(piece, (40 + y * 150, 50 + x * 150), piece)

    file = io.BytesIO()
    img.save(file, format="PNG")
    file.seek(0)
    return file
