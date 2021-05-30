import io
import os

from PIL import Image

# 0 | b king
# 1 | b queen
# 2 | b bishop
# 3 | b horse
# 4 | b rook
# 5 | b pawn

# 6 | w king
# 7 | w queen
# 8 | w bishop
# 9 | w horse
# 10| w rook
# 11| w pawn

nb_to_image = {"P": "pieces_11.png", "B": "pieces_08.png", "k": "pieces_00.png", "q": "pieces_01.png", "b": "pieces_02.png",
               "n": "pieces_03.png", "r": "pieces_04.png", "p": "pieces_05.png", "K": "pieces_06.png", "Q": "pieces_07.png",
               "N": "pieces_09.png", "R": "pieces_10.png"}

board_image = "board_00.png"
subdirectory = "Minigames/chess/images/"

def render(board):
    img = Image.open(os.path.join(os.path.abspath(''),  subdirectory + board_image))
    j = -1
    k = 0
    for i in range(64):
        if i % 8 == 0:
            j += 1
            k = 0
        if board.piece_at(i) is None:
            k += 1
            continue
        piece = Image.open(os.path.join(os.path.abspath(''), subdirectory + nb_to_image[str(board.piece_at(i))]))
        img.paste(piece, (40+k*150, 50+j*150), piece)
        k += 1
    file = io.BytesIO()
    img.save(file, format="PNG")
    file.seek(0)
    return file
