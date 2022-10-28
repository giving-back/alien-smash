from random import randrange
import pygame

alien = Actor("alien")
alien.pos = 100, 65

WIDTH = 1000
HEIGHT = 700

score = 0
high_score = 0

def draw():
    screen.clear()
    screen.blit("space", (0, 0))
    alien.draw()
    screen.draw.text(f"Score: {score}", (0, 0))

def random_move():
    alien.x = randrange(alien.width//2, WIDTH - (alien.width//2))
    alien.y = randrange(alien.height//2, HEIGHT - (alien.height//2))

clock.schedule_interval(random_move, 1.0)

def update():
    if keyboard.f:
        pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    if keyboard.escape:
        exit()

def set_alien_hurt():
    alien.image = "burst"
    sounds.laser.play()
    clock.schedule_unique(set_alien_normal, 0.3)

def set_alien_normal():
    alien.image = "alien"

def on_mouse_down(pos):
    global score
    if alien.collidepoint(pos):
        score += 1
        set_alien_hurt()
    else:
        score -= 1
    
