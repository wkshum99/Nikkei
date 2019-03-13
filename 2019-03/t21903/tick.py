#tick test
import pygame

WIDTH = 640
HEIGHT= 480
BLACK = (  0,  0,  0)
WHITE = (255,255,255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
myfont = pygame.font.Font(None, 32)
myclock = pygame.time.Clock()
loopcnt = 0
endflag = 0

while endflag==0:
  for event in pygame.event.get():
    if event.type == pygame.QUIT: endflag = 1

  screen.fill(BLACK)
  loopcnt += 1
  imagetext = myfont.render(str(loopcnt), True, WHITE)
  screen.blit(imagetext, (320, 240))
  myclock.tick(60)
  pygame.display.flip()

pygame.quit ()
