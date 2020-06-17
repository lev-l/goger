from tkinter import *

# Globals
WIDTH = 500
HEIGHT = 500
PSize = 10
SSize = 20
# --------------
# create window
wn = Tk()
gog = Canvas(wn, width=WIDTH, height=HEIGHT)
wn.title('goger')
# --------------
class ALIVE(object):
    #parent class for standart objects in this game
    def __init__(self, x, y, fill):
        self.x = x
        self.y = y
        #color of this object
        self.fill = fill

    def repaint(self):
        #this function must rewrite in a douther class
        raise ValueError

class MOVENMENT(ALIVE):

    def __init__(self, x, y, hp, atk, fill):
        #creature's health
        self.hp = hp
        #creature's atack
        self.atk = atk
        super().__init__(x, y, fill)
        #the previos x and y
        self.prex = self.x
        self.prey = self.y


class STOP(ALIVE):
    """this class create obstacle"""

    def stop(self, x, y):
        global PSize, SSize

        #logic of stoping player
        if x + PSize > self.x and y + PSize > self.y and x < self.x + SSize and y < self.y + SSize:
            return "stop"
        return "nonstop"
        #----------------------------------

    def repaint(self):
        global SSize, gog
        stop = gog.create_rectangle(self.x, self.y, self.x + SSize, self.y + SSize, fill = self.fill)


class PLAYER(MOVENMENT):
    """class for main being in this game"""
    def __init__(self, x, y, hp, atk, fill, weapon, inventory = [], curent_loc = None):
        #player's inventort
        self.inventory = inventory
        self.weapon = weapon
        self.curent_loc = curent_loc
        super().__init__(x, y, hp, atk, fill)

    def move(self, e):
        """move player on the screen"""
        #Size of player
        global PSize
        #which key is press
        awsd = e.char
        #where player can go
        fblr = {"a": [0, -5], "w": [-5, 0], "s": [5, 0], "d": [0, 5]}
        #if presed key is 'a', 'w', 's', or 'd', player will go
        if awsd in fblr:
            #mind the previos x and y
            self.prex = self.x
            self.prey = self.y
            # course of player's go
            plusXY = fblr[awsd]
            self.x += plusXY[1]
            self.y += plusXY[0]
        else:
            pass

    def loc_end(self):
        # player must not go away from the screen
        if self.x <= 0:
            #self.x += 5
            return "<x"
        if self.y <= 0:
            #self.y += 5
            return "<y"
        if self.x >= HEIGHT - PSize / 2:
            #self.x -= 5
            return "x>"
        if self.y >= WIDTH - PSize / 2:
            #self.y -= 5
            return "y>"

    def stoping(self, stop):
        #logic of stoping player
        if stop == "stop":
            self.x = self.prex
            self.y = self.prey

    def die(self):
        #player dying
        if self.hp <= 0:
            return 0
        else:
            #or no
            return 1

    def repaint(self):
        global PSize, gog
        player = gog.create_rectangle(self.x, self.y, self.x + PSize, self.y + PSize, fill = self.fill)

class SPEAR(ALIVE):
    """This a thing what can kill a lot of enemy. You can
    use it with any evil."""

    def __init__(self, x, y, damage, fill, title, active = 0):
        super().__init__(x, y, fill)
        #damadge of the spear
        self.damage = damage
        #this variable answer "does the spear activated?"
        self.active = active
        self.title = title

    def attack(self, x, y):
        global PSize

        #if spear touch enemy, it hurts him!
        if self.x + 5 > x and self.y + 2 > y and self.x - 6 < x + PSize and self.y - 8 < y + PSize:
            return self.damage
        return 0

    def put_to_inventory(self, player):
        if self.title not in player.inventory and self.damage > player.weapon.damage:
            player.inventory.append(self.title)

    def put_to_weapons(self, player, thing):
        if thing is not player.weapon and self.damage > player.weapon.damage:
            player.weapon = thing

    def repaint(self):
        global PSize, gog
        gog.create_rectangle(self.x, self.y, self.x - 5, self.y - 10, fill = self.fill)

class ENEMY(MOVENMENT):
    """class what create evil"""

    def __init__(self, x, y, hp, atk, fill):
        #i can not explain it on English
        #переменная которая означает, какой сейчас ход у монстра, и следовательно
        #куда его нужно сдвинуть
        self.hod = 0
        super().__init__(x, y, hp, atk, fill)

    def kill(self, x, y):
        global PSize, SSize

        #logic of killing player
        if x + PSize + 1 > self.x and y + PSize + 1 > self.y and x < self.x + PSize + 1 and y < self.y + PSize + 1 and self.hp > 0:
            return self.atk
        return 0
        #-----------------------

    def move(self):
        #'which "hod" is now?' and move the enemy
        if self.hp > 0:
            if self.hod == 0:
                self.y += 5
            if self.hod == 1:
                self.y += 5
            if self.hod == 2:
                self.y += 5
            if self.hod == 3:
                self.y += 5
            if self.hod == 4:
                self.x += 5
            if self.hod == 5:
                self.x += 5
            if self.hod == 6:
                self.x += 5
            if self.hod == 7:
                self.x += 5
            if self.hod == 8:
                self.y -= 5
            if self.hod == 9:
                self.y -= 5
            if self.hod == 10:
                self.y -= 5
            if self.hod == 11:
                self.y -= 5
            if self.hod == 12:
                self.x -= 5
            if self.hod == 13:
                self.x -= 5
            if self.hod == 14:
                self.x -= 5
            if self.hod == 15:
                self.x -= 5
        #--------------------------
        #next "hod"
        self.hod += 1
        #hod must not be biger then 15
        if self.hod > 15:
            self.hod = 0

    def repaint(self):
        global PSize, gog
        enemy = gog.create_rectangle(self.x, self.y, self.x + PSize, self.y + PSize, fill = self.fill)

class KEY(object):
    """key fo a door"""

    def __init__(self, title):
        self.title = title
    def put_to_inventory(self, player):
        if self.title not in player.inventory:
            player.inventory.append(self.title)

    def put_to_weapons(self, player, thing):
        pass

class CHEST(STOP):

    def __init__(self, x, y, invent, fill):
        #what in the chest
        self.invent = invent
        #-------------------
        super().__init__(x, y, fill)

    def give_inventory(self, x, y , e):
        global PSize, gog

        #if player near from chest, and he press key "e", he will take the inventory of the chest
        if x + (PSize + 1) > self.x and y + (PSize + 1) > self.y and x < self.x + (PSize + 1) and y < self.y + (PSize + 1) and e == "e":
            return self.invent

    def stop(self, x, y):
        global PSize, gog

        if x + PSize > self.x and y + PSize > self.y and x < self.x + PSize and y < self.y + PSize:
            #if player had stoped he take the inventory of this chest
            return "stop"#"stop" - это то что означает, что игрок должен остановиться(sorry for rusian)
        return "nonstop"

    def empty(self):
        self.invent.pop()

    def repaint(self):
        global PSize, gog
        chest = gog.create_rectangle(self.x, self.y, self.x + PSize, self.y + PSize, fill = self.fill)
