import os
import keyboard
import time
import threading
import random
from colorama import Fore, init
from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator
import pyfiglet
import sys




init(True)

def clear():
	os.system('cls' if os.name == 'nt' else 'clear')






def keyboard_thread():
	# CHECK KEYS
	global DIRECTION, SPEED
	while True:
		key = keyboard.read_key()
		if key == "down" and DIRECTION != "up":
			DIRECTION = "down"
		elif key == "up" and DIRECTION != "down":
			DIRECTION = "up"
		elif key == "left" and DIRECTION != "right":
			DIRECTION = "left"
		elif key == "right" and DIRECTION != "left":
			DIRECTION = "right"

		elif key == "s" and DIRECTION != "up":
			DIRECTION = "down"
		elif key == "w" and DIRECTION != "down":
			DIRECTION = "up"
		elif key == "a" and DIRECTION != "right":
			DIRECTION = "left"
		elif key == "d" and DIRECTION != "left":
			DIRECTION = "right"



def die():
	print_at_coordinate(SNAKE_CORDS[-1][0], SNAKE_CORDS[-1][1], f"{Fore.RED}X{Fore.RESET}")
	time.sleep(2)
	clear()
	border()
	print_at_coordinate(TERMINAL_COLUMNS // 2, TERMINAL_LINES // 2, "DIED")
	print_at_coordinate(TERMINAL_COLUMNS // 2, TERMINAL_LINES // 2 + 1, f"SCORE: {SCORE}")
	print_at_coordinate(0, TERMINAL_LINES - 3, "")
	input("Press Enter To Continue...")
	main_menu()

def handler():
	print_at_coordinate(SNAKE_CORDS[-1][0], SNAKE_CORDS[-1][1], f"{Fore.RED}X{Fore.RESET}")
	time.sleep(2)
	clear()
	border()
	print_at_coordinate(TERMINAL_COLUMNS // 2, TERMINAL_LINES // 2, "TERMINATED")
	print_at_coordinate(TERMINAL_COLUMNS // 2, TERMINAL_LINES // 2 + 1, f"SCORE: {SCORE}")
	print_at_coordinate(0, TERMINAL_LINES - 3, "")
	input("Press Enter To Continue...")
	main_menu()

def print_at_coordinate(x, y, text):
	print(f"\033[{y};{x}H{text}")


def place_food(x,y):
	global FOOD_CORDS
	print_at_coordinate(x,y,f"{Fore.RED}${Fore.RESET}")

def border():
	print("╔", end="")
	print("═"*(TERMINAL_COLUMNS - 2), end="")
	print("╗")
	print(f"║{' '*(TERMINAL_COLUMNS - 2)}║\n"*(TERMINAL_LINES - 5), end="")
	print("╚", end="")
	print("═"*(TERMINAL_COLUMNS - 2), end="")
	print("╝")

def main():
	global SNAKE_CORDS
	global FOOD_CORDS
	global INC
	global LENGTH
	global SCORE, SPEED
	if LOGGING:
		f = open("log.txt", "w")
	while True:

		
		if LOGGING:
			f.write(str(SNAKE_CORDS))
			f.write("\n")
		clear()
		print(" " * ((TERMINAL_COLUMNS // 2) - len(str(SCORE))), end="")
		print(f"Score: {SCORE}")
		border()
		place_food(FOOD_CORDS[0], FOOD_CORDS[1])
		if DIRECTION == "up":
			SNAKE_CORDS.append([SNAKE_CORDS[INC][0], SNAKE_CORDS[INC][1] - 1])
		elif DIRECTION == "down":
			SNAKE_CORDS.append([SNAKE_CORDS[INC][0], SNAKE_CORDS[INC][1] + 1])
		elif DIRECTION == "left":
			SNAKE_CORDS.append([SNAKE_CORDS[INC][0] - 1, SNAKE_CORDS[INC][1]])
		elif DIRECTION == "right":
			SNAKE_CORDS.append([SNAKE_CORDS[INC][0] + 1, SNAKE_CORDS[INC][1]])

		if DIRECTION == "up" or DIRECTION == "down":
			SPEED = MSPEED + SPEED // 1.5
		else:
			SPEED = MSPEED

		for CORD in SNAKE_CORDS:
			if CORD[0] == 1 or CORD[1] == 2 or CORD[0] == TERMINAL_COLUMNS or CORD[1] == TERMINAL_LINES - 2:
				die()

			if 2 in set([SNAKE_CORDS.count(n) for n in SNAKE_CORDS]):
				for CORD in SNAKE_CORDS:
					print_at_coordinate(CORD[0], CORD[1], "*")
				die()

			if CORD == FOOD_CORDS:
				LENGTH += 1
				SCORE += 1
				FOOD_CORDS = [random.randint(2, TERMINAL_COLUMNS - 1), random.randint(3, TERMINAL_LINES - 3)]

			print_at_coordinate(CORD[0], CORD[1], "*")



		if len(SNAKE_CORDS) > LENGTH:
			SNAKE_CORDS.pop(0)
			INC -= 1

		INC += 1
		time.sleep(SPEED)

def start():
	global TERMINAL_SIZE
	global TERMINAL_COLUMNS
	global TERMINAL_LINES
	global SNAKE_CORDS
	global FOOD_CORDS
	global INC
	global DIRECTION
	global LENGTH
	global SCORE

	#TERMINAL CONFIG
	TERMINAL_SIZE = os.get_terminal_size()
	TERMINAL_LINES = int(TERMINAL_SIZE.lines)
	TERMINAL_COLUMNS = int(TERMINAL_SIZE.columns)
	SNAKE_CORDS = [[TERMINAL_COLUMNS // 2, TERMINAL_LINES // 2]]

	# SNAKE CONFIG
	INC = 0
	DIRECTION = "up"
	LENGTH = 3
	SCORE = 0

	# FOOD CONFIG
	FOOD_CORDS = [random.randint(2, TERMINAL_COLUMNS - 1), random.randint(3, TERMINAL_LINES - 3)]
	
	# STARTUP
	key_thread = threading.Thread(target=keyboard_thread, daemon = True)
	key_thread.start()
	main()

def logo():
	return str(pyfiglet.figlet_format("Snake")) + "\n"


def settings():
	global SPEED
	global MSPEED
	global USER_SPEED_NUM
	global USER_SPEED_NUM_LITERAL
	global LOGGING
	clear()
	print(logo())
	setting_choice = inquirer.select(
			message = "Select Option",
			choices = ["Snake Speed", "Logging", "Back"]
		).execute()

	if setting_choice.lower() == "snake speed":
		clear()
		print(logo())
		print(f"Current Speed: {USER_SPEED_NUM}")
		integer_val = inquirer.number(
			message="Enter Speed Value (Use ↑↓ Arrow Keys) :",
			min_allowed=1,
			max_allowed=10,
			validate=EmptyInputValidator(),
			default=USER_SPEED_NUM,
		).execute()
		USER_SPEED_NUM = int(integer_val)
		USER_SPEED_NUM_LITERAL = 11 - USER_SPEED_NUM
		MSPEED = float(USER_SPEED_NUM_LITERAL / 30)
		SPEED = MSPEED
		settings()
	elif setting_choice.lower() == "logging":
		clear()
		print(logo())
		print(f"Logging: {LOGGING}")
		logging_option = inquirer.confirm("Enter Choice: ").execute()
		settings()
	elif setting_choice.lower() == "back":
		main_menu()

def main_menu():
	clear()
	print(logo())
	menu_choice = inquirer.select(
		message = "Select Option",
		choices = ["Play", "Settings", "Help", "Exit"]
	).execute()

	if menu_choice.lower() == "play":
		try:
			start()
		except KeyboardInterrupt:
			handler()

	elif menu_choice.lower() == "settings":
		settings()

	elif menu_choice.lower() == "help":
		help()
	elif menu_choice.lower() == "exit":
		exit()



if __name__ == "__main__":
	# MISC
	LOGGING = False

	# SPEED CONFIG
	USER_SPEED_NUM = 7
	USER_SPEED_NUM_LITERAL = 11 - USER_SPEED_NUM
	MSPEED = float(USER_SPEED_NUM_LITERAL / 30)
	SPEED = MSPEED

	# MENU
	try:
		main_menu()
	except KeyboardInterrupt:
		exit()



