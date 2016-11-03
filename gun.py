from random import randrange as rnd, choice
from tkinter import *
import math
 
#print (dir(math))
 
import time
root = Tk()
fr = Frame(root)
root.geometry('800x600')
canv = Canvas(root, bg = 'white')
canv.pack(fill=BOTH,expand=1)


class ball():
    """ Класс ball описывает мяч. """

    def __init__(self,x=40,y=450):
        """ Конструктор класса ball
        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(['blue','green','red','brown'])
        self.id = canv.create_oval(self.x-self.r, self.y-self.r, self.x+self.r, self.y+self.r, fill=self.color)
        self.live = 30

    def set_coords(self):
        canv.coords(self.id, self.x-self.r, self.y-self.r, self.x+self.r, self.y+self.r)

    def move(self):
        """ Метод move описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения 
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
            и стен по краям окна (размер окна 800х600).
        """
        #FIXME #DONE
        g = 2
        self.vy -= g
        self.x += self.vx
        self.y -= (self.vy)
        self.set_coords()
        # def f_sopr(x,y,r):
        #     k = 2
        #     f = k
        #     return f

        b1 = 0.3
        b2 = 0.1
        k = 2
        if self.x + self.r >= 800 or self.x-self.r <=0:
            self.vx -= self.vx*b1
            self.vy -= self.vy*b2
        if self.y + self.r >=600 or self.y - self.r <=0:
             self.vx -= self.vx*b2
             self.vy -= self.vy*b1
        if self.x + self.r >= 800:
            self.vx += k*(800-self.x-self.r)
        if self.x - self.r <= 0:
            self.vx += k*(0-self.x+self.r)
        if self.y + self.r >= 600:
            self.vy -= k*(600-self.y-self.r)
        if self.y - self.r <= 0:
            self.vy -= k*(0-self.y+self.r)

    def hittest(self,ob):
        """ Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте ob.

        Args:
            ob: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        #FIXME #DONE
        X = self.x
        Y= self.y
        R  = self.r
        x = ob.x
        y=ob.y
        r  = ob.r
        return ((X-x)**2+(Y-y)**2)**0.5 <= (R+r)


class gun():
    """ Класс gun описывает пушку. """
    def __init__(self):

        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.id = canv.create_line(20,450,50,420,width=7) # FIXME: don't know how to set it...#Done
         
    def fire2_start(self,event):
        self.f2_on = 1
 
    def fire2_end(self,event):
        """ Выстрел мячом происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = ball()
        new_ball.r += 5
        self.an = math.atan((event.y-new_ball.y)/(event.x-new_ball.x))
        new_ball.vx = self.f2_power*math.cos(self.an)
        new_ball.vy = -self.f2_power*math.sin(self.an)
        print(new_ball.vx, new_ball.vy)
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 10
 
 
    def targetting (self,event=0):
        """ Прицеливание. Зависит от положения мыши.
        """
        if event:
            self.an = math.atan((event.y-450)/(event.x-20))    
        if self.f2_on:
            canv.itemconfig(self.id,fill = 'orange')
        else:
            canv.itemconfig(self.id,fill = 'black')
        canv.coords(self.id, 20, 450, 20 + max(self.f2_power, 20) * math.cos(self.an), 450 + max(self.f2_power, 20) * math.sin(self.an))
         

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            canv.itemconfig(self.id,fill = 'orange')
        else:
            canv.itemconfig(self.id,fill = 'black')
        
class target():
    """ Класс target описывает цель. """
    def __init__(self):
        self.points = 0
        self.live = 1
    # FIXME: don't work!!! How to call this functions when object is created? #DONE
        self.id = canv.create_oval(0,0,0,0)
        self.id_points = canv.create_text(30,30,text = self.points,font = '28')
        self.new_target()
    def move(self):
        """ Метод move описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
            и стен по краям окна (размер окна 800х600).
        """
        #FIXME #DONE

        self.x += self.vx
        self.y -= (self.vy)
        self.draw()


        if self.x + self.r >= 800 or self.x-self.r <=0:
            self.vx = -self.vx
        if self.y + self.r >=600 or self.y - self.r <=0:
            self.vy = -self.vy
    def draw(self):
        color = self.color = 'green'
        canv.coords(self.id, self.x-self.r,self.y-self.r,self.x+self.r,self.y+self.r)
        canv.itemconfig(self.id, fill = color)
    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = rnd(600,780)
        y = self.y = rnd(300,550)
        r = self.r = rnd(2,50)
        vx = self.vx = rnd(1,5)
        vy = self.vy = rnd(1,5)
        self.draw()
         
    def hit(self,points = 1):
        """ Попадание шарика в цель. """

        canv.coords(self.id,-10,-10,-10,-10)
        self.points += points
        canv.itemconfig(self.id_points, text = self.points)



screen1 = canv.create_text(400,300, text = '',font = '28')
g1 = gun()
bullet = 0
balls = []



def new_game(event=''):
    global gun, screen1, balls, bullet
    targets = [target(), target()]
    bullet = 0
    balls = []
    canv.bind('<Button-1>', g1.fire2_start)
    canv.bind('<ButtonRelease-1>', g1.fire2_end)
    canv.bind('<Motion>', g1.targetting)
 
    z = 0.03
    n=2
    while n>0 or balls:
        for l in targets:
            if l.live:
                l.move()

        for b in balls:
            b.move()

            for x in targets:

                if (b.hittest(x) and x.live):
                    print('True')
                    x.live = 0
                    x.hit()
                    n-=1
                    if n == 0:
                        canv.bind('<Button-1>', '')
                        canv.bind('<ButtonRelease-1>', '')
                        canv.itemconfig(screen1, text = 'Вы уничтожили цели за ' + str(bullet) + ' выстрелов')
                        for b in balls:
                            canv.delete(b.id)
                        balls.clear()

        canv.update()
        time.sleep(0.03)
        g1.targetting()
        g1.power_up()
    time.sleep(1.5)
    canv.itemconfig(screen1, text = '')
    canv.delete(gun)
    root.after(750,new_game)

new_game()   
 
mainloop()

