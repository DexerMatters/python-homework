import pygame
import random
import math

################################# pygame info ####################################

SCREEN_WIDTH = 30 * 40
SCREEN_HEIGHT = 30 * 40
CHUNK_SIZE = 30

FPS = 60
SLOWNESS = 5

WCHUNKS = math.floor(SCREEN_WIDTH / CHUNK_SIZE)
HCHUNKS = math.floor(SCREEN_HEIGHT / CHUNK_SIZE)

KEYBINDING = [
  (pygame.K_w, 3),
  (pygame.K_s, 1),
  (pygame.K_a, 2),
  (pygame.K_d, 0)
]

################################# pygame prep ####################################

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_WIDTH))


snake = [(10, 10)]     # present as a tuple queue list
food = [(random.randint(0, WCHUNKS), random.randint(0, HCHUNKS))]
direction = 0

def draw_rect(color, cood):
  pygame.draw.rect(
    screen, 
    color, 
    pygame.Rect(cood[0] * CHUNK_SIZE, cood[1] * CHUNK_SIZE, CHUNK_SIZE, CHUNK_SIZE)
  )

def draw():
  draw_rect("green", food[0])
  for e in snake:
    draw_rect("red", e)

def drop():
  food[0] = (random.randint(0, WCHUNKS), random.randint(0, HCHUNKS))

def move():
  head = snake[0]

  # Die when it overlaps its tail
  if head in snake[1::]:
    die()
    return
  
  # Die when it hits the boundary
  if head[0] < 0 or head [0] > WCHUNKS or head[1] < 0 or head[1] > HCHUNKS:
    die()
    return

  if head != food[0]:
    snake.pop()
  else:
    drop()
  match direction:
    case 0:  # Right
      snake.insert(0, (head[0] + 1, head[1]))
    case 1:  # Down
      snake.insert(0, (head[0], head[1] + 1))
    case 2:  # Left
      snake.insert(0, (head[0] - 1, head[1]))
    case 3:  # Up
      snake.insert(0, (head[0], head[1] - 1))

def die():
  post_delay()
  snake.clear()
  snake.append((10, 10))
  drop()

delay = [0]
def post_delay():
  delay[0] = 60

################################# pygame setup ####################################

clock = pygame.time.Clock()
tick = 0
running = True

while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  screen.fill("black")

    ## Key
  keys = pygame.key.get_pressed()
  for k, v in KEYBINDING:
    if keys[k]:
      direction = v
      # An extra movement rendered to improve sensitivity
      draw()

    ## Movement
  if delay[0] == 0:
    tick = tick + 1
    if tick == SLOWNESS:
      move()
      tick = 0
  else:
    delay[0] = delay[0] - 1
    
  ## Drawing
  draw()

  pygame.display.flip()
  clock.tick(FPS) 

pygame.quit()