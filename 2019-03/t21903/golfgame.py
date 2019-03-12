#3D golf game
import pygame
import math
import random

WIDTH = 640  
HEIGHT= 480  
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
myfont = pygame.font.Font(None, 48)
myclock = pygame.time.Clock()

#地形データの作成
mapdata = \
  [[0 for i in range(50)] for j in range(50)]
zmin = 999             
zmax = -999            
for y in range(50):    
  for x in range(50):  
    z = math.cos(math.radians(x * 30)) + \
      math.cos(math.radians(y * 40)) 
    mapdata[x][y] = z             
    if zmin > z: zmin = z 
    if zmax < z: zmax = z

cdeg = 0 #camera angle
cx = 0 #camera position
cy = 0
cz = 0
bx = 2 #ball position
by = 24
bz = 0
bdeg = 0 #ball angle
ex = 40 #cup position
ey = 26
ez = mapdata[ex][ey]

#移動処理の関数。戻り値は移動後のXY座標
def moveangle(x, y, deg, speed):
  x += math.cos(math.radians(deg)) * speed
  y += math.sin(math.radians(deg)) * speed
  return x, y

#2点のXY座標から距離と角度を算出する関数
def getdist(xa, ya, xb, yb): 
  dx = xa - xb
  dy = ya - yb
  tempdeg = math.degrees(math.atan2(dy, dx))
  tempdist = math.sqrt(dx * dx + dy * dy)
  return tempdist, tempdeg

#XYZ座標から表示用のXY座標を算出する関数
def getxy(x, y, z):  
  if x<0 or x>49 or y<0 or y>49 :return -1, -1
  dist, deg = getdist(x, y, cx, cy)
  deg = deg - cdeg
  if deg > 180 :deg -= 360
  if deg < -180:deg += 360
  #カメラの外側にある場合は-1, -1を返す
  if abs(deg)>60: return -1, -1 
  if dist == 0: dist = 0.01
  dz = z - cz
  gx = deg * (WIDTH / 2) / 45 + WIDTH / 2
  gy = HEIGHT / 2 + dz * 120 / dist
  return gx, gy

#テキスト表示用関数
def drawtext(x, y, text):  
  imagetext = myfont.render(text, True, WHITE)
  screen.blit(imagetext, (x, y))

#main loop
seq = 0
endflag = 0

while endflag == 0:
  for event in pygame.event.get():
    if event.type == pygame.QUIT: endflag=1

  screen.fill(BLACK)
  #空の描画
  pygame.draw.rect(screen, \
    BLUE, (0, 0, WIDTH, HEIGHT/2))   
  #draw map
  for mode in range(2):
    for j in range(50):
      x2 = -1
      y2 = -1
      for i in range(50):
        if mode:
          x = i
          y = j
        else:
          x = j
          y = i
        #地形データから表示用の座標を算出 
        z = mapdata[x][y]  
        x1, y1 = getxy(x, y, z) 
        if x1 != -1 and x2 != -1:
          r = 255 - (z-zmin)*255/(zmax-zmin)
          c = (r, 200, 0)
          #地形の描画
          pygame.draw.line(screen, \
            c, (x1, y1), (x2, y2)) 

        x2 = x1
        y2 = y1

  gx, gy = getxy(bx, by, bz)
  #ball
  pygame.draw.circle(screen, \
    WHITE, (int(gx), int(gy)), 4)   
  gx, gy = getxy(ex, ey, ez)
  #cup
  pygame.draw.circle(screen, \
    RED, (int(gx), int(gy)), 4)     
  if seq == 0:
    #最初のカメラアングルを算出
    dist, cdeg = getdist(ex, ey, bx, by) 
    bz = mapdata[int(bx)][int(by)]
    bspeed = 0 #ball speed
    bz1 = 0 #ball z speed
    seq = 1
  elif seq==1:
    #ボールを中心にカメラ座標を算出
    cx, cy = moveangle(bx, by, cdeg + 180, 3) 
    cz = bz - 2
    bspeed += 0.05
    if bspeed > 1: bspeed = 0
    #ボールを発射するパワーを表示
    rect = (150, 400, bspeed*100, 20)  
    pygame.draw.rect(screen, RED, rect)
    drawtext(150, 430, "PUSH SPACE KEY")
    press = pygame.key.get_pressed()
    #カーソルキーで方向指定
    if press[pygame.K_LEFT]: cdeg -= 2     
    if press[pygame.K_RIGHT]: cdeg += 2 
    if press[pygame.K_SPACE]: 
      bdeg = cdeg    
      bz1 = -bspeed
      #スペースキーでボールを発射
      cx, cy = moveangle(bx, by, bdeg + 60, 15) 
      dist, cdeg = getdist(bx, by, cx, cy)
      seq = 2 
  else:
    #move ball 
    bx, by = moveangle(bx, by, bdeg, bspeed)
    #move camera 
    cx, cy = moveangle(cx, cy, bdeg, bspeed) 
    if bx<0 or by<0 or bx>49 or by>49:
      drawtext(150, 240, "OB")
      break

    gz = mapdata[int(bx)][int(by)]
    #ボールが地面で反射する処理
    if gz < (bz+bz1): bz1 *= -0.7 
    bspeed *= 0.96 
    bz += bz1
    #ボールの減速と落下処理
    bz1 += 0.05    
    dist, deg = getdist(bx, by, ex, ey)
    #ボールとカップの衝突判定
    if dist<0.4 and abs(bspeed)<0.1:
      drawtext(240, 120, "CUP IN")  
      break    

    if abs(bspeed)<0.02:
      bspeed = 0
      seq = 0

  myclock.tick(30)
  pygame.display.flip()

for i in range(90):
  myclock.tick(30)
  pygame.display.flip()

pygame.quit()
