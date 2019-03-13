#maze game
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
NAVY = (0, 0, 128)
WIDTH = 640
HEIGHT= 480

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
myfont = pygame.font.Font(None, 48)
myclock = pygame.time.Clock()
bgx = 0 #BG offset
bgy = 0
size = 32 #sprite size

#sprite class
class Spclass(pygame.sprite.Sprite):
  def __init__(self, x,y,filename):
    pygame.sprite.Sprite.__init__(self)
    self.image = \
      pygame.image.load(filename).convert()
    colorkey = self.image.get_at((0, 0))
    self.image.set_colorkey(colorkey)
    self.x = x
    self.y = y
    self.dir = 0
    self.walking = 0
    self.rect = self.image.get_rect()

#player
class Player(Spclass):
  def update(self):
    global bgx, bgy
    x1 = [ 0, 1, 0, -1]
    y1 = [-1, 0, 1,  0]
    if self.walking == 0:
      newdir = -1
      press = pygame.key.get_pressed()
      if press[pygame.K_UP]   : newdir = 0
      if press[pygame.K_RIGHT]: newdir = 1
      if press[pygame.K_DOWN] : newdir = 2
      if press[pygame.K_LEFT] : newdir = 3
      if newdir != -1:
        newx = int(self.x/size) + x1[newdir]
        newy = int(self.y/size) + y1[newdir]
        if bgdata[newy][newx] == " ":
          self.dir = newdir
          self.walking = 1
    else:
      self.x += x1[self.dir] * 4
      self.y += y1[self.dir] * 4
      if (self.x%size)==0 and (self.y%size)==0:
        self.walking = 0

    #画面のスクロール処理
    if self.x - bgx < 160          :bgx -= 1 
    if self.x - bgx >= WIDTH - 160 :bgx += 1 
    if self.y - bgy < 160          :bgy -= 1 
    if self.y - bgy >= HEIGHT - 160:bgy += 1 
    self.rect.left = self.x - bgx
    self.rect.top = self.y - bgy
    #衝突判定
    hitlist = pygame.sprite.spritecollide( \
      self, allgroup, False)
    if len(hitlist) >= 2: #2以上なら宝箱と接触
      imagetext = \
        myfont.render("GOAL!", True, WHITE) 
      screen.blit(imagetext, (260, 150)) 

#box
class Box(Spclass): 
  def update(self):
    global bgx, bgy
    self.rect.left = self.x - bgx
    self.rect.top = self.y - bgy

#迷路データ
bgdata = [  
  "11111111111111111111",
  "1 1     1   1      1",
  "1   111 1 1 1111 1 1",
  "11111     1 1    1 1",
  "1   11111 1 1 1111 1",
  "1 1   1   1 1    1 1",
  "111 1   1 1   11 1 1",
  "1   11111 111 11 1 1",
  "1 1  1      1 1  1 1",
  "11111111111111111111"]

blockimage = \
pygame.image.load("block.png").convert()
bgimage = pygame.Surface((size*20, size*10))
bgimage.fill(NAVY)

#迷路を描画する
for y in range(10):   
  for x in range(20):       
    if (bgdata[y][x]==" "): continue 
    bgimage.blit(blockimage, (size*x,size*y))

allgroup = pygame.sprite.Group()    
box = Box(size*18, size*8, "box.png")
allgroup.add(box)
player = Player(size*1, size*1, "man.png")  
allgroup.add(player) 
endflag = 0

#main loop
while endflag == 0:
  for event in pygame.event.get(): 
    if event.type == pygame.QUIT: endflag = 1

  screen.fill(BLACK)
  #迷路の表示
  screen.blit(bgimage, (-bgx, -bgy)) 
  allgroup.update() 
  allgroup.draw(screen) 
  myclock.tick(60)
  pygame.display.flip()

pygame.quit()