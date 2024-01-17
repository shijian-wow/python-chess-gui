import pyautogui

client_screen_size = pyautogui.size()
client_screen_x_length = client_screen_size[0]
client_screen_y_length = client_screen_size[1]


width, height = 600, 600


import os
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{int(client_screen_x_length / 2 - width / 2)},{int(client_screen_y_length / 2  - height / 2)}"


import pygame
import chess
import chess.engine
import sys


white_pawn   = pygame.image.load('./assets/white_pawn.png')
white_bishop = pygame.image.load('./assets/white_bishop.png')
white_knight = pygame.image.load('./assets/white_knight.png')
white_rook   = pygame.image.load('./assets/white_rook.png')
white_queen  = pygame.image.load('./assets/white_queen.png')
white_king   = pygame.image.load('./assets/white_king.png')

black_pawn   = pygame.image.load('./assets/black_pawn.png')
black_bishop = pygame.image.load('./assets/black_bishop.png')
black_knight = pygame.image.load('./assets/black_knight.png')
black_rook   = pygame.image.load('./assets/black_rook.png')
black_queen  = pygame.image.load('./assets/black_queen.png')
black_king   = pygame.image.load('./assets/black_king.png')


chess.Color = True

def create_board():
    rfen = ""
    for i in sys.argv[1:]:
        rfen += i + " "
    rfen = rfen[:-1]
    if len (sys.argv) < 2 and rfen == "":
        return chess.Board()
    else:
        return chess.Board(rfen)

board = create_board()


possible_moves_ = []
selected_piece = ""
before_path = ""
promote_square = ""
promote_to = ""
bot_turn = True

pygame.init()

surface = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chess & Stockfish Using PyGame")
frame = pygame.time.Clock()


engine_ = chess.engine.SimpleEngine.popen_uci("stockfish-windows.exe")


square_size = (width / 8, height / 8)

dark_square_color  = (184, 135, 98)
light_square_color = (237, 214, 176)


def update_board():
    color = light_square_color
    next_color = lambda : dark_square_color if color == light_square_color else light_square_color
    for y in range(8):
        color = next_color()
        for x in range(8) :
            pygame.draw.rect(
                surface, color,
                pygame.Rect(x * width / 8, y * height / 8, square_size[0],
                square_size[1])
            )
            color = next_color()


def update_pieces():
    pieces = board.piece_map()
    for key in pieces.keys():
        piece = pieces[key]
        piece_x, piece_y = int(key), 0
        while piece_x > 7:
            piece_x -= 8
            piece_y += 1
        piece_type = str(piece.symbol())
        pieces_icons: dict[str, pygame.Surface] = {
            'P': white_pawn, 'p': black_pawn,
            'B': white_bishop, 'b': black_bishop,
            'N': white_knight, 'n': black_knight,
            'R': white_rook, 'r': black_rook,
            'Q': white_queen, 'q': black_queen,
            'K': white_king, 'k': black_king
        }
        piece_icon = pieces_icons[piece_type]
        piece_x = piece_x * width / 8 + \
            (square_size[0] - piece_icon.get_width()) / 2
        piece_y = piece_y * height / 8 + \
            (square_size[0] - piece_icon.get_height()) / 2
        surface.blit(
            piece_icon,
            (piece_x, piece_y)
        )


def possible_moves(uci: str="None"):
    all_possible_moves = [str(x) for x in list(board.legal_moves)]
    result = []
    for move in all_possible_moves:
        if move.startswith(uci):
            result.append(move)
    return result


def draw_transparent_circle(center: tuple, radius: float, color: tuple):
    st_circle = pygame.Surface((radius, radius), pygame.SRCALPHA)
    pygame.draw.circle(st_circle, color, (radius / 2, radius / 2), radius / 2)
    surface.blit(st_circle, (center[0] - (radius / 2), center[1] - (radius / 2)))


def draw_transparent_rect(rect: tuple, color: tuple):
    st_rect = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA)
    pygame.draw.rect(st_rect, color, (0, 0, rect[2], rect[3]))
    surface.blit(st_rect, (rect[0], rect[1]))


def uci_to_index(uci: str) -> tuple[int, int]:
    return (
        {"a": 0, "b": 1, "c": 2,
         "d": 3, "e": 4, "f": 5,
         "g": 6, "h": 7}[uci[0]],
        int(uci[1]) - 1
    )
    
    
def index_to_uci(index: tuple[int, int]) -> str:
    return f"{['a','b','c','d','e','f','g','h'][index[0]]}{index[1] + 1}"
       

pygame.mixer.Sound("./assets/game-start.mp3").play()
     

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            engine_.close()
            sys.exit(0)
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                engine_.close()
                sys.exit(0)
            elif event.key == pygame.K_t:
                pygame.mixer.Sound("./assets/game-start.mp3").play()
                board = create_board()
                before_path     = ""
                selected_piece  = ""
                possible_moves_ = []
                promote_to = ""
                bot_turn = True
            elif event.key == pygame.K_b:
                promote_to = "b"
            elif event.key == pygame.K_n:
                promote_to = "n"
            elif event.key == pygame.K_r:
                promote_to = "r"
            elif event.key == pygame.K_q:
                promote_to = "q"
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and bot_turn == False :
                client_mouse_x, client_mouse_y = pygame.mouse.get_pos()
                square_x, square_y = 0, 0

                while client_mouse_x > 600 / 8:
                    square_x += 1
                    client_mouse_x -= 600 / 8

                while client_mouse_y > 600 / 8:
                    square_y += 1
                    client_mouse_y -= 600 / 8

                if selected_piece + index_to_uci((square_x, square_y)) + promote_to in possible_moves_:
                    if board.is_capture(chess.Move.from_uci(selected_piece + index_to_uci((square_x, square_y)))):
                        pygame.mixer.Sound("./assets/capture.mp3").play()
                    elif board.is_castling(chess.Move.from_uci(selected_piece + index_to_uci((square_x, square_y)))):
                        pygame.mixer.Sound("./assets/castle.mp3").play()
                    else:
                        pygame.mixer.Sound("./assets/move-self.mp3").play()
                    board.push_uci(selected_piece + index_to_uci((square_x, square_y)) + promote_to)
                    before_path     = selected_piece
                    selected_piece  = index_to_uci((square_x, square_y))
                    possible_moves_ = possible_moves(index_to_uci((square_x, square_y)))
                    if board.is_checkmate():
                        pygame.mixer.Sound("./assets/game-end.mp3").play()
                    elif board.is_check():
                        pygame.mixer.Sound("./assets/move-check.mp3").play()
                    bot_turn = True
                else:
                    before_path = ""
                    selected_piece = index_to_uci((square_x, square_y)) 
                    possible_moves_ = possible_moves(index_to_uci(
                        (square_x, square_y))) if board.is_game_over() == False else []
                promote_to = ""
    
            
    update_board()
    
    if bot_turn:
        re = engine_.play(board, chess.engine.Limit(0.5))
        bot_turn = False
        if board.is_capture(re.move):
            pygame.mixer.Sound("./assets/capture.mp3").play()
        elif board.is_castling(re.move):
            pygame.mixer.Sound("./assets/castle.mp3").play()
        else:
            pygame.mixer.Sound("./assets/move-self.mp3").play()
        board.push(re.move)
        if board.is_checkmate():
            pygame.mixer.Sound("./assets/game-end.mp3").play()
        elif board.is_check():
            pygame.mixer.Sound("./assets/move-check.mp3").play()
    
    for move in possible_moves_:
        x, y = uci_to_index(move[2:])
        
        draw_transparent_rect(
            (x * (width / 8),
             y * (height / 8),
             (width / 8),
             (height / 8)),
            (180, 213, 56, 150)
        )
        
        draw_transparent_circle(
            (x * (width / 8) + (width / 16),
             y * (height / 8) + (height / 16)),
            (width + height / 2) / 8 - (width + height / 2) / 10,
            (0, 0, 0, 50)
        )

    if before_path != "":
        x, y = uci_to_index(before_path)
        draw_transparent_rect(
            (x * (width / 8),
             y * (height / 8),
             (width / 8),
             (height / 8)),
            (180, 213, 56, 100)
        )
    
    if selected_piece != "":
        x, y = uci_to_index(selected_piece)
        draw_transparent_rect(
            (x * (width / 8),
             y * (height / 8),
             (width / 8),
             (height / 8)),
            (180, 213, 56, 100)
        )

    if board.is_checkmate() or board.is_check():
        piece_x, piece_y = int(str(board.king(board.turn))), 0
        while piece_x > 7:
            piece_x -= 8
            piece_y += 1
        draw_transparent_rect(
            (piece_x * (width / 8),
             piece_y * (height / 8),
             (width / 8),
             (height / 8)),
            (227, 34, 30, 150)
        )
    
    elif board.is_game_over():
        piece_x1, piece_y1 = int(str(board.king(chess.WHITE))), 0
        piece_x2, piece_y2 = int(str(board.king(chess.BLACK))), 0
        while piece_x1 > 7:
            piece_x1 -= 8
            piece_y1 += 1
        draw_transparent_rect(
            (piece_x1 * (width / 8),
             piece_y1 * (height / 8),
             (width / 8),
             (height / 8)),
            (214, 183, 19, 150)
        )
        while piece_x2 > 7:
            piece_x2 -= 8
            piece_y2 += 1
        draw_transparent_rect(
            (piece_x2 * (width / 8),
             piece_y2 * (height / 8),
             (width / 8),
             (height / 8)),
            (214, 183, 19, 150)
        )
    
    update_pieces()

    pygame.display.flip()
    frame.tick(60)
