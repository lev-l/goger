from CLASES import *
from tkinter import *
import time, threading

#list of beings
#special objects
spear = SPEAR(250, 247, 1, "gray", "spear")
spear1 = SPEAR(250, 247, 2, "black", "forest-spear")
spear2 = SPEAR(250, 247, 3, "white", "hell-spear")
spear3 = SPEAR(250, 247, 4, "green", "sky-spear")
forest_key = KEY("forest_key")
hell_key = KEY("hell_key")
sky_key = KEY("sky_key")
player = PLAYER(245, 245, 1, 0, "yellow", spear, ["spear"])
#forest locations
#first location
enemy = ENEMY(100, 200, 1, 1, "orange")
enemy1 = ENEMY(200, 100, 1, 1, "orange")
enemy2 = ENEMY(300, 400, 1, 1, "orange")
stop = STOP(50, 300, "blue")
stop1 = STOP(400, 50, "blue")
stop2 = STOP(355, 245, "blue")
chest = CHEST(210, 110, spear1, "brown")
#second location
enemy3 = ENEMY(285, 390, 1, 1, "orange")
enemy4 = ENEMY(155, 165, 1, 1, "orange")
enemy5 = ENEMY(380, 110, 1, 1, "orange")
stop3 = STOP(110, 270, "blue")
stop4 = STOP(350, 410, "blue")
stop5 = STOP(215, 280, "blue")
chest1 = CHEST(390, 120, forest_key, "brown")
#third location
enemy6 = ENEMY(450, 250, 1, 1, "orange")
enemy7 = ENEMY(300, 175, 1, 1, "orange")
enemy8 = ENEMY(125, 340, 1, 1, "orange")
stop6 = STOP(305, 205, "blue")
stop7= STOP(45, 410, "blue")
stop8 = STOP(215, 80, "blue")
chest2 = CHEST(310, 185, spear1, "brown")
#-----------------------------------------------
#hell locations
#fourth location
enemy9 = ENEMY(220, 190, 2, 2, "orange")
enemy10 = ENEMY(270, 190, 2, 2, "orange")
enemy11 = ENEMY(320, 190, 2, 2, "orange")
stop9 = STOP(200, 200, "gray")
stop10= STOP(250, 200, "gray")
stop11 = STOP(300, 200, "gray")
chest3 = CHEST(230, 200, spear2, "brown")
#fiveth location
enemy12 = ENEMY(200, 250, 2, 2, "orange")
enemy13 = ENEMY(300, 175, 2, 2, "orange")
enemy14 = ENEMY(150, 340, 2, 2, "orange")
stop12 = STOP(305, 205, "gray")
stop13= STOP(310, 10, "gray")
stop14 = STOP(215, 340, "gray")
chest4 = CHEST(310, 185, spear, "brown")
#sixth location
enemy15 = ENEMY(150, 200, 2, 2, "orange")
enemy16 = ENEMY(285, 100, 2, 2, "orange")
enemy17 = ENEMY(125, 340, 2, 2, "orange")
stop15 = STOP(400, 100, "gray")
stop16= STOP(300, 50, "gray")
stop17 = STOP(200, 100, "gray")
chest5 = CHEST(295, 110, hell_key, "brown")
#----------------------------------------------
#sky location
#seventh location
enemy18 = ENEMY(235, 235, 3, 3, "orange")
enemy19 = ENEMY(210, 235, 3, 3, "orange")
enemy20 = ENEMY(260, 235, 3, 3, "orange")
stop18 = STOP(240, 200, "white")
stop19= STOP(100, 350, "white")
stop20 = STOP(460, 300, "white")
chest6 = CHEST(245, 245, spear3, "brown")
#eighth location
enemy21 = ENEMY(75, 280, 3, 3, "orange")
enemy22 = ENEMY(120, 300, 3, 3, "orange")
enemy23 = ENEMY(270, 100, 3, 3, "orange")
stop21 = STOP(50, 300, "white")
stop22= STOP(150, 350, "white")
stop23 = STOP(300, 100, "white")
chest7 = CHEST(280, 110, spear, "brown")
#nineth location
enemy24 = ENEMY(170, 400, 3, 3, "orange")
enemy25 = ENEMY(260, 400, 3, 3, "orange")
enemy26 = ENEMY(215, 360, 3, 3, "orange")
stop24 = STOP(200, 400, "white")
stop25 = STOP(220, 400, "white")
stop26 = STOP(240, 400, "white")
chest8 = CHEST(225, 370, sky_key, "brown")
#--------------------------------------------------
#-------------------------------------------------------------
#list of locations
#sky
loc1 = ['light blue', player, enemy18, enemy19, enemy20, stop18, stop19, stop20, chest6, player.weapon]
loc2 = ['light blue', player, enemy21, enemy22, enemy23, stop21, stop22, stop23, chest7, player.weapon]
loc3 = ['light blue', player, enemy24, enemy25, enemy26, stop24, stop25, stop26, chest8, player.weapon]
#-------
#forest
loc4 = ['green', player, enemy3, enemy4, enemy5, stop3, stop4, stop5, chest1, player.weapon]
loc5 = ['green', player, enemy, enemy1, enemy2, stop, stop1, stop2, chest, player.weapon]
loc6 = ['green', player, enemy6, enemy7, enemy8, stop6, stop7, stop8, chest2, player.weapon]
#-------
#hell
loc7 = ['red', player, enemy9, enemy10, enemy11, stop9, stop10, stop11, chest3, player.weapon]
loc8 = ['red', player, enemy12, enemy13, enemy14, stop12, stop13, stop14, chest4, player.weapon]
loc9 = ['red', player, enemy15, enemy16, enemy17, stop15, stop16, stop17, chest5, player.weapon]
#-------
#---------------------------------------------
#stop the player on the edge of the location
player_x = lambda: player.x - 5
player_y = lambda: player.y - 5
playerPx = lambda: player.x + 5
playerPy = lambda: player.y + 5
#all locations in one list
locs = [
        [loc1, 'PS', 'PS', 1, 3], [loc2, 0, 'PS', 2, 4], [loc3, 1, 'PS', 'PS', 5],
        [loc4, 'PS', 0, 4, 6], [loc5, 3, 1, 5, 7], [loc6, 4, 2, 'PS', 8],
        [loc7, 'PS', 3, 7, 'PS'], [loc8, 6, 4, 8, 'PS'], [loc9, 7, 5, 'PS', 'PS']
        ]
#[[loc, left, up, rigt, down]]
#-------------------------------
#player's curent loc
player.curent_loc = locs[4]
#-------------------

class ENGINE(object):
    """This class answer for all logic"""

    def __init__(self, locs_map):
        #map of location
        self.locs_map = locs_map
        #variavle "do the game going?"
        self.ran = 0
        #does spear active?
        self.spear_activated = 0

    def repaint(self):
        """repaint all what is need"""
        global gog, player
        gog.delete(ALL)
        #fon of the screen
        fon = gog.create_rectangle(-1, -1, WIDTH + 1, HEIGHT + 1, fill = player.curent_loc[0][0])
        #-------------
        #printing player's inventory
        text = Label(gog, text=", ".join(player.inventory))
        text.place(x=0, y=480)

        #repaint the spear only when it is activated
        if self.spear_activated == 1:
            player.curent_loc[0][9].repaint()

        #repaint player
        player.repaint()
        #repaint enemies only when they are not died
        if player.curent_loc[0][2].hp > 0:
            player.curent_loc[0][2].repaint()
        if player.curent_loc[0][3].hp > 0:
            player.curent_loc[0][3].repaint()
        if player.curent_loc[0][4].hp > 0:
            player.curent_loc[0][4].repaint()
        #repaint obstructions
        player.curent_loc[0][5].repaint()
        player.curent_loc[0][6].repaint()
        player.curent_loc[0][7].repaint()
        player.curent_loc[0][8].repaint()
        gog.pack()

    def take_from_chest(self, e):
        # take something from chest's inventory
        thing = player.curent_loc[0][8].give_inventory(player.x, player.y, e)
        if thing is not None:
            thing.put_to_inventory(player)
            thing.put_to_weapons(player, thing)
            #take the last spear
            player.curent_loc[0][9] = player.weapon
        # --------------------------------------
    def stoping_player(self, e1):
        e = e1.char
        #if the player "врезался"
        #chest's stoping
        stoping = player.curent_loc[0][8].stop(player.x, player.y)
        self.take_from_chest(e)
        player.stoping(stoping)
        #----------
        #standart stopping
        stoping = player.curent_loc[0][7].stop(player.x, player.y)
        player.stoping(stoping)
        stoping = player.curent_loc[0][6].stop(player.x, player.y)
        player.stoping(stoping)
        stoping = player.curent_loc[0][5].stop(player.x, player.y)
        player.stoping(stoping)

    def killing_player(self):
        """enemy has killed player"""
        damage = 0
        #damage of 1-st enemy
        damage += player.curent_loc[0][2].kill(player.x, player.y)
        # damage of 2-nd enemy
        damage += player.curent_loc[0][3].kill(player.x, player.y)
        # damage of 3-rd enemy
        damage += player.curent_loc[0][4].kill(player.x, player.y)
        #player take damage
        player.hp -= damage
        sr = player.die()

        if sr == 0:
            #if player died, announce the text
            text = Label(gog, text='GAME\nOVER')
            text.place(x=230, y=240)

        self.repaint()
        #if player has died, the game will stoped
        self.ran = sr

    def move_enemies(self):
        """move all enemies in this location"""
        player.curent_loc[0][2].move()
        player.curent_loc[0][3].move()
        player.curent_loc[0][4].move()
        #if spear active, try kill enemy
        if self.spear_activated == 1:
            self.kiling_enemy()

    def spear_disactivate(self):
        """hide the spear"""
        self.spear_activated = 0

    def kiling_enemy(self):
        #enemy's die
        damadge = 0
        if self.spear_activated == 1:
            damadge = player.curent_loc[0][9].attack(player.curent_loc[0][2].x, player.curent_loc[0][2].y)
            player.curent_loc[0][2].hp -= damadge
            if damadge > 0 and player.curent_loc[0][2].hp > 0:
                #disactivate spear if you hurted enemy but do not kiled he
                self.spear_disactivate()
            
            damadge = player.curent_loc[0][9].attack(player.curent_loc[0][3].x, player.curent_loc[0][3].y)
            player.curent_loc[0][3].hp -= damadge
            if damadge > 0 and player.curent_loc[0][3].hp > 0:
                self.spear_disactivate()
            
            damadge = player.curent_loc[0][9].attack(player.curent_loc[0][4].x, player.curent_loc[0][4].y)
            player.curent_loc[0][4].hp -= damadge
            if damadge > 0 and player.curent_loc[0][4].hp > 0:
                self.spear_disactivate()

    def key_press(self, e):
        global player
        #when any key press
        #move player
        player.move(e)
        self.locs_map.perehod()
        #if player stoped
        self.stoping_player(e)
        #player atack by spear
        if e.char == "f" or e.char == "F":
            self.spear_activated = 1
            if self.ran == 1:
                #hide the spear
                threading.Timer(1, self.spear_disactivate).start()

        #spear always is next to player
        player.curent_loc[0][9].x = player.x + 5
        player.curent_loc[0][9].y = player.y + 2

    def start(self):
        global player

        self.ran = 1
        # all function what we need to ran
        #move enemies
        self.move_enemies()
        #-----------
        #enemy killing player
        self.killing_player()
        #--------------------
        # if the game going we need ran this function again
        if self.ran == 1:
            threading.Timer(0.1, self.start).start()
        #----------------------------------

    def stop(self):
        #stop the game
        self.ran = 0

class LOCATION(object):
    """location's logic"""
    def __init__(self, locs_list):
        self.locs_list = locs_list

    def go_or_teleport(self, i, end):
        #teleport to next location or stop
        global player
        go = player.curent_loc[i]
        
        if type(go) != int:
                player.stoping("stop")
        else:
            player.curent_loc = self.locs_list[go]
            player.curent_loc[0][9] = player.weapon
            return end

    def perehod(self):
        global player
        perehod = player.loc_end()
        
        #Is the player at the top, bottom, right or left border?
        if perehod == "<x":
            x = self.go_or_teleport(1, 490)
            if x is not None:
                player.x = x
        elif perehod == "x>":
            x = self.go_or_teleport(3, 0)
            if x is not None:
                player.x = x
        elif perehod == "<y":
            y = self.go_or_teleport(2, 490)
            if y is not None:
                player.y = y
        elif perehod == "y>":
            y = self.go_or_teleport(4, 0)
            if y is not None:
                player.y = y

loc = LOCATION(locs)
log = ENGINE(loc)

#ran engine
log.start()
wn.bind('<KeyPress>', log.key_press)

wn.mainloop()
