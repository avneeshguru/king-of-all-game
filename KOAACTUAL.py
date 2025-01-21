import pygame
import random
from random import randint

pygame.init()
# original code
SCREEN_HEIGHT = 800
SCREEN_WIDTH = 700

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("King Of All")

draw = False
golem_turn_flag = True
first_turn = True
starting_position_set = False

original_deck = ['Punch', 'Punch', 'Punch', 'Punch', 'Punch', 'Kick', 'Kick', 'Kick', 'Kick', 'Kick',
        'Lasershot', 'Lasershot', 'Lasershot', 'Lasershot', 'Lasershot',
        'Cannon', 'Cannon', 'Cannon', 'Cannon', 'Cannon', 'Bomb', 'Deflection']

deck = original_deck.copy()

attack_list = []
placed_attacks = []
pieces_list = []

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

font = pygame.font.SysFont('Futura', 30)

max_cards = 5

# Load images
golem_image = pygame.image.load('golem.png')
opgolem_image = pygame.image.load('opgolem.png')
board_image = pygame.image.load('board.jpg')

def draw_hand(font, text_col):
    x_var = 10
    y_var = 750
    card_spacing = 120
    cards_per_row = SCREEN_WIDTH // card_spacing

    for i, attack in enumerate(attack_list):
        if i > 0 and i % cards_per_row == 0:
            x_var = 10
            y_var -= 40
        img = font.render(attack, True, text_col)
        screen.blit(img, (x_var, y_var))
        x_var += card_spacing

def draw_board():
    screen.blit(board_image, (0, 0))

def draw_draw_button():
    pygame.draw.rect(screen, (0, 255, 0), (300, 700, 70, 50))
    draw_text = font.render('Draw', True, WHITE)
    screen.blit(draw_text, (315, 710))

def draw_prompt():
    prompt_text = font.render('Select your starting square', True, BLACK)
    screen.blit(prompt_text, (SCREEN_WIDTH // 2 - prompt_text.get_width() // 2, SCREEN_HEIGHT // 2 - prompt_text.get_height() // 2))

class GamePiece:
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.selected = False
        self.move_options = []
        self.name = name

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, 100, 100))
        if not self.selected:
            name_text = font.render(self.name, True, WHITE)
            screen.blit(name_text, (self.x + 50 - name_text.get_width() // 2,
                                  self.y + 50 - name_text.get_height() // 2))

    def draw_move_options(self):
        for option in self.move_options:
            pygame.draw.circle(screen, GREEN, (option[0] + 50, option[1] + 50), 15)

class Punch(GamePiece):
    def __init__(self, x, y):
        super().__init__(x, y, "Punch")

    def generate_move_options(self):
        self.move_options = []
       
        # Add corner positions
        corners = [(0, 0), (600, 0), (0, 600), (600, 600)]
        for corner in corners:
            self.move_options.append(corner)
           
        # Add golem-like movement (adjacent squares)
        for dx, dy in [(dx, dy) for dx in [-100, 0, 100] for dy in [-100, 0, 100]]:
            if (dx, dy) != (0, 0):  # Exclude current position
                new_x = self.x + dx
                new_y = self.y + dy
                if 0 <= new_x < 700 and 0 <= new_y < 700:
                    self.move_options.append((new_x, new_y))

class Golem:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.attacks_list = []
        self.selected = False
        self.move_options = []

    def golem_turn(self):
        global deck, original_deck, draw, first_turn, starting_position_set

        if golem_turn_flag and not first_turn and starting_position_set and draw:
            deck_empty = all(card == '' for card in deck)
            if deck_empty:
                deck = original_deck.copy()
           
            new_card = ''
            while new_card == '':
                new_index = randint(0, len(deck) - 1)
                new_card = deck[new_index]

            deck[new_index] = ''  
            self.attacks_list.append(new_card)
            attack_list.append(new_card)
            draw = False

    def draw(self):
        screen.blit(golem_image, (self.x, self.y))

    def draw_move_options(self):
        for option in self.move_options:
            pygame.draw.circle(screen, BLUE, option, 15)

    def generate_move_options(self):
        self.move_options = [
            (self.x + dx + 50, self.y + dy + 50)
            for dx, dy in [(dx, dy) for dx in [-100, 0, 100] for dy in [-100, 0, 100]]
            if (dx, dy) != (0, 0) and 0 <= self.x + dx < 700 and 0 <= self.y + dy < 700
        ]

class Cannon(GamePiece):
    def __init__(self, x, y):
        super().__init__(x, y, "Cannon")

    def generate_move_options(self):
        self.move_options = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dx, dy in directions:
            for step in range(1, 8):
                new_x = self.x + dx * step * 100
                new_y = self.y + dy * step * 100
                if 0 <= new_x < 700 and 0 <= new_y < 700:
                    self.move_options.append((new_x, new_y))
                else:
                    break

class Bomb(GamePiece):
    def __init__(self, x, y):
        super().__init__(x, y, "Bomb")

    def generate_move_options(self):
        self.move_options = [
            (self.x + dx, self.y + dy)
            for dx, dy in [(dx, dy) for dx in [-100, 0, 100] for dy in [-100, 0, 100]]
            if (dx, dy) != (0, 0) and 0 <= self.x + dx < 700 and 0 <= self.y + dy < 700
        ]

class Kick(GamePiece):
    def __init__(self, x, y):
        super().__init__(x, y, "Kick")

    def generate_move_options(self):
        self.move_options = []
        directions = [(1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dx, dy in directions:
            for step in range(1, 8):
                new_x = self.x + dx * step * 100
                new_y = self.y + dy * step * 100
                if 0 <= new_x < 700 and 0 <= new_y < 700:
                    self.move_options.append((new_x, new_y))
                else:
                    break

class Deflection(GamePiece):
    def __init__(self, x, y):
        super().__init__(x, y, "Deflection")

    def generate_move_options(self):
        self.move_options = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx, dy in directions:
            for step in range(1, 8):
                new_x = self.x + dx * step * 100
                new_y = self.y + dy * step * 100
                if 0 <= new_x < 700 and 0 <= new_y < 700:
                    self.move_options.append((new_x, new_y))
                else:
                    break

class Lasershot(GamePiece):
    def __init__(self, x, y):
        super().__init__(x, y, "Lasershot")

    def generate_move_options(self):
        self.move_options = []
       
        # Get positions adjacent to player's golem
        for dx, dy in [(dx, dy) for dx in [-100, 0, 100] for dy in [-100, 0, 100]]:
            if (dx, dy) != (0, 0):  # Exclude golem's position
                new_x = golem.x + dx
                new_y = golem.y + dy
                if 0 <= new_x < 700 and 0 <= new_y < 700:
                    self.move_options.append((new_x, new_y))
       
        # Get positions adjacent to opponent's golem
        for dx, dy in [(dx, dy) for dx in [-100, 0, 100] for dy in [-100, 0, 100]]:
            if (dx, dy) != (0, 0):  # Exclude opgolem's position
                new_x = opgolem.x + dx
                new_y = opgolem.y + dy
                if 0 <= new_x < 700 and 0 <= new_y < 700:
                    # Avoid duplicating positions if golems are near each other
                    if (new_x, new_y) not in self.move_options:
                        self.move_options.append((new_x, new_y))

class Opgolem:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.attacks_list = []

    def draw(self):
        screen.blit(opgolem_image, (self.x, self.y))

def get_random_position():
    return (randint(0, 6) * 100, randint(0, 6) * 100)

# Initialize game objects
golem = Golem(0, 0)
opgolem_x, opgolem_y = get_random_position()
while opgolem_x == golem.x and opgolem_y == golem.y:
    opgolem_x, opgolem_y = get_random_position()
opgolem = Opgolem(opgolem_x, opgolem_y)

dragging = False
dragged_card = None
dragged_card_index = None

# Game loop
run = True
while run:
    screen.fill(BLACK)
    draw_board()
    draw_hand(font, RED)

    if starting_position_set:
        draw_draw_button()
        golem.golem_turn()
        golem.draw()
        opgolem.draw()
        for piece in pieces_list:
            piece.draw()
            if piece.selected:
                piece.draw_move_options()
        if golem.selected:
            golem.draw_move_options()
    else:
        draw_prompt()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
           
            if first_turn and not starting_position_set:
                if mouse_pos[1] < 700:
                    golem.x = (mouse_pos[0] // 100) * 100
                    golem.y = (mouse_pos[1] // 100) * 100
                    starting_position_set = True
                    first_turn = False
            else:
                if starting_position_set:
                    # Handle golem selection
                    if golem.x <= mouse_pos[0] <= golem.x + 100 and golem.y <= mouse_pos[1] <= golem.y + 100:
                        golem.selected = not golem.selected
                        if golem.selected:
                            golem.generate_move_options()
                        else:
                            golem.move_options = []

                    # Handle piece selection
                    piece_clicked = False
                    for piece in pieces_list:
                        if piece.x <= mouse_pos[0] <= piece.x + 100 and piece.y <= mouse_pos[1] <= piece.y + 100:
                            piece_clicked = True
                            if not piece.selected:
                                for other_piece in pieces_list:
                                    other_piece.selected = False
                                piece.selected = True
                                piece.generate_move_options()
                            else:
                                piece.selected = False
                            break

                    # Handle piece movement
                    if not piece_clicked:
                        for piece in pieces_list:
                            if piece.selected:
                                for option in piece.move_options:
                                    option_x = option[0]
                                    option_y = option[1]
                                    if (abs(mouse_pos[0] - (option_x + 50)) < 15 and
                                        abs(mouse_pos[1] - (option_y + 50)) < 15):
                                        piece.x = option_x
                                        piece.y = option_y
                                        piece.selected = False
                                        break

                    # Handle draw button
                    if 300 < mouse_pos[0] < 370 and 700 < mouse_pos[1] < 750:
                        if len(attack_list) < max_cards:
                            draw = True

                    # Handle card dragging
                    for i, attack in enumerate(attack_list):
                        card_x = 10 + (i % (SCREEN_WIDTH // 120)) * 120
                        card_y = 750 - (i // (SCREEN_WIDTH // 120)) * 40
                        if card_x < mouse_pos[0] < card_x + 100 and card_y < mouse_pos[1] < card_y + 30:
                            dragging = True
                            dragged_card = attack
                            dragged_card_index = i
                            break

        if event.type == pygame.MOUSEBUTTONUP:
            if dragging:
                mouse_pos = pygame.mouse.get_pos()
                grid_x = mouse_pos[0] // 100 * 100
                grid_y = mouse_pos[1] // 100 * 100

                if 0 <= grid_x < 700 and 0 <= grid_y < 700:
                    new_piece = None
                    if dragged_card == "Cannon":
                        new_piece = Cannon(grid_x, grid_y)
                    elif dragged_card == "Bomb":
                        new_piece = Bomb(grid_x, grid_y)
                    elif dragged_card == "Kick":
                        new_piece = Kick(grid_x, grid_y)
                    elif dragged_card == "Deflection":
                        new_piece = Deflection(grid_x, grid_y)
                    elif dragged_card == "Punch":
                        new_piece = Punch(grid_x, grid_y)
                    elif dragged_card == "Lasershot":
                        new_piece = Lasershot(grid_x, grid_y)
                   
                    if new_piece:
                        pieces_list.append(new_piece)
                        attack_list.pop(dragged_card_index)

                dragging = False
                dragged_card = None
                dragged_card_index = None

    pygame.display.update()

pygame.quit()