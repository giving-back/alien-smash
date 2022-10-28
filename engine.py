import pygame

from enum import Enum
from random import randrange

class GameState(Enum):
    TOSTART = 1
    INPROGRESS = 2
    OVER = 3

WIDTH = 800
HEIGHT = 800

start_game = Actor("ready", center=(WIDTH/2, HEIGHT/2))
game_over = Actor("gameover", center=(WIDTH/2, HEIGHT/2))
crosshair = Actor("crosshair")
pink_alien = Actor("pinkalien")
game_background = Actor("gamebackground")

#Globals
game_state = GameState.TOSTART
score = 0
move_time = 1.0
game_time = 10.0

def end_game():
    global game_state
    sounds.gameover.play()
    game_state = GameState.OVER

def draw_home():
    screen.blit("gamebackground", (0, 0))
    start_game.draw()
    crosshair.draw()
    screen.draw.text("ALIEN  SMASH", color=(0,0,0), center=(WIDTH/2, (HEIGHT - HEIGHT/4)-20))
    screen.draw.text("Created By Christian & Blake", color=(0,0,0), center=(WIDTH/2, HEIGHT - HEIGHT/4))

def draw_game():
    screen.blit("gamebackground", (0, 0))
    pink_alien.draw()
    crosshair.draw()

def draw_game_over():
    global score
    screen.blit("gamebackground", (0, 0))
    game_over.draw()
    crosshair.draw()
    screen.draw.text(f"Score: {score}", color=(0,0,0), center=(WIDTH/2, (HEIGHT - HEIGHT/4)-20))

def set_alien_hurt():
    pink_alien.image = "pinkburst"
    sounds.laser.play()
    clock.schedule_unique(set_alien_normal, 0.3)

def set_alien_normal():
    pink_alien.image = "pinkalien"

def random_move():
    pink_alien.x = randrange(pink_alien.width//2, WIDTH - (pink_alien.width//2))
    pink_alien.y = randrange(pink_alien.height//2, HEIGHT - (pink_alien.height//2))

clock.schedule_interval(random_move, move_time)

def draw():
    screen.clear()
    if game_state == GameState.TOSTART:
        draw_home()
    elif game_state == GameState.INPROGRESS:
        draw_game()
    elif game_state == GameState.OVER:
        draw_game_over()

def on_mouse_move(pos):
    crosshair.pos = pos

def update():
    global game_state

    if keyboard.f:
        pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    if keyboard.escape:
        game_state = GameState.TOSTART
    if keyboard.q:
        quit()

    if crosshair.colliderect(start_game):
        start_game.image = 'go'
    else:
        start_game.image = 'ready'

    if crosshair.colliderect(game_over):
        game_over.image = 'go'
    else:
        game_over.image = 'gameover'

def on_mouse_down(pos):
    global game_state
    global score

    if start_game.collidepoint(pos):
        score = 0
        sounds.go.play()
        game_state = GameState.INPROGRESS
        clock.schedule_unique(end_game, game_time)
    
    if pink_alien.collidepoint(pos):
        score += 1
        set_alien_hurt()
