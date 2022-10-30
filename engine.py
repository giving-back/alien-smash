import pygame

from enum import Enum
from random import randrange

class GameState(Enum):
    TOSTART = 1
    INPROGRESS = 2
    OVER = 3

WIDTH = 1000
HEIGHT = 800

start_game = Actor("ready", center=(WIDTH/2, HEIGHT/2))
game_over = Actor("gameover", center=(WIDTH/2, HEIGHT/2))
crosshair = Actor("crosshair")
pink_alien = Actor("pinkalien")
game_background = Actor("gamebackground")
walker = Actor("walk1")
bonus_clock = Actor("clock")

bonus_clock.x = -100
walker.x = 0
walker.y = 25


#Globals
game_state = GameState.TOSTART
score = 0
move_time = 1.0
game_time = 30.0
game_timer = game_time
walker_step = WIDTH // game_time
bonus_clock_appears = game_time // randrange(1, 5)

print(bonus_clock_appears)

def end_game():
    global game_state
    global game_timer
    global game_time

    game_timer = game_time
    walker.x = 0
    sounds.gameover.play()
    clock.unschedule(tick_timer)
    game_state = GameState.OVER

def tick_timer():
    global game_timer
    global walker_step
    game_timer -= 1
    walker.x += walker_step
    
    if walker.image == "walk1":
        walker.image = "walk2"
    else:
        walker.image = "walk1"

    if game_timer <= 0:
        end_game()

def draw_home():
    screen.blit("gamebackground", (0, 0))
    start_game.draw()
    crosshair.draw()
    screen.draw.text("ALIEN  SMASH", fontname="retro", fontsize=30, color=(0,0,0), center=(WIDTH/2, (HEIGHT - HEIGHT/4)-25))
    screen.draw.text("Created By Christian & Blake", fontsize=15, fontname="retro", color=(0,0,0), center=(WIDTH/2, HEIGHT - HEIGHT/4))

def draw_game():
    global game_timer
    screen.blit("gamebackground", (0, 0))
    pink_alien.draw()
    bonus_clock.draw()
    walker.draw()
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

def alien_random_move():
    pink_alien.x = randrange(pink_alien.width//2, WIDTH - (pink_alien.width//2))
    pink_alien.y = randrange(pink_alien.height//2, HEIGHT - (pink_alien.height//2))


def clock_appear():
    print("here")
    bonus_clock.x = 15

clock.schedule_interval(alien_random_move, move_time)
clock.schedule_interval(clock_appear, bonus_clock_appears)

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
        end_game()
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
    global game_timer
    global game_time
    global score
    global walker_step

    if start_game.collidepoint(pos):
        score = 0
        sounds.go.play()
        game_state = GameState.INPROGRESS
        clock.schedule_interval(tick_timer, 1.0)
    
    if pink_alien.collidepoint(pos):
        score += 1
        set_alien_hurt()

    if bonus_clock.collidepoint(pos):
        bonus_clock.x = -100
        game_timer = min(game_time, game_timer + 3)
        walker.x = max(0, walker.x - 3 * walker_step)
        
