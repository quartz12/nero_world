import math

import numpy as np
import pygame
from ii_main import nero1, nero2
import os
import pickle
import matplotlib.pyplot as plt


def sigm(a):
    return 1/(1+np.exp(-a))

pygame.font.init()

WIDTH = 1900
HEIGHT = 1000
FPS = 0


#всякие переменные
line_rect = 10 #длина клетки
line_world = 0.84 #длина мира в процентах
color_badgraund = {'all':(255, 255, 255), 'lines':(10, 10, 10), 'wall':(10, 10, 10), 'text':(100, 100, 100), 'button_color_on':(200, 100, 100), 'button_color_of':(100, 50, 50), 'collor_menu':[20, 20, 20], 'collor_see':[200, 200, 10], 'color_cirkl':[0, 0, 0]} #цвета мира
gamers = pygame.sprite.Group() #все игроки
piples_reestr = {}#реестр существ
sea_lenn = {'1':[1, -1], '2':[1, 0], '3':[1, 1], '4':[0, 1], '5':[-1, 1], '6':[-1, 0], '7':[-1, -1], '8':[0, -1]} #переменная изменений позиции в зависимости от поворота
font = pygame.font.Font(None, 25) #ширифт
pause = False #пауза
pipl_see = None #цель для мышки
butons= {} #кнопки
data = os.getcwd()#дериктория
gamers_set=500 #количество особей при спавне
group=1 #группа мозгов
if group==1: neros_group=[6, 3, 4, 6] #ввод при создании мозгов
else: neros_group=100
ags=np.array([])#умершие в день
delags = np.array([])#умершие в средем
pro = 0#пропуск хода
sredl=np.array([]) #выживаемость поселения
epoh = 0 #количество эпох
update_tik=0
update_tik_all=0 #количество тиков между апдатами
porog = 12000 #порог количества особей
gamers_py = np.array([]) #група обьектов сущностей
visir = 0#режим отображения


#число в rjb
def hex_to_rgb(value):
    value = abs(int(value))
    try:
        r, g, b = value.to_bytes(3, byteorder='big')
        return [r, g, b]
    except:
        return [0, 0, 0]

#взаимодействие кнопок
def but_on(name):
    global screen
    global update_tik_all
    global gamers
    global delags
    global pro
    global visir
    if name=='reset':
        start_game()
    if name=='tik+':
        update_tik_all+=1
    if name=='tik-':
        update_tik_all-=1
    if name=='load':
        try:
            with open(data+'\data'+str(group)+'.pickle', 'rb') as f:
                gamers = pickle.load(f)
                set_reestr()
                for i in gamers:
                    piples_reestr[' '.join(map(str, i.pos))]=i
        except:
            print('no save')
    if name=='save':
        with open(data+'\data'+str(group)+'.pickle', 'wb') as f:
            pickle.dump(gamers, f)
    if name=='l_auto':
        print('qsave_load')
        with open(data+'\qdata'+str(group)+'.pickle', 'rb') as f:
            gamers = pickle.load(f)
            set_reestr()
            for i in gamers:
                piples_reestr[' '.join(map(str, i.pos))]=i
    if name=='sred':
        plt.plot(delags)
        plt.show()
    if name=='sredl':
        plt.plot(sredl)
        plt.show()
    if name=='pro+':
        pro+=2
    if name=='pro-':
        pro-=2
    if name=='vis':
        visir+=1
        if visir>3:
            visir=0

class button():
    def __init__(self, pos, size, color_on=color_badgraund['button_color_on'], color_of=color_badgraund['button_color_of'], text_on='restart', text_of='restart', size_fond=30, color_text=color_badgraund['text'], text_pos=[0, 0], ret=False, set_but='None'):
        self.onof=False #значение
        self.sur = pygame.surface.Surface(size) #поверхность
        self.color_on = color_on #звет фона
        self.color_of = color_of
        self.color=color_of
        self.text_pos=text_pos #позиция текста(центра)
        self.text_on=text_on
        self.text_of=text_of
        self.text=text_of
        self.size_fond=size_fond
        self.color_text=color_text
        self.retu=ret
        self.pos=pos
        self.size=size
        self.set_but=set_but
        self.udate() #применить изменения
    def udate(self): #применение изменений
        if self.onof:
            self.color = self.color_on
            self.text = self.text_on
        else:
            self.color = self.color_of
            self.text = self.text_of
        font = pygame.font.Font(None, self.size_fond)
        text = font.render(str(self.text), True, self.color_text)
        self.sur.fill(self.color)
        self.rect=pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.sur.blit(text, [self.rect.size[0]//2-text.get_size()[0]//2, self.rect.size[1]//2-text.get_size()[1]//2])
    def ret(self): #возврат кнопки
        return self.sur
    def on(self, pos): #нажатие
        if pos[0] > self.rect.topleft[0]:
            if pos[1] > self.rect.topleft[1]:
                if pos[0] < self.rect.bottomright[0]:
                    if pos[1] < self.rect.bottomright[1]:
                        if not self.retu:
                            self.onof = not self.onof
                            self.udate()
                        else:
                            but_on(self.set_but)

#иницилизация реестра
def set_reestr():
    global WIDTH
    global HEIGHT
    global line_rect
    global line_world
    for i in range(int(WIDTH*line_world//line_rect)):
        for a in range(int(HEIGHT//line_rect)):
            if i==0 or i == int(WIDTH*line_world//line_rect)-1 or a==0 or a==int(HEIGHT//line_rect)-1:
                piples_reestr[str(i)+' '+str(a)]=-1
            else:
                piples_reestr[str(i) + ' ' + str(a)] = 0
set_reestr()

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

#создание сетки и меню
menu_displau = pygame.surface.Surface((WIDTH*(1-line_world), HEIGHT))
menu_displau.fill(color_badgraund['collor_menu'])
display = pygame.surface.Surface((WIDTH, HEIGHT))
display.fill(color_badgraund['all'])
for i in range(HEIGHT//line_rect):
    pygame.draw.line(display, color_badgraund['lines'], [0, i*line_rect], [WIDTH*line_world, i*line_rect])
for i in range(int(WIDTH*line_world)//line_rect+1):
    pygame.draw.line(display, color_badgraund['lines'], [i*line_rect, 0], [i*line_rect, HEIGHT])



#создаем сетку увеличения
display_sea_size = [200, 200]
display_sea_size_rekt = 40
display_sea_pos = [WIDTH-display_sea_size[0]-50, HEIGHT-display_sea_size[0]-50]
display_sea = pygame.surface.Surface([display_sea_size[0]+1, display_sea_size[1]+1])
display_sea.fill(color_badgraund['all'])
for i in range(display_sea_size[1]//display_sea_size_rekt+1):
    pygame.draw.line(display_sea, color_badgraund['lines'], [0, (i*display_sea_size_rekt)], [display_sea_size[0], (i*display_sea_size_rekt)])
for i in range(int(display_sea_size[0]//display_sea_size_rekt+1)):
    pygame.draw.line(display_sea, color_badgraund['lines'], [i*display_sea_size_rekt, display_sea_size[1]], [i*display_sea_size_rekt, 0])


#создание кнопок
butons['test']=button([WIDTH * line_world + 10, HEIGHT * 0.1 + 105], [70, 30], ret=True, set_but='reset', text_of='spawn')
butons['auto_start']=button([WIDTH * line_world + 10+72, HEIGHT * 0.1 + 105], [70, 30], text_on='auto_spaun', text_of='not_spawn')
butons['tik+']=button([WIDTH * line_world + 10+60, HEIGHT * 0.1 + 140], [30, 30], ret=True, set_but='tik+', text_of='+')
butons['tik-']=button([WIDTH * line_world + 10, HEIGHT * 0.1 + 140], [30, 30], ret=True, set_but='tik-', text_of='-')
butons['paus']=button([WIDTH * line_world + 10+95, HEIGHT * 0.1 + 140], [50, 30], text_on='pause', text_of='run')
butons['save']=button([WIDTH * line_world + 10+70, HEIGHT * 0.1 + 175], [60, 30], ret=True, set_but='save', text_of='save')
butons['load']=button([WIDTH * line_world + 10, HEIGHT * 0.1 + 175], [60, 30], ret=True, set_but='load', text_of='load')
butons['l_auto']=button([WIDTH * line_world + 10+140, HEIGHT * 0.1 + 175], [60, 30], ret=True, set_but='l_auto', text_of='q_save')
butons['sred']=button([WIDTH * line_world + 10, HEIGHT * 0.1 + 210], [60, 30], ret=True, set_but='sred', text_of='sred')
butons['sredl']=button([WIDTH * line_world + 10+70, HEIGHT * 0.1 + 210], [60, 30], ret=True, set_but='sredl', text_of='sredl')
butons['pro+']=button([WIDTH * line_world + 10+60, HEIGHT * 0.1 + 245], [30, 30], ret=True, set_but='pro+', text_of='+')
butons['pro-']=button([WIDTH * line_world + 10, HEIGHT * 0.1 + 245], [30, 30], ret=True, set_but='pro-', text_of='-')
butons['vis']=button([WIDTH * line_world + 120, HEIGHT * 0.1 + 245], [60, 30], ret=True, set_but='vis', text_of='set_vis')



class pepl_nero1(pygame.sprite.Sprite):
    #рождение
    def __init__(self, group, nerons, spawn=True, brain=None, pos=None, sea=8, old_max=1000, enerji_max=50, parents=None, enerji=10):
        super().__init__()
        self.out_brain_set='' #вывод итогов на экран
        self.out="я родился" #вывод мыслей на экран
        self.group = group #вид мозга(пока 2)
        self.old_max=old_max #максимальный возраст существ
        self.sea = sea #направление взгляда
        self.enerji_max = enerji_max #максимальная энергия
        self.old=0 #возрост
        self.enerji=enerji #энергия
        self.nerons = nerons #либо количество нейронов либо длина днк в зависимости от мозгов
        self.color = [0, 254, 0] #цвет
        if spawn: #если заспавнили
            #рандомная позииця
            self.pos = [np.random.randint(2, WIDTH*line_world//line_rect-2), np.random.randint(2, HEIGHT//line_rect-2)]
            while self.seart(self.pos)!=0:
                self.pos = [np.random.randint(2, WIDTH * line_world // line_rect - 2),
                       np.random.randint(2, HEIGHT // line_rect - 2)]
        else:
            self.pos = pos #не рандомная позиция

        #установка мозгов
        if group==1:
            if spawn:
                self.brain=nero1(nerons)
            else:
                self.brain=brain
        if group==2:
            if spawn:
                self.brain=nero2(nerons)
            else:
                self.brain=brain
        #установки риестра
        piples_reestr[' '.join(map(str, self.pos))]=self
        self.color_parents=hex_to_rgb(sum(self.brain.nerons_all)*10000)
        self.color_energi=[self.enerji*2, 0, 0]

    #основной цикл
    def update(self):
        global ags
        global piples_reestr
        self.color_energi=[self.enerji / self.enerji_max*255, 0, 0]
        self.old+=1 #старение
        self.enerji-=2 #городание
        #взгляд перед собой перс стена и пустота соответственно
        sea = self.seart(self.box_set())
        if sea == 0: pusto=1
        else: pusto=0
        if sea == -1: stena=1
        else: stena=0
        if sea != 0 and sea != -1:
            rods = self.del_pip(sea) #устанавливаем разницу в генах с тем на кого смотрим
        else: rods=0
        inp = [pusto, stena, rods, 1-self.enerji / self.enerji_max, 1-self.old / self.old_max, sigm(abs(rods))] #ввод окружения
        self.out_brain_set = self.brain.run(inp) #вывод мозгов
        if self.out_brain_set[0]!=None: #если мозги выводят
            out_brain_set = np.delete(self.out_brain_set.copy(), -1) #удаляем 5 нейрон
            set_o = np.argmax(out_brain_set) #узнаем доминирующий нйрон
            if set_o==2 and self.out_brain_set[2]!=0: #если доминирует 2 то спавн
                self.spawn_set()
                self.out="ражаю"
            if set_o==3 and self.out_brain_set[3]!=0: #если доминирует 3 фотосинте
                self.fotos()
                self.out="ем солнце"
            if set_o==0 and self.out_brain_set[0]!=0: #если доминирует 0 шаг вперед
                self.move()
                self.out="иду"
            if set_o==1 and self.out_brain_set[1]!=0: #если доминирует 1 атаковать
                self.attak()
                self.out="бью"
            if self.out_brain_set[4]>0.5:
                self.rootr(self.out_brain_set[5]) #поворот от 6 нейгона
        if self.enerji <= 0 or self.old >= self.old_max: #смерть от старости или голода
            ags = np.append(ags, self.old)
            gamers.remove(self)

    #спавн детей
    def spawn_set(self):
        a=self.sea+4
        if a>8: a=a-8
        box = self.box_set(a)
        if self.seart(box)==0 and self.enerji>7 and len(gamers)<porog:
            self.enerji -= 7
            brain=self.brain.spawn(5, 3)
            gamers.add(pepl_nero1(self.group, self.nerons, False, brain, box, self.sea, parents=None, enerji=5))

    #выбор блока перед собой(возвращает позицию)
    def box_set(self, a=None):
        if a==None: a=self.sea
        pos_sear = [0, 0]
        pos_sear[0] = self.pos[0] + sea_lenn[str(a)][0]
        pos_sear[1] = self.pos[1] + sea_lenn[str(a)][1]
        return pos_sear

    #рвзница в геноме
    def del_pip(self, a):
        return np.sum(self.brain.nerons_all-a.brain.nerons_all)

    #взгляд(возвращает то что находиться в выбраном блоке)
    def seart(self, pos_sear):
        pos_sear = ' '.join(map(str, pos_sear))
        try:
            return piples_reestr[pos_sear]
        except:
            print('error searth pos_sear:'+pos_sear+' '+'pos:'+str(self.pos))
            return -1
    #движение вперед
    def move(self):
        box = self.box_set()
        box_exampol=self.seart(box)
        if box_exampol==0:
            piples_reestr[' '.join(map(str, self.pos))]=0
            self.pos=box
            piples_reestr[' '.join(map(str, self.pos))] = self

    #фотосинте
    def fotos(self):
        if self.enerji<self.enerji_max:
            self.enerji+=7
            if self.color[1]<200:
                self.color[1]+=100
                self.color[0]-=100

    #поворот в зависимости от входа
    def rootr(self, a):
        if a>0.5:
            self.sea+=1
        elif a<0.5:
            self.sea-=1
        if self.sea>8:
            self.sea=1
        if self.sea<1:
            self.sea=8

    #атака
    def attak(self):
        sea = self.seart(self.box_set())
        if sea!=0 and sea!=-1:
            pos_sea=sea.pos
            self.enerji+=sea.enerji//2
            gamers.remove(sea)
            piples_reestr[' '.join(map(str, pos_sea))]=0
            if self.color[0]<200:
                self.color[0]+=100
                self.color[1]-=100
        else:
            self.enerji-=1


#выбор блока по координатам
def box_set(a):
    pos_sear = ' '.join(map(str, a))
    try:
        return piples_reestr[pos_sear]
    except:
        return -1

#создание цевилизации
def start_game():
    global spawns
    global gamers
    global ags
    global gamers_py
    global delags
    spawns=True
    delags = np.append(delags, np.mean(ags)) #среднее выживание
    ags = np.array([])  # умершие в день
    set = pepl_nero1(group, neros_group, sea=np.random.randint(1, 8),
                         pos=[random.randint(1, int(WIDTH * line_world // line_rect) - 2),
                              random.randint(1, HEIGHT // line_rect - 2)])
    gamers.add(set)

#отрисовка текста
def render_text(text, bak=None):
    text = font.render(str(text), True, color_badgraund['text'])
    sur=pygame.surface.Surface((text.get_size()))
    if bak!=None:
        sur.fill(bak)
        text.blit(sur, [0, 0])
        return sur
    return text

#отрисовка
def draw(screan):
    screen.blit(display, (0, 0)) #рисовка поля
    #отрисовка реестра
    for i in piples_reestr.keys():
        pos = [int(a) for a in i.split(' ')]
        if piples_reestr[i] == -1:
            pygame.draw.rect(screan, color_badgraund['wall'],
                             [pos[0] * line_rect, pos[1] * line_rect, line_rect, line_rect])
        elif piples_reestr[i] in gamers:
            if visir==0: color=piples_reestr[i].color
            elif visir==1: color=piples_reestr[i].color_parents
            elif visir==2: color=piples_reestr[i].color_energi
            else: color=(100, 100, 100)
            try:
                pygame.draw.rect(screan, color,
                                 [pos[0] * line_rect, pos[1] * line_rect, line_rect, line_rect])
            except: pass

    #######
    screan.blit(menu_displau, [WIDTH*line_world, 0])#рисовка меню
    # рисовка текста
    screan.blit(render_text('количество особей: ' + str(len(gamers))), [WIDTH * line_world + 10, HEIGHT * 0.1])
    screan.blit(render_text('FPS: ' + str(int(clock.get_fps()))), [WIDTH * line_world + 10, HEIGHT * 0.1 + 15])
    screan.blit(render_text('epoh: ' + str(epoh)), [WIDTH * line_world + 10, HEIGHT * 0.1 + 30])
    #отрисовка сетки увеличения
    screan.blit(display_sea, display_sea_pos)
    #отрисовка выбранного
    if pipl_see != None:
        #текст
        screan.blit(render_text('енергия: ' + str(pipl_see.enerji)), [WIDTH * line_world + 10, HEIGHT * 0.1 + 45])
        screan.blit(render_text('старость: ' + str(pipl_see.old)), [WIDTH * line_world + 10, HEIGHT * 0.1 + 60])
        screan.blit(render_text('o: ' + str(pipl_see.out)+'  '+str(round(sum(pipl_see.brain.nerons_all), 2))), [WIDTH * line_world + 10, HEIGHT * 0.1 + 90])
        try:
            screan.blit(render_text('o: ' + str(np.round(pipl_see.out_brain_set, 2))), [WIDTH * line_world + 10, HEIGHT * 0.1 + 75])
        except:
            screan.blit(render_text('error'), [WIDTH * line_world + 10, HEIGHT * 0.1 + 75])
        #квадрат вокруг
        pygame.draw.rect(screan, color_badgraund['collor_see'], [pipl_see.pos[0] * line_rect, pipl_see.pos[1] * line_rect, line_rect+3, line_rect+3], 3)
        #геном
        if pipl_see.group==2:
            for i in range(pipl_see.brain.size):
                if i == pipl_see.brain.run_id:
                    pygame.draw.rect(screan, color_badgraund['collor_see'],
                                     [WIDTH * line_world + 10 + i % 10 * 22, HEIGHT * 0.1 + 300 + 15 + i // 10 * 22, 22,
                                      22], 3)
                screan.blit(render_text(str(pipl_see.brain.brain[i])),
                            [WIDTH * line_world + 10 + i % 10 * 22, HEIGHT * 0.1 + 300 + 15 + i // 10 * 22])
        else:
            pis_d_x=50
            for i in range(pipl_see.nerons[0]):
                try:
                    pygame.draw.circle(screan, [abs(pipl_see.brain.input[i]*250), 50, 50], [WIDTH*line_world+10+pis_d_x, 450+i*40], 10)
                    for a in range(pipl_see.nerons[2]):
                        pygame.draw.line(screan, [sigm(pipl_see.brain.nero_input[i][a])*250, 0, 0], [WIDTH*line_world+10+pis_d_x, 450+i*40], [WIDTH*line_world+10+30+pis_d_x, 450+a*40+(pipl_see.nerons[0]-pipl_see.nerons[1])*13], 1)
                except:pass
            for i in range(pipl_see.nerons[1]):
                for a in range(pipl_see.nerons[2]):
                    try:
                        pygame.draw.circle(screan, [sigm(pipl_see.brain.nerons_out[i*a+a]) * 250, 50, 50],[WIDTH * line_world + 40+i*40+pis_d_x, 450 + a*40+(pipl_see.nerons[0]-pipl_see.nerons[1])*13], 10)
                    except: pass
            for i in range(pipl_see.nerons[1]-1):
                for a in range(pipl_see.nerons[2]):
                    try:
                        for n in range(pipl_see.nerons[2]):
                            pygame.draw.line(screan, [sigm(pipl_see.brain.nero_sloi[i][a][n]) * 250, 0, 0],
                                             [WIDTH * line_world + 40+i*40+pis_d_x, 450 + a*40+(pipl_see.nerons[0]-pipl_see.nerons[1])*13], [WIDTH * line_world + 40+(i+1)*40+pis_d_x, 450 + n*40-a*40+a*40+(pipl_see.nerons[0]-pipl_see.nerons[1])*13], 1)
                    except:pass
            for i in range(pipl_see.nerons[3]):
                try:
                    pygame.draw.circle(screan, [abs(pipl_see.brain.nerons_out[len(pipl_see.brain.nerons_out)-(pipl_see.nerons[3]-i)]*250), 50, 50], [WIDTH*line_world+pipl_see.nerons[2]*40+pis_d_x, 450+i*40], 10)
                    for a in range(pipl_see.nerons[2]):
                        pygame.draw.line(screan, [sigm(pipl_see.brain.nero_input[i][a])*250, 0, 0], [WIDTH * line_world + 40+(pipl_see.nerons[1]-1)*40+pis_d_x, 450 + a*40+(pipl_see.nerons[0]-pipl_see.nerons[1])*13], [WIDTH*line_world+pipl_see.nerons[2]*40+pis_d_x, 450+i*40], 1)
                except:pass
        #отрисовка увиличения
        for i in range(5):
            for a in range(5):
                pos_draw=[display_sea_pos[0]+a*display_sea_size_rekt, display_sea_pos[1]+i*display_sea_size_rekt]
                pos_sea=[pipl_see.pos[0]-2+a, pipl_see.pos[1]-2+i]
                pos_sea=box_set(pos_sea)
                #отриоовка стен
                if pos_sea==-1:
                    pygame.draw.rect(screan, color_badgraund['wall'], [pos_draw[0], pos_draw[1], display_sea_size_rekt, display_sea_size_rekt])
                #отрисовка существ
                elif pos_sea!=0:
                    pygame.draw.rect(screan, pos_sea.color, [pos_draw[0], pos_draw[1], display_sea_size_rekt, display_sea_size_rekt])
                    pygame.draw.circle(screan, color_badgraund['color_cirkl'], [pos_draw[0]+display_sea_size_rekt/2+display_sea_size_rekt/2*math.cos(math.radians((pos_sea.sea-2)*45)), pos_draw[1]+display_sea_size_rekt/2+display_sea_size_rekt/2*math.sin(math.radians((pos_sea.sea-2)*45))], 4)
    else:
        #выбор генома
        screan.blit(render_text('выбранно: ' + str(pipl_see)), [WIDTH * line_world + 10, HEIGHT * 0.1 + 45])
    #пропуск кадров и фпс
    screan.blit(render_text(str(update_tik_all)), [WIDTH * line_world + 45, HEIGHT * 0.1 + 145])
    screan.blit(render_text(str(pro)), [WIDTH * line_world + 45, HEIGHT * 0.1 + 245])

    #отрисовка кнопок
    for i in butons.keys():
        screan.blit(butons[i].ret(), butons[i].pos)

#автосейв
def qSave():
    global gamers
    with open(data+'\qdata'+str(group)+'.pickle', 'wb') as f:
        pickle.dump(gamers, f)

# Цикл игры
#всякие нужные переменные
running = True #работа програмы
game_tikl=0 #тики выжевания
game_tik=0 #тики пропуска кадров
game_tik_pro = 0 #пропуск отрисовки
spawns=False #спавн произошел

def speadhak(a):
    for n in range(a):
        for i in piples_reestr.keys():  # очиска реестра
            if piples_reestr[i] != 0 and piples_reestr[i] != -1:
                if not piples_reestr[i] in gamers:
                    piples_reestr[i] = 0
        gamers.update()
        if len(gamers) < gamers_set:
            start_game()
        print(n)

while running:
    if not butons['paus'].onof: update_tik+=1 #тик
    for i in piples_reestr.keys():#очиска реестра
        if piples_reestr[i]!=0 and piples_reestr[i]!=-1:
            if not piples_reestr[i] in gamers:
                piples_reestr[i]=0
    game_tik_pro+=1#тик
    if game_tikl<10000 and not butons['paus'].onof: game_tikl+=1#тик
    if not butons['paus'].onof: game_tik+=1#тик
    if game_tik>1800:
        qSave()
        game_tik=0
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # проверка кнопок
            for i in butons.keys():
                butons[i].on(pygame.mouse.get_pos())
            pos_mous=[pygame.mouse.get_pos()[0]//line_rect, pygame.mouse.get_pos()[1]//line_rect]
            #проверка выбора особи
            see = box_set(pos_mous)
            if see!=0 and see!=-1:
                pipl_see=see
            else:
                pipl_see=None
        #пауза на клавиатуру
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                butons['paus'].onof=not butons['paus'].onof
                butons['paus'].udate()
            if event.key == pygame.K_2:
                speadhak(1000)
            if event.key == pygame.K_1:
                speadhak(2000)
            if event.key == pygame.K_3:
                speadhak(3000)
            if event.key == pygame.K_4:
                speadhak(10000)

    # Обновление
    if not butons['paus'].onof and update_tik>update_tik_all:
        gamers.update()
        update_tik=0
    if len(gamers)<gamers_set and butons['auto_start'].onof and not butons['paus'].onof:
        epoh+=1
        sredl = np.append(sredl, game_tikl/60)
        game_tikl=0
        start_game()

    if game_tik_pro>pro or pro==0:
        draw(screen)
        # После отрисовки всего, переворачиваем экран
        pygame.display.flip()
        game_tik_pro=0

pygame.quit()