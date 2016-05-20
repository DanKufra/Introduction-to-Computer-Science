#############################################################
# FILE : asteroidMain.py
# WRITER : Dan Kufra , dan_kufra ,
# EXERCISE : intro2cs ex8
# DESCRIPTION:
# This is a version of the classic game "Asteroids". The goal is to control
# the spaceship and destroy the asteroids.
#############################################################
from torpedo import *
from asteroid import *
from spaceship import *
from gameMaster import *
import math
import sys


class GameRunner:

	def __init__(self, amnt = 3):
		self.game = GameMaster()
		self.screenMaxX = self.game.get_screen_max_x()
		self.screenMaxY = self.game.get_screen_max_y()
		self.screenMinX = self.game.get_screen_min_x()
		self.screenMinY = self.game.get_screen_min_y()
		shipStartX = (self.screenMaxX-self.screenMinX)/2 + self.screenMinX
		shipStartY = (self.screenMaxY-self.screenMinY)/2 + self.screenMinY
		self.game.set_initial_ship_cords( shipStartX, shipStartY )
		self.game.add_initial_astroids(amnt)
		# created a new class object called dead_torpedos that is a list of
		# our marked for deletion torpedos.
		self.dead_torpedos = []

	def run(self):
		self._do_loop()
		self.game.start_game()

	def _do_loop(self):
		self.game.update_screen()
		self.game_loop()
		# Set the timer to go off again
		self.game.ontimer(self._do_loop,5)

	def move_object(self, obj):
		"""
		Function that moves and object to the proper coordinates
		:param obj: the object we want to move
		"""
		# set our variables to the old coordinates and the speed of the object
		x_cord = obj.get_x_cor()
		y_cord = obj.get_y_cor()
		speed_x = obj.get_speed_x()
		speed_y = obj.get_speed_y()
		delta_x = self.screenMaxX - self.screenMinX
		delta_y = self.screenMaxY - self.screenMinY
		# calculate the new coordinates
		new_cord_x = ((speed_x + x_cord - self.screenMinX) % delta_x) + \
					 self.screenMinX
		new_cord_y = ((speed_y + y_cord - self.screenMinY) % delta_y) + \
					 self.screenMinY
		# use the move method to move our object
		obj.move(new_cord_x, new_cord_y)

	def move_asteroids(self, asteroid_list):
		'''
		:param asteroid_list: our list of asteroids
		'''
		for asteroid in asteroid_list:
			self.move_object(asteroid)

	def move_ship(self, ship):
		"""
		Function that moves the ship based on which buttons the player presses
		:param ship = our ship object
		"""
		# get our ship and it's starting speed
		speed_x = ship.get_speed_x()
		speed_y = ship.get_speed_y()
		# increase or decrease the angle based on what the player presses
		if self.game.is_right_pressed():
			ship.decrease_angle()
		elif self.game.is_left_pressed():
			ship.increase_angle()
		# if the player presses the up arrow, increase the speed in the
		# correct angle
		elif self.game.is_up_pressed():
			angle = ship.get_angle()
			new_speed_x = speed_x + (math.cos(math.radians(angle)))
			new_speed_y = speed_y + (math.sin(math.radians(angle)))
			ship.set_speed_x(new_speed_x)
			ship.set_speed_y(new_speed_y)
		# move the ship using our move_object() method.
		self.move_object(ship)

	def fire_torpedo(self, ship, torpedo_list):
		"""
		Function that adds torpedos to our game when the space bar is pressed
		:param ship = our ship object
		:param torpedo_list = our list of torpedos
		"""
		# use methods to get our ship object, it's speed, angle and location
		speed_x = ship.get_speed_x()
		speed_y = ship.get_speed_y()
		x_cord = ship.get_x_cor()
		y_cord = ship.get_y_cor()
		angle = ship.get_angle()
		# set our maximum torpedo amount to 20 and get our list of torpedos
		MAX_TORPEDO = 20
		# if clauses that check whether the fire is pressed, if it was and
		# there aren't the maximum amount of torpedos then fire a torpedo.
		if self.game.is_fire_pressed():
			if len(torpedo_list) < MAX_TORPEDO:
				tor_speed_x = speed_x + (2 * math.cos(math.radians(angle)))
				tor_speed_y = speed_y + (2 * math.sin(math.radians(angle)))
				self.game.add_torpedo(x_cord, y_cord, tor_speed_x,
									tor_speed_y, angle)

	def mark_torpedo(self, torpedo_list):
		"""
		Function that marks torpedos whose lifespan has ended
		:param torpedo_list = our list of torpedos
		"""
		# Set the lifespan limit to 0
		life_span_ended = 0
		# iterate over the list and if the lifespan ran out, append them to
		#  our list of dead torpedos
		for i in range(len(torpedo_list)):
			life_span = torpedo_list[i].get_life_span()
			if life_span <= life_span_ended:
				self.dead_torpedos.append(torpedo_list[i])

	def move_torpedo(self, torpedo_list):
		"""
		Function that moves the torpedos
		:param torpedo_list = our list of torpedos
		"""
		# iterate over our list of torpedos and call the move_object method
		# on them
		for i in range(len(torpedo_list)):
			self.move_object(torpedo_list[i])

	def create_asteroids(self, old_asteroid, torpedo, size):
		"""
		Function that creates new asteroids when hit by a torpedo
		:param old_asteroid: the asteroid that explodes
		:param torpedo: the torpedo that destroyed the asteroid
		:param size: the size of the asteroid that was destroyed
		"""
		# set our variables to the coordinates and speed of the old asteroid
		#  and torpedo
		x_co = old_asteroid.get_x_cor()
		y_co = old_asteroid.get_y_cor()
		speed_x = old_asteroid.get_speed_x()
		speed_y = old_asteroid.get_speed_y()
		torpedo_speed_x = torpedo.get_speed_x()
		torpedo_speed_y = torpedo.get_speed_y()
		# calculate the new speed
		new_speed_x = ((torpedo_speed_x + speed_x) /
						(math.sqrt((speed_x ** 2) + (speed_y ** 2))))
		new_speed_y = ((torpedo_speed_y + speed_y) /
						(math.sqrt((speed_x ** 2) + (speed_y ** 2))))
		# update the size of the new asteroids
		new_size = size - 1
		# use the add_asteroid method to create the new asteroids going in
		# opposite directions.
		self.game.add_asteroid(x_co, y_co, new_speed_x,
								new_speed_y, new_size)
		self.game.add_asteroid(x_co, y_co, -1 * new_speed_x,
							   -1 * new_speed_y, new_size)

	def blow_asteroids(self, torpedo_list, asteroid_list):
		"""
		Function that checks whether our torpedo hit an asteroid, updates
		the score, removes the asteroid, and adds 2 smallers ones if needed.
		:param torpedo_list: our list of torpedos
		:param asteroid_list: our list of asteroids
		"""
		# Iterates over our torpedo list, asteroid list and checks whether
		# the torpedo collided with any asteroid.
		for torpedo in torpedo_list:
			for asteroid in asteroid_list:
				# if they did collide, get the asteroids size and update
				# score accordingly
				if self.game.intersect(torpedo, asteroid):
					self.dead_torpedos.append(torpedo)
					asteroid_size = asteroid.get_size()
					if asteroid_size == 3:
						self.game.add_to_score(30)
						self.create_asteroids(asteroid, torpedo, 3)
					elif asteroid_size == 2:
						self.game.add_to_score(50)
						self.create_asteroids(asteroid, torpedo, 2)
					elif asteroid_size == 1:
						self.game.add_to_score(100)
					# remove the asteroid that was hit
					self.game.remove_asteroid(asteroid)

	def remove_objects(self, obj):
		"""
		Removes our dead torpedos.
		:param obj: our dead torpedo list
		"""
		self.game.remove_torpedos(obj)

	def ship_collision(self, ship, asteroid_list):
		"""
		Function checks whether the ship has collided with an asteroid. If
		it did, remove a life and show a message.
		:param ship: our ship
		:param asteroid_list: our asteroid list
		"""
		# set our title and message variables
		title = "Collision!"
		message = "Watch out! You have lost 1 life!"
		# iterate over the asteroids
		for asteroid in asteroid_list:
			# check whether any has collided with our ship, if it has print
			# a message, remove the asteroid and take off 1 life.
			if self.game.intersect(ship, asteroid):
				self.game.remove_asteroid(asteroid)
				self.game.ship_down()
				self.game.show_message(title, message)

	def end_game(self, asteroid_list):
		'''
		Checks whether the game ended and prints the appropriate message
		:param asteroid_list: our list of asteroids
		'''
		# set our constant EMPTY to 0 and our variable lives to lives we have
		EMPTY = 0
		lives = self.game.get_num_lives()
		# set the game_end to False while game isn't lost
		game_end = False
		# check if the different lose clauses exist, if they do update the
		# message and change the boolean value of game_end
		if lives <= EMPTY:
			title = "You lose!"
			message = "You lost the game!"
			game_end = True
		elif len(asteroid_list) == EMPTY:
			title = "You win!"
			message = "Congratulations! You have destroyed all the asteroids!"
			game_end = True
		elif self.game.should_end():
			title = "You quit!"
			message = "You have quit the game."
			game_end = True
		# if the game ended, print the message and quit the game
		if game_end:
			self.game.show_message(title, message)
			self.game.end_game()

	def game_loop(self):
		'''
		Function that runs the game and calls the appropriate methods.
		'''
		# set our variables that we will use in multiple methods.
		torpedo_list = self.game.get_torpedos()
		asteroid_list = self.game.get_asteroids()
		ship = self.game.get_ship()
		#call the appropriate methods that the game uses
		self.move_asteroids(asteroid_list)
		self.move_ship(ship)
		self.fire_torpedo(ship, torpedo_list)
		self.mark_torpedo(torpedo_list)
		self.move_torpedo(torpedo_list)
		self.blow_asteroids(torpedo_list, asteroid_list)
		self.remove_objects(self.dead_torpedos)
		self.ship_collision(ship, asteroid_list)
		self.end_game(asteroid_list)


def main(amount):
	runner = GameRunner(amount)
	runner.run()

if __name__ == "__main__":
	# Set the default amount of asteroids to 3
	amount = 3
	# if an argument is entered in the command line set the asteroid amount
	# to that argument
	if len(sys.argv) == 2:
		amount = int(sys.argv[1])
	# call our main function with the amount of asteroids
	main(amount)
