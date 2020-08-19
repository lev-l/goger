import pygame

# Globals
WIDTH = 500
HEIGHT = 500
PSize = 10
SSize = 20
# --------------
# create window
pygame.init()
gog = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("goger")
# --------------
class Alive(object):
	#parent class for standart objects in this game
	def __init__(self, x, y, scin):
		self.x = x
		self.y = y
		#color of this object
		self.scin = scin

	def repaint(self):
		#this function must rewrite in a douther class
		raise ValueError

class Movenment(Alive):

	def __init__(self, x, y, hp, atk, scin):
		#creature's health
		self.hp = hp
		#creature's atack
		self.atk = atk
		super().__init__(x, y, scin)
		#the previos x and y
		self.prex = self.x
		self.prey = self.y


class Button(Alive):
	"""Class for buttons in menu"""
	
	def __init__(self, x, y, scin, width, height):
		super().__init__(x, y, scin)
		self.width = width
		self.height = height
	
	def pressed(self, mouse_x, mouse_y):
		"""call when we need to know does the button pressed"""
		if self.x + self.width > mouse_x > self.x \
			and self.y + self.height > mouse_y > self.y:
			return True
		return False
	
	def repaint(self):
		global gog
		gog.blit(self.scin, (self.x, self.y))


class Stop(Alive):
	"""this class create obstacle"""

	def stop(self, x, y):
		global PSize, SSize

		#logic of stoping player
		if x + PSize > self.x and y + PSize > self.y and x < self.x + SSize and y < self.y + SSize:
			return "stop"
		return "nonstop"
		#----------------------------------

	def repaint(self):
		global gog
		gog.blit(self.scin, (self.x, self.y))


class Player(Movenment):
	"""class for main being in this game"""
	def __init__(self, x, y, hp, atk, scin, profil, weapon, throw, armour, inventory = [], curent_loc = None):
		#player's inventort
		self.inventory = inventory
		#this scin we use when player go down
		self.standart_scin = scin
		#and this scin we use when player go left, right or up
		self.profil = profil
		#spear
		self.weapon = weapon
		#throwen spear
		self.throw = throw
		self.armour = armour
		#only player know in which location he is
		self.curent_loc = curent_loc
		super().__init__(x, y, hp, atk, scin)

	def move(self, e):
		"""move player on the screen"""
		#Size of player
		global PSize
		#if presed key is 'a', 'w', 's', or 'd', player will go
		if e[pygame.K_a]:
			self.scin = self.profil
			#mind the previos x and y
			self.prex = self.x
			self.prey = self.y
			# course of player's go
			self.x -= 5
		elif e[pygame.K_d]:
			self.scin = self.profil
			self.prex = self.x
			self.prey = self.y
			self.x += 5
		elif e[pygame.K_w]:
			self.scin = self.profil
			self.prex = self.x
			self.prey = self.y
			self.y -= 5
		elif e[pygame.K_s]:
			self.scin = self.standart_scin
			self.prex = self.x
			self.prey = self.y
			self.y += 5
		else:
			pass
	
	def loc_end(self):
		# the player says which edge of the screen he wants to go beyond
		if self.x <= 0:
			return "<x"
		if self.y <= 0:
			return "<y"
		if self.x >= HEIGHT - PSize / 2:
			return "x>"
		if self.y >= WIDTH - PSize / 2:
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
		global gog
		gog.blit(self.scin, (self.x, self.y))

class Spear(Alive):
	"""This a thing what can kill a lot of enemy. You can
	use it with any evil."""

	def __init__(self, x, y, damage, scin, title, active = 0):
		super().__init__(x, y, scin)
		#damadge of the spear
		self.damage = damage
		#this variable answer "does the spear activated?"
		self.active = active
		self.title = title

	def attack(self, x, y):
		global PSize

		#if spear touch enemy, it hurts him!
		if self.x + 5 >= x and self.y >= y and self.x <= x + PSize and self.y - 1 <= y + PSize:
			return self.damage
		return 0

	def put_to_inventory(self, player):
		# append title of spear to player's inventory
		if self.title not in player.inventory and self.damage > player.weapon.damage:
			player.inventory.append(self.title)

	def put_to_weapons(self, player, thing):
		# now player can atack by this spear
		if thing is not player.weapon and self.damage > player.weapon.damage:
			player.weapon = thing
	
	def put_to_armours(self, player, thing):
		# spear isn't armour
		pass
	
	def put_to_throw(self, player, thing):
		# spear isn't throwen spear
		pass
	
	def repaint(self):
		global PSize, gog
		gog.blit(self.scin, (self.x, self.y))

class ThrowenSpear(Spear):
	
	def __init__(self, x, y, damage, scin, title, active = 0, swing = 0):
		self.swing = swing
		super().__init__(x, y, damage, scin, title, active)
	
	def put_to_weapons(self, player, thing):
		# throwen spear isn't spear
		pass
	
	def put_to_throw(self, player, thing):
		# becouse we can have several throwen spear at once
		player.throw.append(thing)
	
	def fly(self, px, py):
		"""call everytime when spear fly foward"""
		if self.swing == 0:
			self.x = px
			self.y = py
			self.y -= 3
			self.swing += 1
		elif self.swing == 1:
			self.y -= 3
			self.swing += 1
		elif self.swing == 2:
			self.y -= 3
			self.swing += 1
		elif self.swing == 3:
			self.y -= 3
			self.swing += 1
		elif self.swing == 4:
			self.y -= 3
			self.swing += 1
		elif self.swing == 5:
			self.y -= 3
			self.swing += 1
		else:
			self.swing = 0
			self.x = px
			self.y = py
			return 0
		return 1
			

class Enemy(Movenment):
	"""class what create evil"""

	def __init__(self, x, y, hp, atk, scin, profil):
		# a variable that means what is the current turn of the monster,
		# and therefore where it needs to be moved
		self.turn = 0
		# enemy can punch player only once
		self.one_punch = False
		self.profil = profil
		self.standart_scin = scin
		super().__init__(x, y, hp, atk, scin)

	def kill(self, x, y):
		global PSize, SSize

		# logic of killing player
		if x + PSize + 1 > self.x and y + PSize + 1 > self.y and x < self.x + PSize + 1 and y < self.y + PSize + 1 and self.hp > 0:
			if self.one_punch == False:
				# if the enemy touches the player, then until he comes off,
				# the enemy will not be able to inflict damage a second time.
				self.one_punch = True
				return self.atk
			else:
				return 0
		
		self.one_punch = False
		return 0
		#-----------------------

	def move(self):
		#'which turn is now?' and move the Enemy
		if self.hp > 0:
			if self.turn == 0:
				self.scin = self.standart_scin
				self.y += 5
			if self.turn == 1:
				self.y += 5
			if self.turn == 2:
				self.y += 5
			if self.turn == 3:
				self.y += 5
			if self.turn == 4:
				self.scin = self.profil
				self.x += 5
			if self.turn == 5:
				self.x += 5
			if self.turn == 6:
				self.x += 5
			if self.turn == 7:
				self.x += 5
			if self.turn == 8:
				self.y -= 5
			if self.turn == 9:
				self.y -= 5
			if self.turn == 10:
				self.y -= 5
			if self.turn == 11:
				self.y -= 5
			if self.turn == 12:
				self.x -= 5
			if self.turn == 13:
				self.x -= 5
			if self.turn == 14:
				self.x -= 5
			if self.turn == 15:
				self.x -= 5
		#--------------------------
		#next turn
		self.turn += 1
		#turn must not be biger then 15
		if self.turn > 15:
			self.turn = 0

	def repaint(self):
		global PSize, gog
		gog.blit(self.scin, (self.x, self.y))

class Key(object):
	"""key fo a door"""
	
	def __init__(self, title):
		self.title = title
	
	def put_to_inventory(self, player):
		if self.title not in player.inventory:
			player.inventory.append(self.title)

	def put_to_weapons(self, player, thing):
		# ker isn't spear
		pass
	
	def put_to_throw(self, player, thing):
		pass
	
	def put_to_armours(self, player, thing):
		pass

class Armour(Key):
	"""player's armour"""
	
	def __init__(self, title, arm):
		self.arm = arm
		super().__init__(title)
	
	def put_to_inventory(self, player):
		if self.title not in player.inventory and self.arm > player.armour.arm:
			player.inventory.append(self.title)
	
	def put_to_throw(self, player, thing):
		pass
	
	def put_to_armours(self, player, thing):
		if thing is not player.armour and self.arm > player.armour.arm:
			player.armour = thing
			
			# visual the armour on the player
			if "leather" in thing.title:
				player.standart_scin = pygame.image.load("docs/player_leather.jpg")
				player.profil = pygame.image.load("docs/player-profil_leather.jpg")
				player.scin = pygame.image.load("docs/player_leather.jpg")
			elif "metal" in thing.title:
				player.standart_scin = pygame.image.load("docs/player_metal.jpg")
				player.profil = pygame.image.load("docs/player-profil_metal.jpg")
				player.scin = pygame.image.load("docs/player_metal.jpg")
			elif "palladium" in thing.title:
				player.standart_scin = pygame.image.load("docs/player_palladium.jpg")
				player.profil = pygame.image.load("docs/player-profil_palladium.jpg")
				player.scin = pygame.image.load("docs/player_palladium.jpg")


class Chest(Stop):
	
	def __init__(self, x, y, invent, scin):
		#what in the chest
		self.invent = invent
		#-------------------
		super().__init__(x, y, scin)
	
	def give_inventory(self, x, y , e):
		global PSize, gog
		
		#if player near from chest, and he press key "e", he will take the inventory of the chest
		if x + (PSize + 1) > self.x and y + (PSize + 1) > self.y and x < self.x + (PSize + 1) and y < self.y + (PSize + 1) and e[pygame.K_e]:
			return self.invent

	def stop(self, x, y):
		global PSize, gog

		if x + PSize > self.x and y + PSize > self.y and x < self.x + PSize and y < self.y + PSize:
			#if player had stoped he take the inventory of this chest
			return "stop"#"stop" - this is what means the player should stop(for refactoring: use 'True' instead 'stop')
		return "nonstop"

	def empty(self):
		# clear the chest
		self.invent = None	
	
	def repaint(self):
		global PSize, gog
		gog.blit(self.scin, (self.x, self.y))
