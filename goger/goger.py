from Classes import *
import pygame
import threading


#menu
button_s = Button(150, 150, pygame.image.load("docs/button_start.jpg"), 200, 50)
button_e = Button(150, 210, pygame.image.load("docs/button_exit.jpg"), 200, 50)

button_1 = Button(150, 140, pygame.image.load("docs/easy.jpg"), 200, 50)
button_2 = Button(150, 200, pygame.image.load("docs/normal.jpg"), 200, 50)
button_3 = Button(150, 260, pygame.image.load("docs/complex.jpg"), 200, 50)
button_4 = Button(150, 320, pygame.image.load("docs/hard.jpg"), 200, 50)

menu = {'fon': pygame.image.load("docs/forest-back.jpg"), 'start': button_s, 'exit': button_e,
		'easy': button_1, 'normal': button_2, 'complex': button_3, 'hard': button_4}
#-----
#texts
fon = pygame.font.Font(None, 20)
text_inventory = fon.render('', 0, (0, 0, 0))
game_over = fon.render('GAME OVER!', 0, (255, 0, 0))
players_hp = fon.render('', 0, (100, 0, 0))
#-----


class ENGINE(object):
	"""This class answer for all logic"""
	
	def __init__(self, locs_map, player):
		self.locs_map = locs_map
		self.player = player
		#variavle "do the game going?"
		self.ran = 0
		self.spear_activated = 0
		self.throwed = 0
	
	def repaint(self):
		"""repaint all what is need"""
		global gog, text_inventory, fon
		#fon of the screen
		gog.blit(self.player.curent_loc[0][0], (0, 0))
		#-------------
		text = ""
		i = 0
		for el in self.player.inventory:
			i += 1
			if el == 'throwen spear':
				text = text + el + 'x' + str(len(self.player.throw)) + ', '
			else:
				text = text + el + ', '
		
		if len(text) > 83:
			text1 = text[83:]
			text = text[:83]
			text_inventory = fon.render(text1, 0, (0, 0, 0))
			gog.blit(text_inventory, (0, 480))
		
		text_inventory = fon.render(text, 0, (0, 0, 0))
		gog.blit(text_inventory, (0, 460))
		players_hp = fon.render('hp:' + str(self.player.hp), 0, (100, 0, 0))
		gog.blit(players_hp, (0, 0))
		
		#repaint the spear only when it is activated
		if self.spear_activated == 1:
			self.player.curent_loc[0][9].repaint()
		if self.throwed == 1:
			self.player.throw[len(self.player.throw) - 1].repaint()
		
		#repaint player
		self.player.repaint()
		#repaint enemies only when they are not died
		if self.player.curent_loc[0][2].hp > 0:
			self.player.curent_loc[0][2].repaint()
		if self.player.curent_loc[0][3].hp > 0:
			self.player.curent_loc[0][3].repaint()
		if self.player.curent_loc[0][4].hp > 0:
			self.player.curent_loc[0][4].repaint()
		#repaint obstructions
		self.player.curent_loc[0][5].repaint()
		self.player.curent_loc[0][6].repaint()
		self.player.curent_loc[0][7].repaint()
		self.player.curent_loc[0][8].repaint()
		pygame.display.update()
	
	def take_from_chest(self, e):
		# take something from chest's inventory
		thing = self.player.curent_loc[0][8].give_inventory(self.player.x, self.player.y, e)
		if thing is not None:
			thing.put_to_inventory(self.player)
			thing.put_to_weapons(self.player, thing)
			thing.put_to_armours(self.player, thing)
			thing.put_to_throw(self.player, thing)
			self.player.curent_loc[0][9] = self.player.weapon
			# clear chest
			self.player.curent_loc[0][8].empty()
		# --------------------------------------
	def stoping_player(self, e):
		#if the player must be stoped
		#chest's stoping
		stoping = self.player.curent_loc[0][8].stop(self.player.x, self.player.y)
		self.take_from_chest(e)
		self.player.stoping(stoping)
		#----------
		#standart stopping
		stoping = self.player.curent_loc[0][7].stop(self.player.x, self.player.y)
		self.player.stoping(stoping)
		stoping = self.player.curent_loc[0][6].stop(self.player.x, self.player.y)
		self.player.stoping(stoping)
		stoping = self.player.curent_loc[0][5].stop(self.player.x, self.player.y)
		self.player.stoping(stoping)
	
	def killing_player(self):
		"""enemy has killed player"""
		global gog, game_over
		damage = 0
		#damage of 1-st enemy
		damage += self.player.curent_loc[0][2].kill(self.player.x, self.player.y)
		# damage of 2-nd enemy
		damage += self.player.curent_loc[0][3].kill(self.player.x, self.player.y)
		# damage of 3-rd enemy
		damage += self.player.curent_loc[0][4].kill(self.player.x, self.player.y)
		#player take damage
		
		if damage - self.player.armour.arm <= 0 and damage != 0:
			damage = 1
		elif damage - self.player.armour.arm > 0 and damage != 0:
			damage -= self.player.armour.arm
		else:
			damage = 0
		
		self.player.hp -= damage
		sr = self.player.die()
		
		if sr == 0:
			#if self.player died, announce the text
			gog.blit(game_over, (230, 240))
		
		self.repaint()
		#if player has died, the game will stoped
		self.ran = sr
	
	def move_enemies(self):
		"""move all enemies in this location"""
		self.player.curent_loc[0][2].move()
		self.player.curent_loc[0][3].move()
		self.player.curent_loc[0][4].move()
		if self.spear_activated == 1 or self.throwed == 1:
			self.kiling_enemy()
	
	def spear_disactivate(self):
		"""hide the spear"""
		self.spear_activated = 0
	
	def kiling_enemy(self):
		#enemy's die
		damadge = 0
		
		if self.spear_activated == 1:
			damadge = self.player.curent_loc[0][9].attack(self.player.curent_loc[0][2].x, self.player.curent_loc[0][2].y)
			self.player.curent_loc[0][2].hp -= damadge
			
			if damadge > 0 and self.player.curent_loc[0][2].hp > 0:
				self.spear_disactivate()
				self.player.curent_loc[0][2].scin = pygame.image.load("docs/monster_hurted.jpg")
			
			damadge = self.player.curent_loc[0][9].attack(self.player.curent_loc[0][3].x, self.player.curent_loc[0][3].y)
			self.player.curent_loc[0][3].hp -= damadge
			
			if damadge > 0 and self.player.curent_loc[0][3].hp > 0:
				self.spear_disactivate()
				self.player.curent_loc[0][3].scin = pygame.image.load("docs/monster_hurted.jpg")
			
			damadge = self.player.curent_loc[0][9].attack(self.player.curent_loc[0][4].x, self.player.curent_loc[0][4].y)
			self.player.curent_loc[0][4].hp -= damadge
			
			if damadge > 0 and self.player.curent_loc[0][4].hp > 0:
				self.spear_disactivate()
				self.player.curent_loc[0][4].scin = pygame.image.load("docs/monster_hurted.jpg")
		
		if self.throwed == 1:
			
			damadge = self.player.throw[len(self.player.throw) - 1].attack(self.player.curent_loc[0][2].x, self.player.curent_loc[0][2].y)
			self.player.curent_loc[0][2].hp -= damadge
			if damadge > 0 and self.player.curent_loc[0][2].hp > 0:
				self.player.curent_loc[0][2].scin = pygame.image.load("docs/monster_hurted.jpg")
			
			damadge = self.player.throw[len(self.player.throw) - 1].attack(self.player.curent_loc[0][3].x, self.player.curent_loc[0][3].y)
			self.player.curent_loc[0][3].hp -= damadge
			if damadge > 0 and self.player.curent_loc[0][3].hp > 0:
				self.player.curent_loc[0][3].scin = pygame.image.load("docs/monster_hurted.jpg")
			
			damadge = self.player.throw[len(self.player.throw) - 1].attack(self.player.curent_loc[0][4].x, self.player.curent_loc[0][4].y)
			self.player.curent_loc[0][4].hp -= damadge
			if damadge > 0 and self.player.curent_loc[0][4].hp > 0:
				self.player.curent_loc[0][4].scin = pygame.image.load("docs/monster_hurted.jpg")
	
	def key_press(self, e):
		#when any key press
		#move player
		self.player.move(e)
		self.locs_map.perehod()
		#if player stoped
		self.stoping_player(e)
		#player atack by spear
		if e[pygame.K_f]:
			self.spear_activated = 1
			if self.ran == 1:
				#hide the spear
				threading.Timer(1, self.spear_disactivate).start()
		elif e[pygame.K_t] and self.player.throw:
			self.throwed = 1
			self.player.throw[len(self.player.throw) - 1].x = self.player.x + 5
			self.player.throw[len(self.player.throw) - 1].y = self.player.y - 8
		
		#spear always is next to player
		self.player.curent_loc[0][9].x = self.player.x + 5
		self.player.curent_loc[0][9].y = self.player.y - 8
	
	def start(self):
		
		self.ran = 1
		# all function what we need to ran
		#move enemies
		self.move_enemies()
		#-----------
		#enemy killing player
		self.killing_player()
		#--------------------
	
	def stop(self):
		#stop the game
		self.ran = 0


class LOCATION(object):
	
	def __init__(self, locs_list, player):
		self.player = player
		self.locs_list = locs_list
	
	def go_or_teleport(self, xy, i, end):
		go = self.player.curent_loc[i]
		if type(go) != int:
			if xy == "x":
				self.player.x = go()
			if xy == "y":
				self.player.y = go()
		else:
			self.player.curent_loc = self.locs_list[go]
			self.player.curent_loc[0][9] = self.player.weapon
			return end
	
	def perehod(self):
		perehod = self.player.loc_end()
		if perehod == "<x":
			x = self.go_or_teleport("x", 1, 490)
			if x is not None:
				self.player.x = x
		elif perehod == "x>":
			x = self.go_or_teleport("x", 3, 0)
			if x is not None:
				self.player.x = x
		elif perehod == "<y":
			y = self.go_or_teleport("y", 2, 490)
			if y is not None:
				self.player.y = y
		elif perehod == "y>":
			y = self.go_or_teleport("y", 4, 0)
			if y is not None:
				self.player.y = y


class Game(object):
	
	def game(self, player_hp):
		#list of beings
		#special objects
		spear = Spear(250, 237, 1, pygame.image.load("docs/spear.png"), "spear")
		spear1 = Spear(250, 237, 2, pygame.image.load("docs/forest-spear.png"), "forest-spear")
		spear2 = Spear(250, 237, 3, pygame.image.load("docs/hell-spear.png"), "hell-spear")
		spear3 = Spear(250, 237, 4, pygame.image.load("docs/sky-spear.png"), "sky-spear")
		
		throw = ThrowenSpear(250, 237, 4, pygame.image.load("docs/spear.png"), "throwen spear")
		
		armour = Armour('leather armour', 1)
		armour1 = Armour('metal armour', 2)
		armour2 = Armour('palladium armour', 3)
		
		forest_key = Key("forest_key")
		hell_key = Key("hell_key")
		sky_key = Key("sky_key")
		
		player = Player(245, 245, player_hp, 0, pygame.image.load("docs/player.jpg"),
						pygame.image.load("docs/player-profil.jpg"), spear, [], Armour('none', 0), ["spear"])
		#forest locations
		#first location
		enemy = Enemy(100, 200, 1, 1, pygame.image.load("docs/monster.jpg"), pygame.image.load("docs/monster-profil.jpg"))
		enemy1 = Enemy(200, 100, 1, 1, pygame.image.load("docs/monster.jpg"), pygame.image.load("docs/monster-profil.jpg"))
		enemy2 = Enemy(300, 400, 1, 1, pygame.image.load("docs/monster.jpg"), pygame.image.load("docs/monster-profil.jpg"))
		stop = Stop(50, 300, pygame.image.load("docs/lake.png"))
		stop1 = Stop(400, 50, pygame.image.load("docs/lake.png"))
		stop2 = Stop(355, 245, pygame.image.load("docs/lake.png"))
		chest = Chest(210, 110, spear1, pygame.image.load("docs/chest.jpg"))
		#second location
		enemy3 = Enemy(285, 390, 1, 1, pygame.image.load("docs/monster.jpg"), pygame.image.load("docs/monster-profil.jpg"))
		enemy4 = Enemy(155, 165, 1, 1, pygame.image.load("docs/monster.jpg"), pygame.image.load("docs/monster-profil.jpg"))
		enemy5 = Enemy(380, 110, 1, 1, pygame.image.load("docs/monster.jpg"), pygame.image.load("docs/monster-profil.jpg"))
		stop3 = Stop(110, 270, pygame.image.load("docs/lake.png"))
		stop4 = Stop(350, 410, pygame.image.load("docs/lake.png"))
		stop5 = Stop(215, 280, pygame.image.load("docs/lake.png"))
		chest1 = Chest(390, 120, forest_key, pygame.image.load("docs/chest.jpg"))
		#third location
		enemy6 = Enemy(450, 250, 1, 1, pygame.image.load("docs/monster.jpg"), pygame.image.load("docs/monster-profil.jpg"))
		enemy7 = Enemy(300, 175, 1, 1, pygame.image.load("docs/monster.jpg"), pygame.image.load("docs/monster-profil.jpg"))
		enemy8 = Enemy(125, 340, 1, 1, pygame.image.load("docs/monster.jpg"), pygame.image.load("docs/monster-profil.jpg"))
		stop6 = Stop(310, 205, pygame.image.load("docs/lake.png"))
		stop7= Stop(45, 410, pygame.image.load("docs/lake.png"))
		stop8 = Stop(215, 80, pygame.image.load("docs/lake.png"))
		if player_hp > 1:
			chest2 = Chest(310, 185, armour, pygame.image.load("docs/chest.jpg"))
		else:
			chest2 = Chest(310, 185, throw, pygame.image.load("docs/chest.jpg"))
		#-----------------------------------------------
		#hell locations
		#fourth location
		enemy9 = Enemy(220, 190, 2, 2, pygame.image.load("docs/monster.jpg"), pygame.image.load("docs/monster-profil.jpg"))
		enemy10 = Enemy(270, 190, 2, 2, pygame.image.load("docs/monster.jpg"), pygame.image.load("docs/monster-profil.jpg"))
		enemy11 = Enemy(320, 190, 2, 2, pygame.image.load("docs/monster.jpg"), pygame.image.load("docs/monster-profil.jpg"))
		stop9 = Stop(200, 200, pygame.image.load("docs/rock.png"))
		stop10= Stop(250, 200, pygame.image.load("docs/rock.png"))
		stop11 = Stop(300, 200, pygame.image.load("docs/rock.png"))
		chest3 = Chest(230, 200, spear2, pygame.image.load("docs/chest.jpg"))
		#fiveth location
		enemy12 = Enemy(200, 250, 2, 2, pygame.image.load("docs/monster.jpg"), pygame.image.load("docs/monster-profil.jpg"))
		enemy13 = Enemy(300, 175, 2, 2, pygame.image.load("docs/monster.jpg"), pygame.image.load("docs/monster-profil.jpg"))
		enemy14 = Enemy(150, 340, 2, 2, pygame.image.load("docs/monster.jpg"), pygame.image.load("docs/monster-profil.jpg"))
		stop12 = Stop(310, 205, pygame.image.load("docs/rock.png"))
		stop13= Stop(310, 10, pygame.image.load("docs/rock.png"))
		stop14 = Stop(215, 340, pygame.image.load("docs/rock.png"))
		if player_hp > 1:
			chest4 = Chest(310, 185, armour1, pygame.image.load("docs/chest.jpg"))
		else:
			chest4 = Chest(310, 185, throw, pygame.image.load("docs/chest.jpg"))
		#sixth location
		enemy15 = Enemy(150, 200, 2, 2, pygame.image.load("docs/monster.jpg"), pygame.image.load("docs/monster-profil.jpg"))
		enemy16 = Enemy(285, 100, 2, 2, pygame.image.load("docs/monster.jpg"), pygame.image.load("docs/monster-profil.jpg"))
		enemy17 = Enemy(125, 340, 2, 2, pygame.image.load("docs/monster.jpg"), pygame.image.load("docs/monster-profil.jpg"))
		stop15 = Stop(400, 100, pygame.image.load("docs/rock.png"))
		stop16= Stop(300, 50, pygame.image.load("docs/rock.png"))
		stop17 = Stop(200, 100, pygame.image.load("docs/rock.png"))
		chest5 = Chest(295, 110, hell_key, pygame.image.load("docs/chest.jpg"))
		#----------------------------------------------
		#sky location
		#seventh location
		enemy18 = Enemy(235, 235, 3, 3, pygame.image.load("docs/monster.jpg"), pygame.image.load("docs/monster-profil.jpg"))
		enemy19 = Enemy(210, 235, 3, 3, pygame.image.load("docs/monster.jpg"), pygame.image.load("docs/monster-profil.jpg"))
		enemy20 = Enemy(260, 235, 3, 3, pygame.image.load("docs/monster.jpg"), pygame.image.load("docs/monster-profil.jpg"))
		stop18 = Stop(240, 200, pygame.image.load("docs/sky_lake.png"))
		stop19= Stop(100, 350, pygame.image.load("docs/sky_lake.png"))
		stop20 = Stop(460, 300, pygame.image.load("docs/sky_lake.png"))
		chest6 = Chest(245, 245, spear3, pygame.image.load("docs/chest.jpg"))
		#eighth location
		enemy21 = Enemy(75, 280, 3, 3, pygame.image.load("docs/monster.jpg"), pygame.image.load("docs/monster-profil.jpg"))
		enemy22 = Enemy(120, 300, 3, 3, pygame.image.load("docs/monster.jpg"), pygame.image.load("docs/monster-profil.jpg"))
		enemy23 = Enemy(270, 100, 3, 3, pygame.image.load("docs/monster.jpg"), pygame.image.load("docs/monster-profil.jpg"))
		stop21 = Stop(50, 300, pygame.image.load("docs/sky_lake.png"))
		stop22= Stop(150, 350, pygame.image.load("docs/sky_lake.png"))
		stop23 = Stop(300, 100, pygame.image.load("docs/sky_lake.png"))
		if player_hp > 1:
			chest7 = Chest(280, 110, armour2, pygame.image.load("docs/chest.jpg"))
		else:
			chest7 = Chest(280, 110, throw, pygame.image.load("docs/chest.jpg"))
		#nineth location
		enemy24 = Enemy(170, 400, 3, 3, pygame.image.load("docs/monster.jpg"), pygame.image.load("docs/monster-profil.jpg"))
		enemy25 = Enemy(260, 400, 3, 3, pygame.image.load("docs/monster.jpg"), pygame.image.load("docs/monster-profil.jpg"))
		enemy26 = Enemy(215, 360, 3, 3, pygame.image.load("docs/monster.jpg"), pygame.image.load("docs/monster-profil.jpg"))
		stop24 = Stop(200, 400, pygame.image.load("docs/sky_lake.png"))
		stop25 = Stop(220, 400, pygame.image.load("docs/sky_lake.png"))
		stop26 = Stop(240, 400, pygame.image.load("docs/sky_lake.png"))
		chest8 = Chest(225, 370, sky_key, pygame.image.load("docs/chest.jpg"))
		#--------------------------------------------------
		#-------------------------------------------------------------
		#list of locations
		#forest
		#sky
		loc1 = [pygame.image.load("docs/sky-back.jpg"), player, enemy18, enemy19, enemy20, stop18, stop19, stop20, chest6, player.weapon]
		loc2 = [pygame.image.load("docs/sky-back.jpg"), player, enemy21, enemy22, enemy23, stop21, stop22, stop23, chest7, player.weapon]
		loc3 = [pygame.image.load("docs/sky-back.jpg"), player, enemy24, enemy25, enemy26, stop24, stop25, stop26, chest8, player.weapon]
		#-------
		loc4 = [pygame.image.load("docs/forest-back.jpg"), player, enemy3, enemy4, enemy5, stop3, stop4, stop5, chest1, player.weapon]
		loc5 = [pygame.image.load("docs/forest-back.jpg"), player, enemy, enemy1, enemy2, stop, stop1, stop2, chest, player.weapon]
		loc6 = [pygame.image.load("docs/forest-back.jpg"), player, enemy6, enemy7, enemy8, stop6, stop7, stop8, chest2, player.weapon]
		#-------
		#hell
		loc7 = [pygame.image.load("docs/hell-back.jpg"), player, enemy9, enemy10, enemy11, stop9, stop10, stop11, chest3, player.weapon]
		loc8 = [pygame.image.load("docs/hell-back.jpg"), player, enemy12, enemy13, enemy14, stop12, stop13, stop14, chest4, player.weapon]
		loc9 = [pygame.image.load("docs/hell-back.jpg"), player, enemy15, enemy16, enemy17, stop15, stop16, stop17, chest5, player.weapon]
		#-------
		#---------------------------------------------
		#all locations in ane list
		player_x = lambda: player.x - 5
		player_y = lambda: player.y - 5
		playerPx = lambda: player.x + 5
		playerPy = lambda: player.y + 5
		locs = [
				[loc1, playerPx, playerPy, 1, 3], [loc2, 0, playerPy, 2, 4], [loc3, 1, playerPy, player_x, 5],
				[loc4, playerPx, 0, 4, 6], [loc5, 3, 1, 5, 7], [loc6, 4, 2, player_x, 8],
				[loc7, playerPx, 3, 7, player_y], [loc8, 6, 4, 8, player_y], [loc9, 7, 5, player_x, player_y]
				]
		#[[loc, left, up, rigt, down]]
		#-------------------------------
		#player's curent loc
		player.curent_loc = locs[4]
		#-------------------
		loc = LOCATION(locs, player)
		log = ENGINE(loc, player)
		log.ran = 1
		
		clock = pygame.time.Clock()
		#ran engine
		while log.ran == 1:
			clock.tick(20)
			log.start()
			
			if log.throwed == 1:
				status = player.throw[len(player.throw) - 1].fly(player.x + 5, player.y - 8)
				log.throwed = status
				if not log.throwed:
					player.throw.pop()
			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit(0)
			
			keys = pygame.key.get_pressed()
			log.key_press(keys)
			log.repaint()
		
		if player.hp <= 0:
			i = 0
			while i < 2:
				pygame.time.delay(1000)
				i += 1
				gog.blit(game_over, (230, 240))
				pygame.display.update()



def repaint_menu(start):
	global menu, gog, game_obj, started
	
	gog.blit(menu['fon'], (0, 0))
	
	if start:
		gog.blit(menu['easy'].scin, (menu['easy'].x, menu['easy'].y))
		gog.blit(menu['normal'].scin, (menu['normal'].x, menu['normal'].y))
		gog.blit(menu['complex'].scin, (menu['complex'].x, menu['complex'].y))
		gog.blit(menu['hard'].scin, (menu['hard'].x, menu['hard'].y))
		
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				if menu['easy'].pressed(event.pos[0], event.pos[1]):
					started = 0
					game_obj.game(10)
				elif menu['normal'].pressed(event.pos[0], event.pos[1]):
					started = 0
					game_obj.game(6)
				elif menu['complex'].pressed(event.pos[0], event.pos[1]):
					started = 0
					game_obj.game(3)
				elif menu['hard'].pressed(event.pos[0], event.pos[1]):
					started = 0
					game_obj.game(1)
	else:
		gog.blit(menu['start'].scin, (menu['start'].x, menu['start'].y))
		gog.blit(menu['exit'].scin, (menu['exit'].x, menu['exit'].y))

clock = pygame.time.Clock()
game_obj = Game()

started = False

#open menu
while True:
	clock.tick(20)
	repaint_menu(started)
	pygame.display.update()
	
	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONDOWN:
			if menu['start'].pressed(event.pos[0], event.pos[1]):
				started = True
			elif menu['exit'].pressed(event.pos[0], event.pos[1]):
				exit(0)
