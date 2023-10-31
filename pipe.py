import pygame
import sys
import random
import os

pygame.init()

clock = pygame.time.Clock()

W=H=602
screen = pygame.display.set_mode((W,H))
pygame.display.set_caption('pipe!')
screen.fill('white')

n=0
cnt=0
x=[]
y=[]
e=[]

mp=[]
org=[]
sta=[]
rot=[]

Q=0

def choose_n():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if pos[1]<400 or pos[1]>450:
                    continue
                for i in range(9):
                    if pos[0]>=50+i*55 and pos[0]<=50+i*55+50:
                        global n
                        n=i+4
                        main()
                        return
        
        text = pygame.image.load('pics/choose.png')
        pic = pygame.image.load('pics/choose_n.png')
        screen.fill('white')
        screen.blit(text,(50,360))
        screen.blit(pic,(50,400))
        pygame.display.flip()

def generate_map():
    global x
    global y
    x=[]
    y=[]
    for i in range(n+1):
        x.append([])
        for j in range(n):
            x[i].append(random.choice([0,1]))
    for i in range(n):
        y.append([])
        for j in range(n+1):
            y[i].append(random.choice([0,1]))

def generate_grid():
    global e
    global rot
    global sta
    e=[]
    rot=[]
    sta=[]
    for i in range(n):
        mp.append([0]*n)
        rot.append([0]*n)
        sta.append([0]*n)
        e.append([])
        for j in range(n):
            e[i].append([x[i][j],y[i][j],x[i+1][j],y[i][j+1]]) # 9,0,3,6'o cleck direction
            mp[i][j] = x[i][j]+x[i+1][j]+y[i][j]+y[i][j+1]
                
            if mp[i][j] == 2:
                if x[i][j] == x[i+1][j]:
                    mp[i][j]=2.2
                    if x[i][j]==1:
                        rot[i][j]=0
                    else:
                        rot[i][j]=1
                else:
                    mp[i][j]=2.1
                    if x[i][j]==y[i][j]==1:
                        rot[i][j]=0
                    elif y[i][j]==x[i+1][j]==1:
                        rot[i][j]=1
                    elif x[i+1][j]==y[i][j+1]==1:
                        rot[i][j]=2
                    else:
                        rot[i][j]=3
            elif mp[i][j]==3:
                if y[i][j+1]==0:
                    rot[i][j]=0
                elif x[i][j]==0:
                    rot[i][j]=1
                elif y[i][j]==0:
                    rot[i][j]=2
                else:
                    rot[i][j]=3
            elif mp[i][j]==1:
                if x[i][j]==1:
                    rot[i][j]=0
                elif y[i][j]==1:
                    rot[i][j]=1
                elif x[i+1][j]==1:
                    rot[i][j]=2
                else:
                    rot[i][j]=3
            sta[i][j]=rot[i][j]
            rot[i][j]=random.choice([0,1,2,3])
            sta[i][j]+=rot[i][j]

def draw_grid():
    screen.fill('white')
    gridline = pygame.image.load('pics/'+str(n)+'.png')
    screen.blit(gridline,((12-n)*25,(12-n)*25))
    for i in range(n):
        for j in range(n):
            if mp[i][j] == 0:
                continue
            pic = pygame.image.load('pics/pipe/'+str(mp[i][j])+'e.png')
            pic = pygame.transform.rotate(pic, -(sta[i][j])*90)
            screen.blit(pic,((12-n+2*i)*25,(12-n+2*j)*25))

def check_finish():
    if Q:
        for j in range(n):
            for i in range(n):
                print([e[i][j][(0-rot[i][j])%4],e[i][j][(1-rot[i][j])%4],e[i][j][(2-rot[i][j])%4],e[i][j][(3-rot[i][j])%4]],end='')
            print('')
    
    for i in range(n):
        for j in range(n):
            if i>0 and e[i][j][(0-rot[i][j])%4] != e[i-1][j][(2-rot[i-1][j])%4]:
                if Q:
                    return (i,j,0)
            if i+1<n and e[i][j][(2-rot[i][j])%4] != e[i+1][j][(0-rot[i+1][j])%4]:
                if Q:
                    return (i,j,1)
                return False
            if j>0 and e[i][j][(1-rot[i][j])%4] != e[i][j-1][(3-rot[i][j-1])%4]:
                if Q:
                    return (i,j,2)
                return False
            if j+1<n and e[i][j][(3-rot[i][j])%4] != e[i][j+1][(1-rot[i][j+1])%4]:
                if Q:
                    return (i,j,3)
                return False

    return True

def main():
    generate_map()
    generate_grid()
    
    px=-1
    py=-1
    global cnt
    
    while True:
        
        clock.tick(20)
        
        draw_grid()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                cnt+=1
                pos = event.pos
                px = (pos[0] - (12-n)*25)//50
                py = (pos[1] - (12-n)*25)//50
                if px>=0 and px<n and py>=0 and py<n:
                    rot[px][py] = (rot[px][py]+1)%4
                    sta[px][py] = (sta[px][py]+1)%4
                if check_finish():
                    draw_grid()
                    pygame.display.flip()
                    finish_one_round()
                    return
                
            if event.type == pygame.MOUSEMOTION:
                pos = event.pos
                px = (pos[0] - (12-n)*25)//50
                py = (pos[1] - (12-n)*25)//50

            #tester part
            if event.type == pygame.KEYDOWN:
                print("question")
                global Q
                Q=1
                print(check_finish())
                Q=0
                
        if px>=0 and px<n and py>=0 and py<n:
            pic = pygame.image.load('pics/select.png')
            screen.blit(pic,((12-n+2*px)*25,(12-n+2*py)*25))
        pygame.display.flip()
    
def finish_one_round():
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        screen.fill('white')
        f = pygame.font.Font('fonts/calibri.ttf',30)
        t1=f.render("Finished!",True,'black',(255,255,255))
        t2=f.render("clicks:"+str(cnt),True,'black',(255,255,255))
        # time to be added
    
        screen.blit(t1,(235,200))
        screen.blit(t2,(235,250))
        pygame.display.flip()

choose_n()
