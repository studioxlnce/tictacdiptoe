# Example file showing a basic pygame "game loop"
from turtle import position
from time import sleep
import pygame

# pygame setup
pygame.init()
[WINDOW_WIDTH, WINDOW_HEIGHT] = [1080, 1080]
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
[PIXEL_WIDTH, PIXEL_HEIGHT] = [WINDOW_WIDTH//3, WINDOW_HEIGHT//3]
clock = pygame.time.Clock()
running = True

# load images
def load_sprite(path, resolution):
    sprite = pygame.image.load(path)
    return pygame.transform.scale(sprite, resolution)

board = [[None for _ in range(3)] for _ in range(3)]
print(f"{board} \n")

# load icons
GRID = load_sprite('assets/icons/grid.png', [WINDOW_WIDTH, WINDOW_HEIGHT])
ICON_X = load_sprite('assets/icons/x.png', [(PIXEL_WIDTH//3 - 20), (PIXEL_HEIGHT//3 - 20)])
ICON_O = load_sprite('assets/icons/o.png', [(PIXEL_WIDTH//3 - 20), (PIXEL_HEIGHT//3 - 20)])
player = 0
winner = None

def check_win():
    # check rows
    for row in board:
        if row in [[0, 0, 0], [1, 1, 1]]:
            if player == 0:
                print("X WINS")
                return 0
            else:
                print("O WINS")
                return 1
    # check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            if player == 0:
                print("X WINS")
                return 0
            else:
                print("O WINS")
                return 1
    # check diagonals
    """
    this will likely have to be rewritten if we add more columns or widths
    """
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        if player == 0:
            print("X WINS")
            return 0
        else:
            print("O WINS")
            return 1
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        if player == 0:
            print("X WINS")
            return 0
        else:
            print("O WINS")
            return 1

def take_turn(turn_taker):
    # i shoose the global player variable, (coz we're gonna need this later)
    global player
    # fond square mouuse is currently in
    pos_rn = pygame.math.Vector2(pygame.mouse.get_pos())//PIXEL_WIDTH
    # if mouse is clicked and square is empty
    if (pygame.mouse.get_pressed()[0]):
        pos_rn_y, pos_rn_x = map(int, pos_rn)
        if (board[pos_rn_x][pos_rn_y] is None):
            board[pos_rn_x][pos_rn_y] = 0 if turn_taker == 0 else 1
            print(f"{board} \n")
            if (check_win() is not None):
                global winner
                winner = player
            else:
                player = 1 - player

def draw_board():
    for x, row in enumerate(board):
        for y, col in enumerate(board[x]):
            if board[x][y] == 0:
                # render cross
                screen.blit(ICON_X, ((y + .5)*PIXEL_HEIGHT, (x + .5)*PIXEL_WIDTH))
            if board[x][y] == 1:
                # render knought
                screen.blit(ICON_O, ((y + .5)*PIXEL_HEIGHT, (x + .5)*PIXEL_WIDTH))

def diplay_win(winner):
    text = ""
    text = f"🎉🎉 PLAYER {winner} WINS! 🎉🎉"
    print(f"PLAYER {winner} WINS")
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(text, True, (0, 0, 0), (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
    screen.blit(text, textRect)

while running:
    if (winner is not None):
        running = False
        sleep(5)

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    # RENDER YOUR GAME HERE
    screen.blit(GRID, (0, 0))
    take_turn(player)
    if (winner is not None):
        diplay_win(winner)
    pygame.event.wait()
    draw_board()

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limit FPS to 60
    clock.tick(60)

pygame.quit()