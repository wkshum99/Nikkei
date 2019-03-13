#sprite test
import pygame
import random

WIDTH = 640
HEIGHT = 480
BLUE = (0, 0, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
myclock = pygame.time.Clock()

#sprite class
class Spclass(pygame.sprite.Sprite):
  #スプライトの初期化関数
  def __init__(self): 
    pygame.sprite.Sprite.__init__(self)
    #画像の読み込み
    self.image = \
      pygame.image.load("man.png").convert()  
    colorkey = self.image.get_at((0, 0))
    #透明色を設定する
    self.image.set_colorkey(colorkey)  
    self.rect = self.image.get_rect()
    self.rect.centerx = random.randrange(WIDTH)
    self.rect.centery = random.randrange(HEIGHT)
    self.x1 = random.randrange(-3, 3)
    self.y1 = random.randrange(-3, 3)

  #スプライトの移動処理を行う関数
  def update(self):  
    self.rect.centerx += self.x1
    self.rect.centery += self.y1
    if self.rect.centerx >= \
      WIDTH or self.rect.centerx < 0:
      self.x1 = -self.x1

    if self.rect.centery >= \
      HEIGHT or self.rect.centery < 0:
      self.y1 = -self.y1

#スプライト100個をグループに登録する
allgroup = pygame.sprite.Group() 
for i in range(100):          
  allgroup.add(Spclass()) 

endflag = 0

while endflag==0:
  for event in pygame.event.get():
    if event.type == pygame.QUIT: endflag = 1

  screen.fill(BLUE)
  #スプライトの移動処理
  allgroup.update()
  #スプライトの描画処理
  allgroup.draw(screen) 
  myclock.tick(60)
  pygame.display.flip()

pygame.quit()