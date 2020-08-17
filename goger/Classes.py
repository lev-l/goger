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
	
	def __init__(self, x, y, scin, width, height):
		super().__init__(x, y, scin)
		self.width = width
		self.height = height
	
	def pressed(self, mouse_x, mouse_y):
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
	def __init__(self, x, y, hp, atk, scin, profil, weapon, inventory = [], curent_loc = None):
		#player's inventort
		self.inventory = inventory
		self.standart_scin = scin
		self.profil = profil
		self.weapon = weapon
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
			#mind the previos x and y
			self.prex = self.x
			self.prey = self.y
			# course of player's go
			self.x += 5
		elif e[pygame.K_w]:
			self.scin = self.profil
			#mind the previos x and y
			self.prex = self.x
			self.prey = self.y
			# course of player's go
			self.y -= 5
		elif e[pygame.K_s]:
			self.scin = self.standart_scin
			#mind the previos x and y
			self.prex = self.x
			self.prey = self.y
			# course of player's go
			self.y += 5
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
		if self.x > x and self.y > y and self.x < x + PSize and self.y - 1 < y + PSize:
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
		gog.blit(self.scin, (self.x, self.y))

class Enemy(Movenment):
	"""class what create evil"""

	def __init__(self, x, y, hp, atk, scin, profil):
		#i can not explain it on English
		#переменная которая означает, какой сейчас ход у монстра, и следовательно
		#куда его нужно сдвинуть
		self.hod = 0
		self.profil = profil
		self.standart_scin = scin
		super().__init__(x, y, hp, atk, scin)

	def kill(self, x, y):
		global PSize, SSize

		#logic of killing player
		if x + PSize + 1 > self.x and y + PSize + 1 > self.y and x < self.x + PSize + 1 and y < self.y + PSize + 1 and self.hp > 0:
			return self.atk
		return 0
		#-----------------------

	def move(self):
		#'which "hod" is now?' and move the Enemy
		if self.hp > 0:
			if self.hod == 0:
				self.scin = self.standart_scin
				self.y += 5
			if self.hod == 1:
				self.y += 5
			if self.hod == 2:
				self.y += 5
			if self.hod == 3:
				self.y += 5
			if self.hod == 4:
				self.scin = self.profil
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
		gog.blit(self.scin, (self.x, self.y))

class Key(object):
	"""key fo a door"""

	def __init__(self, title):
		self.title = title
	def put_to_inventory(self, player):
		if self.title not in player.inventory:
			player.inventory.append(self.title)

	def put_to_weapons(self, player, thing):
		pass


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
			return "stop"#"stop" - это то что означает, что игрок должен остановиться(sorry for rusian)
		return "nonstop"

	def empty(self):
		self.invent.pop()	
	
	def repaint(self):
		global PSize, gog
		gog.blit(self.scin, (self.x, self.y))
