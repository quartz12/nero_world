import numpy
import numpy as np
import random
class nero1():
    #сигрмоида
    def sigm(self, a):
        return 1/(1+np.exp(-a))

    #другие активации
    def bilo(self, a, nerons_name):
        if nerons_name=='to_on':
            if a>1: a=1
            if a<1: a=-1
            return a
        elif nerons_name=='to_po_one':
            if a>0: a=1
            if a<0: a=-1
            return a
        elif nerons_name=='sig':
            return 1 / (1 + np.exp(-a))
        elif nerons_name=='of':
            return a

    def __init__(self, nerons, spawn=True, nero_sloi=None, nero_input=None, nero_out=None, bias=None, nero_tex=None):
        self.nerons_set=nerons #количество всех нейронов
        self.inp = nerons[0] #количество нейронов на входе
        self.sloi = nerons[1] #количество нейроновых слоев
        self.nerons = nerons[2] #количество нейронов в слое
        self.output = nerons[3] #количество нейронов на выходе
        if spawn == True: #если заспавнили
            self.nero_sloi = [] #настройко слоев
            self.bias = np.random.rand(self.sloi, self.nerons) #смещение(есть только у скрытых слоев)
            self.nero_tex = [[np.random.choice(['to_on', 'to_po_one', 'sig', 'of']) for i in range(self.nerons)] for a in range(self.sloi)] #разные функции активации(тоже только у скрытых слоев)
            self.nero_input=(np.random.rand(self.inp, self.nerons)-0.5)*2 #веса входа
            self.nero_out=(np.random.rand(self.nerons, self.output)-0.5)*2 #веса выхода
            for i in range(self.sloi):
                self.nero_sloi.append((np.random.rand(self.nerons, self.nerons)-0.5)*2) #веса в слоях
        else: # если само уродилось
            self.nero_tex=nero_tex #
            self.bias=bias
            self.nero_sloi = nero_sloi
            self.nero_input = nero_input
            self.nero_out = nero_out
        self.nerons_all=[] #настройка всех ннейронов вместе
        for i in self.nero_input:
            [self.nerons_all.append(a) for a in i]
        for i in self.nero_sloi:
            for a in i:
                [self.nerons_all.append(n) for n in a]
                if self.nero_tex=='to_on':
                    self.nerons_all.append(0,2)
                else:
                    self.nerons_all.append(0)
        for i in self.nero_out:
            [self.nerons_all.append(a) for a in i]
        self.nerons_all=np.array(self.nerons_all) #итог все нейронные связи вместе для определения разных родов
        self.nerons_out = self.nerons_all.copy()
        self.input=self.nerons_all.copy()

    def stat(self): #вывод статов нейронов
        print("input nero = ")
        print(self.nero_input)
        print("nero sloi:")
        [print(i) for i in self.nero_sloi]
        print("nero out:")
        print(self.nero_out)

    def run(self, input): #работа нейронки
        input = np.array(input) #вход
        self.input=input
        vesa = np.dot(input, self.nero_input) #первый видимый слой
        self.nerons_out=vesa.copy()
        for i in range(self.sloi):
            vesa = np.dot(vesa, self.nero_sloi[i]) #скрытые слои дот
            for a in range(len(vesa)): #функция активации в зависимости от рандома
                vesa[a] = self.bilo(vesa[a], self.nero_tex[i][a])
            vesa = vesa+self.bias[i] #смещение
            self.nerons_out = np.append(self.nerons_out, vesa)
        vesa = np.dot(vesa, self.nero_out) #итоговые веса
        vesa = self.sigm(vesa) #сигмоида
        self.nerons_out = np.append(self.nerons_out, vesa)
        return vesa

    def spawn(self, rand=5, spead=3):#спавн мозга потомка
        if np.random.randint(0, rand) == 0:#случайноя мутация
            #копирование нейронов родителей
            nero_s=self.nero_sloi.copy()
            nero_o=self.nero_out.copy()
            nero_i=self.nero_input.copy()
            #генерирование количество измененый связей
            neroset =np.random.randint(0, spead)
            #генерирование количества измененных смещений
            bias_set=np.random.randint(0, spead-2)
            for i in range(bias_set): #изменение смещений
                self.bias[np.random.randint(0, self.sloi-1)][np.random.randint(0, self.nerons-1)]=np.random.uniform(-0.01, 0.01)
            if 0==np.random.randint(0, rand*5): #изменение 1 активации редко
                self.nero_tex[np.random.randint(0, self.sloi-1)][np.random.randint(0, self.nerons-1)]=np.random.choice(['to_on', 'to_po_one', 'sig', 'of'])
            for i in range(neroset): #изменение весов
                a=np.random.randint(1, self.sloi+2) #выбор слоя
                if a==1:
                    #изменение входного слоя
                    nero_i[np.random.randint(0, self.inp-1)][np.random.randint(0, self.nerons-1)]+=np.random.uniform(-0.01, 0.01)
                elif a<self.sloi+2:
                    #изменение рандомного скрытого
                    nero_s[a-2][np.random.randint(0, self.nerons-1)][np.random.randint(0, self.nerons)-1]+=np.random.uniform(-0.01, 0.01)
                else:
                    #изменение выходного
                    nero_o[np.random.randint(0, self.nerons-1)][np.random.randint(0, self.output)-1]+=np.random.uniform(-0.01, 0.01)
            return nero1(self.nerons_set, spawn=False, nero_sloi=nero_s, nero_out=nero_o, nero_input=nero_i, bias=self.bias, nero_tex=self.nero_tex) #возврат с мутацией
        else:
            return nero1(self.nerons_set, spawn=False, nero_sloi=self.nero_sloi, nero_out=self.nero_out, nero_input=self.nero_input, bias=self.bias, nero_tex=self.nero_tex) #возврат без мутации

class nero2():

    def __init__(self, size, spawn=False, brain=None):
        self.run_id=0
        self.size=size
        if spawn==False:
            self.brain = np.random.randint(0, 20, size)
        else:
            self.brain = brain
        self.nerons_all=np.sum(self.brain)

    def run(self, input):
        ret = 0
        while True:
            if self.run_id>self.size-1: self.run_id=self.run_id-self.size
            ret+=1
            if ret>20:
                return [None]
            do=self.brain[self.run_id]
            if do==1:
                self.run_id+=1
                return [0, 0, 0, 1, 0, 0]
            elif do==2:
                self.run_id+=1
                return [1, 0, 0, 0, 0, 0]
            elif do==3:
                self.run_id+=1
                return [0, 0, 1, 0, 0, 0]
            elif do==4:
                self.run_id+=1
                return [0, 1, 0, 0, 0, 0]
            elif do==5:
                self.run_id+=1
                return [0, 0, 0, 0, 1, 1]
            elif do==6:
                self.run_id+=1
                return [0, 0, 0, 0, 1, 0]
            elif do==7:
                if input[0]==1:
                    self.run_id+=1
                elif input[1]==1:
                    self.run_id+=2
                elif input[2]==1:
                    if input[5]<1:
                        self.run_id+=3
                    else:
                        self.run_id+=4
                continue
            elif do==8:
                self.run_id+=int(input[3]*5)
                continue
            elif do==9:
                self.run_id+=int(input[5]*5)
                continue
            elif do>9:
                if self.run_id>=self.size-1:
                    self.run_id=self.run_id-self.size
                else:
                    self.run_id+=self.brain[self.run_id+1]
                continue
            self.run_id+=1
            return [None]

    def spawn(self, rand=1, a=0):
        aa=self.brain.copy()
        for i in range(rand):
            aa[np.random.randint(self.size)]=np.random.randint(100)
        return nero2(self.size, True, aa)


