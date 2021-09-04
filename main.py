import pygame
import random
import os


################################################################
    # UP    --> W
    # DOWN  --> S
    # LEFT  --> A
    # RIGHT --> D
    # L_SHIFT --> enable SLOW MO
################################################################


resolution = (602, 652)
win = pygame.display.set_mode(resolution)
pygame.display.set_caption("Snake")

green = (0, 255, 0)
red = (255, 0, 0)
white = (255, 255, 255)
grey = (50, 50, 50)
apple = pygame.image.load('apple.jpg')


def round_rect(surf, rect, rad, color, thick=0):
	if not rad:
		pygame.draw.rect(surf, color, rect, thick)
	elif rad > rect.width / 2 or rad > rect.height / 2:
		rad = min(rect.width/2, rect.height/2)

	if thick > 0:
		r = rect.copy()
		x, r.x = r.x, 0
		y, r.y = r.y, 0
		buf = pygame.surface.Surface((rect.width, rect.height)).convert_alpha()
		buf.fill((0, 0, 0, 0))
		round_rect(buf, r, rad, color, 0)
		r = r.inflate(-thick*2, -thick*2)
		round_rect(buf, r, rad, (0, 0, 0, 0), 0)
		surf.blit(buf, (x, y))

	else:
		r = rect.inflate(-rad * 2, -rad * 2)
		for corn in (r.topleft, r.topright, r.bottomleft, r.bottomright):
			pygame.draw.circle(surf, color, corn, rad)
		pygame.draw.rect(surf, color, r.inflate(rad*2, 0))
		pygame.draw.rect(surf, color, r.inflate(0, rad*2))


class snake(object):
    body = []
    turns = {}

    def __init__(self, pos):
        self.head = cube(pos)
        self.body.append(self.head)

        self.dirX = 0
        self.dirY = 1
        self.TdirX = 1
        self.TdirY = 0
        self.dir, self.Tdir = "RIGHT", "RIGHT"

    def move(self, Cpos):
        global wid
        self.Cpos = Cpos                
        keys = pygame.key.get_pressed()
    
        if keys[pygame.K_a] and self.dir != "RIGHT":
            self.Tdir = "LEFT"
            self.TdirX = -1
            self.TdirY = 0
        elif keys[pygame.K_d] and self.dir != "LEFT":
            self.Tdir = "RIGHT"
            self.TdirX = 1
            self.TdirY = 0
        elif keys[pygame.K_w] and self.dir != "DOWN":
            self.Tdir = "UP"
            self.TdirX = 0
            self.TdirY = -1
        elif keys[pygame.K_s] and self.dir != "UP":
            self.Tdir = "DOWN"
            self.TdirX = 0
            self.TdirY = 1

        if Cpos == 0:
            self.dir = self.Tdir
            self.dirX = self.TdirX
            self.dirY = self.TdirY
            self.turns[self.head.pos[:]] = [self.dirX, self.dirY]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)  
            else:
                if c.dirX == -1 and c.pos[0] <= -1:
                    self.reset((270, 270))
                elif c.dirX == 1 and c.pos[0] >= wid-28:
                    self.reset((270, 270))
                elif c.dirY == 1 and c.pos[1] >= wid-28:
                    self.reset((270, 270))
                elif c.dirY == -1 and c.pos[1] <= -1:
                    self.reset((270, 270))
                else:
                    c.move(c.dirX, c.dirY)

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.drawSnake(surface, self.dir, True)
            else:
                c.drawSnake(surface, self.dir)

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirX, tail.dirY

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-30, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+30, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1]-30)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1]+30)))
        
        self.body[-1].dirX = dx
        self.body[-1].dirY = dy
    
    def reset(self, pos):
        global Food, Cpos, point, point2, point3
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        for i in range(0, 3):
            self.addCube()
        Food = cube(food(wid//30, Snake), color=red)
        self.dirX = 0
        self.dirY = 1
        self.TdirX = 1
        self.TdirY = 0
        self.dir, self.Tdir = "RIGHT", "RIGHT"
        Cpos = -1
        point2 = point
        if point > point3:
            point3 = point
        point = 1


class cube(object):
    w = resolution[0]-2
    rows = w//30
    
    def __init__(self, start, dirX=1, dirY=0, color=green):
        self.pos = start
        self.dirX = 1
        self.dirY = 0
        self.color = color

    def move(self, dirX, dirY):
        self.dirX = dirX
        self.dirY = dirY
        self.pos = (self.pos[0] + self.dirX, self.pos[1] + self.dirY)
    
    def drawSnake(self, surface, dir, eyes=False):
        i = self.pos[0]
        j = self.pos[1]
        x1, y1 = i+22, j+10    # i+centre+7 (centre=15)
        x2, y2 = i+22, j+22    # i+centre+7 (centre=15)

        round_rect(surface, pygame.Rect(i+2, j+2, 29, 29), 3, (0, 0, 0), thick=0)
        round_rect(surface, pygame.Rect(i+2, j+2, 29, 29), 3, self.color, thick=1)
        round_rect(surface, pygame.Rect(i+2+3, j+2+3, 23, 23), 3, self.color, thick=0)

        if dir == "RIGHT":
            x1, y1 = i+22, j+10
            x2, y2 = i+22, j+22
        elif dir == "LEFT":
            x1, y1 = i+10, j+10
            x2, y2 = i+10, j+22
        elif dir == "UP":
            x1, y1 = i+10, j+10
            x2, y2 = i+22, j+10
        elif dir == "DOWN":
            x1, y1 = i+22, j+22
            x2, y2 = i+10, j+22

        if eyes:
            radius = 2
            circleMiddle = (x1, y1)
            circleMiddle2 = (x2, y2)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)

    def drawFood(self, surface):
        i = self.pos[0]
        j = self.pos[1]

        surface.blit(apple, (i+4, j+4))
        #pygame.draw.circle(surface, self.color, (i+2+14, j+2+14), 13, 1)
        #pygame.draw.circle(surface, self.color, (i+2+14, j+2+14), 9, 0)


def food(rows, snake):

    positions = snake.body

    while True:
        x = (random.randrange(rows))
        y = (random.randrange(rows))

        if len(list(filter(lambda z: (z.pos[0]//30, z.pos[1]//30) == (x, y), positions))) > 0:
            continue
        else:
            break
    return (x*30, y*30)


def eat(Snake, Food):
    check = False
    if Snake.body[0].pos == (Food.pos[0], Food.pos[1]):
        check = True
    elif Snake.body[0].pos == (Food.pos[0], Food.pos[1]):
        check = True
    elif Snake.body[0].pos == (Food.pos[0], Food.pos[1]):
        check = True
    elif Snake.body[0].pos == (Food.pos[0], Food.pos[1]):
        check = True
    
    return check


def score(point, point2, point3, surface):
    pygame.font.init()
    myfont = pygame.font.SysFont('Consolas', 25)
    text = myfont.render('Score: ' + str(point) + '    L_Score: ' + str(point2) + '    H_Score: ' + str(point3), False, white)
    surface.blit(text, (8, 615))


def drawGrid(surface):
    global wid
    w = wid+2
    distance = 30
    x, y = 1, 1

    for r in range(wid//30):
        x = x + distance
        y = y + distance

        pygame.draw.line(surface, grey, (x, 0), (x, w-1))
        pygame.draw.line(surface, grey, (0, y), (w, y))

    pygame.draw.rect(win, white, pygame.Rect(0, 0, w, w), 1)
    pygame.draw.rect(win, white, pygame.Rect(0, w, w, 50), 1)


def failSafe(Snake):
    for x in range(len(Snake.body)):
        X, Y = 2*Snake.dirX, 2*Snake.dirY
        if X == -2: X = -1
        if Y == -2: Y = -1
        if (((Snake.body[0].pos[0]-abs(X)//2)//30+X), ((Snake.body[0].pos[1]-abs(Y)//2)//30+Y)) in list(map(lambda z: (z.pos[0]//30, z.pos[1]//30), Snake.body[x+1:])):
            return True
    return False


def draw_window(surface, dev):
    global Snake, Food, point, point2, point3, wid
    
    X, Y = 2*Snake.dirX, 2*Snake.dirY
    if X == -2: X = -1
    if Y == -2: Y = -1
    temp = (((Snake.body[0].pos[0]-abs(X)//2)//30+X)*30, ((Snake.body[0].pos[1]-abs(Y)//2)//30+Y)*30)
    
    surface.fill((0, 0, 0))
    score(point, point2, point3, surface)
    drawGrid(surface)
    Food.drawFood(surface)
    Snake.draw(surface)
    if dev:
        pygame.draw.circle(surface, white, temp, 1, 0)
    pygame.display.update()


def main():
    global wid, Snake, Food, Cpos, point, point2, point3
    clock = pygame.time.Clock()
    speed = 300
    wid = resolution[0]-2
    Snake = snake((270, 270))
    for i in range(0, 3):
        Snake.addCube()

    Food = cube(food(wid//30, Snake), color=red)
    isPlaying = True
    Cpos = -1

    HS = open("HScore.txt", "r")
    point, point2, point3 = 1, 0, int(HS.read())
    HS.close()
    temp = point3
    dev = False

    while isPlaying:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if point3 > temp:
                    HS = open("HScore.txt", "w")
                    HS.write(str(point3))
                    HS.close()
                pygame.quit()

    #########################
        if not dev and pygame.key.get_pressed()[pygame.K_LSHIFT] and Cpos == 0:
            dev = True
        elif dev and pygame.key.get_pressed()[pygame.K_LSHIFT] and Cpos == 0:
            dev = False

        if dev and failSafe(Snake):
            speed = 30
        else:
            speed = 300
    #########################

        clock.tick(speed)

        Cpos += 1
        if Cpos == 30:
            Cpos = 0
        
        Snake.move(Cpos)
        check = eat(Snake, Food)
        if check:
            point += 1
            Snake.addCube()
            Food = cube(food(wid//30, Snake), color=red)
            check = False

        for x in range(len(Snake.body)):
	    # This will check if any of the positions in our body list overlap
            X, Y = Snake.dirX, Snake.dirY
            if X == -1: X = 0
            if Y == -1: Y = 0
            if (((Snake.body[0].pos[0]-X)//30+X), ((Snake.body[0].pos[1]-Y)//30+Y)) in list(map(lambda z: (z.pos[0]//30, z.pos[1]//30), Snake.body[x+1:])):
                Snake.reset((270, 270))
                break
        
        draw_window(win, dev)

if __name__ == "__main__":
        main()
