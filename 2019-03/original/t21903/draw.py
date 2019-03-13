#draw test
import pygame

WIDTH = 640
HEIGHT= 480
BLACK = (  0,  0,  0)
WHITE = (255,255,255)
RED   = (255,  0,  0)
GREEN = (  0,255,  0)
BLUE  = (  0,  0,255)

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
myfont = pygame.font.Font(None, 32)
myclock = pygame.time.Clock()
screen.fill(BLACK)

#draw text
def drawtext(x,y,text):
  imagetext = myfont.render(text, True, WHITE)
  screen.blit(imagetext, (x, y))

#line
drawtext(20, 20, "pygame.draw.line")
startpos = (250, 20)
endpos = (450, 100)
pygame.draw.line(screen,WHITE,startpos,endpos) 

#rect
drawtext(20, 130, "pygame.draw.rect")
rect = (250, 130, 200, 100)
pygame.draw.rect(screen, RED, rect)

#circle
drawtext(20, 240, "pygame.draw.circle")
pos = (300, 290)
radius = 50
pygame.draw.circle(screen, GREEN, pos, radius)

#polygon
drawtext(20, 350, "pygame.draw.polygon")
poslist = [(250, 450), (300, 350), (350, 450)]
pygame.draw.polygon(screen, BLUE, poslist)

endflag = 0

while endflag == 0:
  for event in pygame.event.get():
    if event.type == pygame.QUIT: endflag=1

  myclock.tick(60)
  pygame.display.flip()

pygame.quit ()
