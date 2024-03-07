#
# Thanks for visiting this project
#
#   Author:
#       shijian-wow@github, https://github.com/shijian-wow
#
#   Details:
#       This project made with Love by shijian-wow@github, if you want to see more
#       projects which those made by me, check out https://github.com/shijian-wow
#
#   License:
#       This project is licensed under MIT license, and here is the license content:
#   
#           MIT License
#       
#           Copyright (c) 2024 shijian-wow
#           
#           Permission is hereby granted, free of charge, to any person obtaining a copy
#           of this software and associated documentation files (the "Software"), to deal
#           in the Software without restriction, including without limitation the rights
#           to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#           copies of the Software, and to permit persons to whom the Software is
#           furnished to do so, subject to the following conditions:
#           
#           The above copyright notice and this permission notice shall be included in all
#           copies or substantial portions of the Software.
#           
#           THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#           IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#           FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#           AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#           LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#           OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#           SOFTWARE.
#

#
# This file is the primary file responsible for starting
# the graphical interface of the Chess GUI project.
# Contributors and shijian-wow wrote its content.
#
# To run this script with typical settings via the command line,
# consider one of the following options:
#
#   (If you prefer using Makefile)
#   $ make run
#
#   (On Windows systems)
#   $ py chess-gui.py [OPTION]
#
#   (On Linux systems)
#   $ python3 chess-gui.py [OPTION]
#
# Replace [OPTION] with optional arguments relevant to your usage.
#
import sys
import click
import chess
import pygame
from time import sleep
import chess.engine as engine

def exit_game(__status = 0):
    stockfish.close()
    sys.exit(__status)

def reversed_string(iterable):
    riterable = ""
    for idx in range(len(iterable)):
        riterable += iterable[(-idx) - 1]
    return riterable

def render_board(surface, width, height, color):
    light_square_color: tuple = (237, 214, 176)
    dark_square_color: tuple = (184, 135, 98)
    
    next_square_color = lambda square_color: light_square_color if \
        square_color == dark_square_color else dark_square_color

    square_color = light_square_color
    
    for x in range(8):
        for y in range(8):
            pygame.draw.rect(surface, (square_color), (x * width / 8,
                y * height / 8, width * 8, height * 8))
            square_color = next_square_color(square_color)
        square_color = next_square_color(square_color)
    
    x = 1
    files = 'abcdefgh'
    
    if color == chess.BLACK:
        files = str(reversed_string(files))
    
    for file in files:
        text_surface = font.render(file, True, square_color)
        text_surface_rect = text_surface.get_rect()
        text_surface_rect.center = (x * width / 8 - 65, 8 * height / 8 - 13)
        surface.blit(text_surface, text_surface_rect)
        square_color = next_square_color(square_color)
        x += 1
    
    y = 1
    ranks = '12345678'
    
    if color == chess.WHITE:
        ranks = str(reversed_string(ranks))
    
    for rank in ranks:
        digit_surface = font.render(rank, True, square_color)
        digit_surface_rect = digit_surface.get_rect()
        digit_surface_rect.center = (8 * width / 8 - 10, y * height / 8 - 65)
        surface.blit(digit_surface, digit_surface_rect)
        square_color = next_square_color(square_color)
        y += 1
        
def index2uci(file: int, rank: int, color):
    if file not in range(1, 9) or rank not in range(1, 9):
        raise ValueError("`file` and `rank` parameter must be in range of 1 and 8")
    if color == chess.WHITE:
        rank = 8 - rank
    else: file = 9 - file
    return 'abcdefgh'[file - 1] + (str(rank + 1) if color == chess.WHITE else str(rank))

def uci2index(uci: str, color):
    file = 'abcdefgh'.index(uci[0])
    rank = int(uci[1])
    if color == chess.WHITE:
        rank = 8 - rank
    else:
        file = 7 - file
        rank -= 1
    return (file, rank)

def render_pieces(surface, width, height, assets, color):
    dragging[2] = None
    
    pieces_map = board.piece_map()
    pieces_arr = []
    
    for y in range(8):
        pieces_arr.append([])
        for x in range(8):
            pieces_arr[y].append(None)
    
    for key in pieces_map.keys():
        piece = pieces_map[key]
        piece_surface = assets[piece.symbol()]
        
        x, y = int(key % 8) + 1, int(key / 8) + 1
        
        if color == chess.WHITE and not (index2uci(x, 9 - y, color) == pressed_square and dragging[0]):
            pieces_arr[y - 1][x - 1] = piece_surface
        elif color == chess.BLACK and not (index2uci(9 - x, y, color) == pressed_square and dragging[0]):
            pieces_arr[y - 1][x - 1] = piece_surface
        else:
            dragging[1] = index2uci(x, y, color)
            dragging[2] = piece_surface
    
    for y in range(len(pieces_arr)):
        for x in range(len(pieces_arr[y])):
            if pieces_arr[y][x] and index2uci(x + 1, y + 1, color) != dragging[1]:
                if color == chess.WHITE:
                    surface.blit(source=pieces_arr[y][x],
                    dest=(x * width / 8 + 10, (7 - y) * height / 8 + 10))
                else:
                    surface.blit(source=pieces_arr[y][x],
                    dest=((7 - x) * width / 8 + 10, y * height / 8 + 10))
    
def render_dragging_piece(surface, piece_image: pygame.Surface | None):
    if piece_image:
        client_x, client_y = pygame.mouse.get_pos()
        surface.blit(piece_image, (client_x - 25, client_y - 25))

def render_promotion_menu(surface, visible, assets):
    if visible:
        rect_surface = pygame.Surface((width,
            height), pygame.SRCALPHA)
        
        pygame.draw.rect(rect_surface, (130, 126, 126, 250),
            (0, 0, width, height))
        
        surface.blit(rect_surface, (0, 0))
        
        surface.blit(assets['q' if board.turn == \
             chess.BLACK else 'Q'], (0   + 150, 270))
        
        surface.blit(assets['r' if board.turn == \
             chess.BLACK else 'R'], (80  + 150, 270))
        
        surface.blit(assets['b' if board.turn == \
             chess.BLACK else 'B'], (160 + 150, 270))
        
        surface.blit(assets['n' if board.turn == \
             chess.BLACK else 'N'], (240 + 150, 270))

def start_game(fen, game_type, color):
    running: bool = True
    
    def init_board():
        return chess.Board(fen)
    
    def previous_board_state():
        return previous_board_states[-1]
    
    global pressed_square
    pressed_square = ""
    
    global highlighted_squares
    highlighted_squares = []
    
    global board
    board = init_board()
    
    is_promotion_menu_visible = False
    promoting_move = ""
    promote_to = ""
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit_game()
                
                elif event.key == pygame.K_u and not is_promotion_menu_visible:
                    if len(previous_board_states) > 0:
                        board = previous_board_state()
                        previous_board_states.pop()
                    pressed_square = ""
                    dragging[0] = False
                    dragging[1] = ""
                    dragging[2] = None
                    promote_to = ""
                    promoting_move = ""
                    is_promotion_menu_visible = False
                    highlighted_squares = []
                
                elif event.key == pygame.K_r and not is_promotion_menu_visible:
                    board = init_board()
                    previous_board_states.clear()
                    pressed_square = ""
                    dragging[0] = False
                    dragging[1] = ""
                    dragging[2] = None
                    promote_to = ""
                    promoting_move = ""
                    is_promotion_menu_visible = False
                    highlighted_squares = []
        
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not is_bot_turn:
                    client_x, client_y = pygame.mouse.get_pos()
                    client_x, client_y = (int((client_x + 1) / (width / 8)),
                        int((client_y + 1) / (height / 8)))

                    if client_x < 8:
                        client_x += 1

                    if client_y < 8:
                        client_y += 1
                    
                    if (pressed_square == "" or pressed_square + \
                        index2uci(client_x, client_y, color) not in legal_moves) \
                            and not is_promotion_menu_visible:
                            
                        pressed_square = index2uci(client_x, client_y, color)
                        highlighted_squares = [pressed_square]
                        
                    elif is_promotion_menu_visible:
                        client_x, client_y = pygame.mouse.get_pos()
                        
                        if client_x in range(150, 207) and client_y \
                            in range(270, 327):
                                promote_to = 'q'
                        
                        elif client_x in range(230, 287) and client_y \
                            in range(270, 327):
                                promote_to = 'r'
                        
                        elif client_x in range(310, 367) and client_y \
                            in range(270, 327):
                                promote_to = 'b'
                        
                        elif client_x in range(390, 447) and client_y \
                            in range(270, 327):
                                promote_to = 'n'
                        
                        else:
                            continue
                        
                        if board.is_capture(chess.Move.from_uci(promoting_move + promote_to)):
                            pygame.mixer.Sound("./assets/capture.mp3").play()
                            
                        elif board.is_castling(chess.Move.from_uci(promoting_move + promote_to)):
                            pygame.mixer.Sound("./assets/castle.mp3").play()
                            
                        if board.turn == color:
                            pygame.mixer.Sound("./assets/move-self.mp3").play()
                        else:
                            pygame.mixer.Sound("./assets/move-opponent.mp3").play()
                        
                        previous_board_states.append(board.copy())
                        
                        board.push_uci(promoting_move + promote_to)
                        
                        highlighted_squares = [pressed_square, promoting_move[2:]]
                        
                        if board.is_checkmate():
                            pygame.mixer.Sound("./assets/game-end.mp3").play()
                        elif board.is_check():
                            pygame.mixer.Sound("./assets/move-check.mp3").play()
                        
                        promote_to = ""
                        promoting_move = ""
                        is_promotion_menu_visible = False
                    
                    elif pressed_square + index2uci(client_x, client_y, color) in \
                        [move[:-1] for move in legal_moves] and not is_promotion_menu_visible:
                        
                        is_promotion_menu_visible = True
                        promoting_move = pressed_square + index2uci(client_x, client_y, color)
                        
                    elif not is_promotion_menu_visible:
                        if board.is_capture(chess.Move.from_uci(pressed_square + \
                            index2uci(client_x, client_y, color))):
                            pygame.mixer.Sound("./assets/capture.mp3").play()
                            
                        elif board.is_castling(chess.Move.from_uci(pressed_square + \
                            index2uci(client_x, client_y, color))):
                            pygame.mixer.Sound("./assets/castle.mp3").play()
                            
                        if board.turn == color:
                            pygame.mixer.Sound("./assets/move-self.mp3").play()
                        else:
                            pygame.mixer.Sound("./assets/move-opponent.mp3").play()
                        
                        previous_board_states.append(board.copy())
                        
                        board.push_uci(pressed_square + \
                            index2uci(client_x, client_y, color))
                        
                        highlighted_squares = [pressed_square, index2uci(client_x, client_y, color)]
                        
                        if board.is_checkmate():
                            pygame.mixer.Sound("./assets/game-end.mp3").play()
                        elif board.is_check():
                            pygame.mixer.Sound("./assets/move-check.mp3").play()
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    client_x, client_y = pygame.mouse.get_pos()
                    client_x, client_y = (int((client_x + 1) / (width / 8)),
                                          int((client_y + 1) / (height / 8)))

                    if client_x < 8:
                        client_x += 1

                    if client_y < 8:
                        client_y += 1
                    
                    try:
                        if color == chess.WHITE and dragging[0] and dragging[1][0] + str(9 - int(dragging[1][1])) + \
                            index2uci(client_x, client_y, color) in legal_moves \
                                and not is_promotion_menu_visible:
                            
                            if board.is_capture(chess.Move.from_uci(
                                dragging[1][0] + str(9 - int(dragging[1][1])) + \
                                index2uci(client_x, client_y, color))):
                                pygame.mixer.Sound("./assets/capture.mp3").play()
    
                            elif board.is_castling(chess.Move.from_uci(
                                dragging[1][0] + str(9 - int(dragging[1][1])) + \
                                index2uci(client_x, client_y, color))):
                                pygame.mixer.Sound("./assets/castle.mp3").play()
    
                            else:
                                if board.turn == color:
                                    pygame.mixer.Sound("./assets/move-self.mp3").play()
                                else:
                                    pygame.mixer.Sound("./assets/move-opponent.mp3").play()
                            
                            previous_board_states.append(board.copy())
                            
                            board.push_uci(dragging[1][0] + str(9 - int(dragging[1][1])) + \
                                index2uci(client_x, client_y, color))
                            
                            highlighted_squares = [dragging[1][0] + str(9 - int(dragging[1][1])),
                                index2uci(client_x, client_y, color)]
                            
                            if board.is_checkmate():
                                pygame.mixer.Sound("./assets/game-end.mp3").play()
                            elif board.is_check():
                                pygame.mixer.Sound("./assets/move-check.mp3").play()
                        
                        elif color == chess.WHITE and dragging[0] and dragging[1][0] + str(9 - int(dragging[1][1])) + \
                                index2uci(client_x, client_y, color) in [move[:-1] for move in legal_moves]:
                            
                            is_promotion_menu_visible = True
                            promoting_move = dragging[1][0] + str(9 - int(dragging[1][1])) + \
                                index2uci(client_x, client_y, color)
                            
                        elif color == chess.BLACK and dragging[0] and 'abcdefgh'[7 - 'abcdefgh'.index(dragging[1][0])] + \
                                dragging[1][1] + index2uci(client_x, client_y, color) in legal_moves \
                                and not is_promotion_menu_visible:
                            
                            if board.is_capture(chess.Move.from_uci(
                                'abcdefgh'[7 - 'abcdefgh'.index(dragging[1][0])] \
                                + dragging[1][1] + index2uci(client_x, client_y, color))):
                                pygame.mixer.Sound("./assets/capture.mp3").play()
    
                            elif board.is_castling(chess.Move.from_uci(
                                'abcdefgh'[7 - 'abcdefgh'.index(dragging[1][0])] \
                                + dragging[1][1] + index2uci(client_x, client_y, color))):
                                pygame.mixer.Sound("./assets/castle.mp3").play()
    
                            else:
                                if board.turn == color:
                                    pygame.mixer.Sound("./assets/move-self.mp3").play()
                                else:
                                    pygame.mixer.Sound("./assets/move-opponent.mp3").play()
                            
                            previous_board_states.append(board.copy())
                            
                            board.push_uci('abcdefgh'[7 - 'abcdefgh'.index(dragging[1][0])] \
                                + dragging[1][1] + index2uci(client_x, client_y, color))
                            
                            highlighted_squares = ['abcdefgh'[7 - 'abcdefgh'.index(dragging[1][0])] + dragging[1][1],
                                index2uci(client_x, client_y, color)]
                            
                            if board.is_checkmate():
                                pygame.mixer.Sound("./assets/game-end.mp3").play()
                            elif board.is_check():
                                pygame.mixer.Sound("./assets/move-check.mp3").play()
                        
                        elif color == chess.BLACK and dragging[0] and 'abcdefgh'[7 - 'abcdefgh'.index(dragging[1][0])] + \
                                dragging[1][1] + index2uci(client_x, client_y, color) in [move[:-1] for move in legal_moves]:
                            
                            is_promotion_menu_visible = True
                            promoting_move = 'abcdefgh'[7 - 'abcdefgh'.index(dragging[1][0])] + \
                                dragging[1][1] + index2uci(client_x, client_y, color)
                    except:
                        pass
                    
                    dragging[0] = False
                    dragging[1] = ""
                    dragging[2] = None
            
            elif event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0] and not is_bot_turn \
                    and not is_promotion_menu_visible:
                    dragging[0] = True
                    
        is_bot_turn = False
        
        if game_type == 'singleplayer' and board.turn != color and not \
            board.is_game_over():
            is_bot_turn = True
        elif game_type == 'bot_versus_itself' and board.is_game_over():
            sleep(0.3)
            is_bot_turn = True
        
        legal_moves = []
        
        for move_uci in [str(move) for move in board.legal_moves]:
            if pressed_square:
                legal_moves.append(move_uci) if \
                    move_uci.startswith(pressed_square) else None
                    
            elif dragging[1]:
                legal_moves.append(move_uci) if \
                    move_uci.startswith(dragging[1]) else None
        
        if is_bot_turn:
            stockfish_play_result = stockfish.play(board, engine.Limit(0.001, 90))
            
            if stockfish_play_result.move:
                if board.is_capture(stockfish_play_result.move):
                    pygame.mixer.Sound("./assets/capture.mp3").play()
                elif board.is_castling(stockfish_play_result.move):
                    pygame.mixer.Sound("./assets/castle.mp3").play()
                else:
                    pygame.mixer.Sound("./assets/move-opponent.mp3").play()
                
                board.push(stockfish_play_result.move)
                
                if board.is_checkmate():
                    pygame.mixer.Sound("./assets/game-end.mp3").play()
                elif board.is_check():
                    pygame.mixer.Sound("./assets/move-check.mp3").play()
        
        render_board(window, width, height, color)
        
        if board.is_checkmate() or board.is_check():
            king_index = int(str(board.king(board.turn)))
            x, y = int(king_index % 8), int(king_index / 8)

            if color == chess.WHITE:
                y = 7 - y
            else: x = 7 - x
            
            window.blit(assets['check'],
                (x * (width / 8),
                 y * (height / 8)))
        
        for move_uci in legal_moves:
            x, y = uci2index(move_uci[2:], color)

            window.blit(assets['dot'],
                        (x * width / 8, y * height / 8))
        
        for square in highlighted_squares:
            square_x, square_y = uci2index(square, color)
            square_width, square_height = width / 8, height / 8
            
            rect_surface = pygame.Surface((square_width,
            square_height), pygame.SRCALPHA)
            
            pygame.draw.rect(rect_surface, (170, 162, 58, 150), (0, 0,
            square_width, square_height))
            
            window.blit(rect_surface, (square_x * width / 8,
                square_y * height / 8))
        
        render_pieces(window, width, height, assets, color)
        render_dragging_piece(window, dragging[2])
        
        render_promotion_menu(window,
            is_promotion_menu_visible, assets)
        
        pygame.display.flip()
        clock.tick(60)

@click.command()
@click.option('--fen', '--starting-fen', '--board-starting-fen', help='this option defines the starting fen of board.', default=chess.STARTING_FEN)
@click.option('--game-type', help='this option defines the type of game, valid values: ("singleplayer" or "multiplayer").', default='singleplayer')
@click.option('--color', help='this option defines your color, and this only works in "singleplayer" mode', default='white')
def initialize_game(fen, game_type, color):
    pygame.init()
    
    global width, height
    width, height = (600, 600)
    
    global window
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Chess against Stockfish - Made with PyGame")
    
    global stockfish
    stockfish = engine.SimpleEngine.popen_uci("./stockfish-windows.exe")
    
    global assets
    assets = {
        'k'  : pygame.image.load('./assets/black_king.png')  , 'K'    : pygame.image.load('./assets/white_king.png'),
        'q'  : pygame.image.load('./assets/black_queen.png') , 'Q'    : pygame.image.load('./assets/white_queen.png'),
        'r'  : pygame.image.load('./assets/black_rook.png')  , 'R'    : pygame.image.load('./assets/white_rook.png'),
        'n'  : pygame.image.load('./assets/black_knight.png'), 'N'    : pygame.image.load('./assets/white_knight.png'),
        'b'  : pygame.image.load('./assets/black_bishop.png'), 'B'    : pygame.image.load('./assets/white_bishop.png'),
        'p'  : pygame.image.load('./assets/black_pawn.png')  , 'P'    : pygame.image.load('./assets/white_pawn.png'),
        'dot': pygame.image.load('./assets/dot.png')         , 'check': pygame.image.load('./assets/check.png')
    }
    
    global font
    font = pygame.font.Font("./assets/Geologica_Auto-Regular.ttf",15)
    
    global previous_board_states
    previous_board_states = []
    
    global clock
    clock = pygame.time.Clock()
    
    global dragging
    dragging = [False, "", None]
    
    start_game(fen, game_type, chess.WHITE if color=="white" or game_type == 'multiplayer' else chess.BLACK)

if __name__ == "__main__":
    initialize_game()
