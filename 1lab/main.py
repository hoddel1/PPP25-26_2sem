import pygame
import sys
import copy

WIDTH, HEIGHT = 600, 600
CHESS_SIZE = 8
SQ_SIZE = WIDTH // CHESS_SIZE

WHITE_COLOR = (240, 217, 181)
BLACK_COLOR = (181, 136, 99)
HIGHLIGHT = (130, 151, 105) 
DANGER = (231, 76, 60)     #Шах-красный
UNDER_ATTACK = (243, 156, 18) #Под боем-оранжевый
SELECT = (186, 202, 43)

RU_NAMES = {
    'Pawn': 'Пешка', 'Rook': 'Ладья', 'Knight': 'Конь', 
    'Bishop': 'Слон', 'Queen': 'Ферзь', 'King': 'Кор.'
}

class Piece:
    def __init__(self, color, name):
        self.color = color
        self.name = name

    def get_valid_moves(self, pos, board):
        return []

    def __repr__(self):
        return f'{RU_NAMES.get(self.name, self.name)}'

class Pawn(Piece):
    def get_valid_moves(self, pos, board):
        moves = []
        r, c = pos
        direction = -1 if self.color == 'white' else 1
        if 0 <= r + direction < 8 and board.grid[r+direction][c] is None:
            moves.append((r + direction, c))
            start_row = 6 if self.color == 'white' else 1
            if r == start_row and board.grid[r + 2*direction][c] is None:
                moves.append((r + 2*direction, c))
        for dc in [-1, 1]:
            nr, nc = r + direction, c + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                target = board.grid[nr][nc]
                if target and target.color != self.color:
                    moves.append((nr, nc))
        return moves

class Knight(Piece):
    def get_valid_moves(self, pos, board):
        moves = []
        for dr, dc in [(-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1)]:
            nr, nc = pos[0] + dr, pos[1] + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                if board.grid[nr][nc] is None or board.grid[nr][nc].color != self.color:
                    moves.append((nr, nc))
        return moves

class Bishop(Piece):
    def get_valid_moves(self, pos, board):
        moves = []
        for dr, dc in [(-1,-1), (-1,1), (1,-1), (1,1)]:
            for i in range(1, 8):
                nr, nc = pos[0] + dr*i, pos[1] + dc*i
                if 0 <= nr < 8 and 0 <= nc < 8:
                    if board.grid[nr][nc] is None: moves.append((nr, nc))
                    elif board.grid[nr][nc].color != self.color:
                        moves.append((nr, nc)); break
                    else: break
                else: break
        return moves

class Rook(Piece):
    def get_valid_moves(self, pos, board):
        moves = []
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            for i in range(1, 8):
                nr, nc = pos[0] + dr*i, pos[1] + dc*i
                if 0 <= nr < 8 and 0 <= nc < 8:
                    if board.grid[nr][nc] is None: moves.append((nr, nc))
                    elif board.grid[nr][nc].color != self.color:
                        moves.append((nr, nc)); break
                    else: break
                else: break
        return moves

class Queen(Piece):
    def get_valid_moves(self, pos, board):
        return Rook.get_valid_moves(self, pos, board) + Bishop.get_valid_moves(self, pos, board)

class King(Piece):
    def get_valid_moves(self, pos, board):
        moves = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0: continue
                nr, nc = pos[0] + dr, pos[1] + dc
                if 0 <= nr < 8 and 0 <= nc < 8:
                    if board.grid[nr][nc] is None or board.grid[nr][nc].color != self.color:
                        moves.append((nr, nc))
        return moves

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.turn = 'white'
        self.history = []
        self.setup()

    def setup(self):
        order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for i, cls in enumerate(order):
            self.grid[0][i] = cls('black', cls.__name__)
            self.grid[7][i] = cls('white', cls.__name__)
        for i in range(8):
            self.grid[1][i] = Pawn('black', 'Pawn')
            self.grid[6][i] = Pawn('white', 'Pawn')

    def get_king_pos(self, color):
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if p and p.name == 'King' and p.color == color: return (r, c)
        return None

    def is_check(self, color):
        kp = self.get_king_pos(color)
        if not kp: return False
        return self.is_square_under_attack(kp, color)

    def is_square_under_attack(self, pos, color):
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if p and p.color != color:
                    if pos in p.get_valid_moves((r, c), self):
                        return True
        return False

    def get_legal_moves(self, pos):
        p = self.grid[pos[0]][pos[1]]
        if not p or p.color != self.turn: return []
        valid = p.get_valid_moves(pos, self)
        legal = []
        for m in valid:
            temp_board = copy.deepcopy(self)
            temp_board.execute_move(pos, m, sim=True)
            if not temp_board.is_check(self.turn):
                legal.append(m)
        return legal

    def execute_move(self, start, end, sim=False):
        if not sim: self.history.append(copy.deepcopy(self.grid))
        p = self.grid[start[0]][start[1]]
        self.grid[end[0]][end[1]] = p
        self.grid[start[0]][start[1]] = None
        if not sim: self.turn = 'black' if self.turn == 'white' else 'white'

    def undo(self):
        if self.history:
            self.grid = self.history.pop()
            self.turn = 'black' if self.turn == 'white' else 'white'

class ChessGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Шахматы')
        self.board = Board()
        self.selected = None
        self.valid_moves = []
        self.game_over = False
        self.result_text = ''
        self.font = pygame.font.SysFont('Arial', 22, True)
        self.big_font = pygame.font.SysFont('Arial', 40, True)

    def check_end_game(self):
        all_moves = []
        for r in range(8):
            for c in range(8):
                p = self.board.grid[r][c]
                if p and p.color == self.board.turn:
                    all_moves.extend(self.board.get_legal_moves((r, c)))
        if not all_moves:
            self.game_over = True
            if self.board.is_check(self.board.turn):
                winner = 'ЧЕРНЫЕ' if self.board.turn == 'white' else 'БЕЛЫЕ'
                self.result_text = f'МАТ! ПОБЕДА: {winner}'
            else:
                self.result_text = 'НИЧЬЯ'

    def draw(self):
        for r in range(8):
            for c in range(8):
                color = WHITE_COLOR if (r + c) % 2 == 0 else BLACK_COLOR
                if (r, c) == self.selected: color = SELECT
                pygame.draw.rect(self.screen, color, (c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                
                p = self.board.grid[r][c]
                if p:
                    if p.name == 'King' and self.board.is_check(p.color):
                        pygame.draw.rect(self.screen, DANGER, (c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                    elif self.board.is_square_under_attack((r, c), p.color):
                        if p.color == self.board.turn:
                            pygame.draw.rect(self.screen, UNDER_ATTACK, (c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                    
                    text_color = (255, 255, 255) if p.color == 'white' else (20, 20, 20)
                    outline_color = (0, 0, 0) if p.color == 'white' else (200, 200, 200)
                    shadow = self.font.render(str(p), True, outline_color)
                    self.screen.blit(shadow, (c*SQ_SIZE + 6, r*SQ_SIZE + 26))
                    txt = self.font.render(str(p), True, text_color)
                    self.screen.blit(txt, (c*SQ_SIZE + 5, r*SQ_SIZE + 25))

        for m in self.valid_moves:
            pygame.draw.circle(self.screen, HIGHLIGHT, (m[1]*SQ_SIZE + SQ_SIZE//2, m[0]*SQ_SIZE + SQ_SIZE//2), 8)
        
        if self.game_over:
            overlay = pygame.Surface((WIDTH, 80))
            overlay.set_alpha(200); overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, HEIGHT//2 - 40))
            res_txt = self.big_font.render(self.result_text, True, (255, 255, 255))
            self.screen.blit(res_txt, (WIDTH//2 - res_txt.get_width()//2, HEIGHT//2 - 20))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if not self.game_over:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                        self.board.undo()
                        self.selected, self.valid_moves = None, []
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        c, r = event.pos[0] // SQ_SIZE, event.pos[1] // SQ_SIZE
                        if (r, c) in self.valid_moves:
                            self.board.execute_move(self.selected, (r, c))
                            self.selected, self.valid_moves = None, []
                            self.check_end_game()
                        else:
                            p = self.board.grid[r][c]
                            if p and p.color == self.board.turn:
                                self.selected = (r, c)
                                self.valid_moves = self.board.get_legal_moves((r, c))
            self.draw()
            pygame.display.flip()

if __name__ == '__main__':
    ChessGame().run()
