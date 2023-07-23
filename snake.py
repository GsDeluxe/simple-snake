import os
import keyboard
import time
import threading
import random
from colorama import Fore, init

init(True)



def clear():
	os.system('cls' if os.name == 'nt' else 'clear')

def pause():
	clear()
	print_at_coordinate(TERMINAL_COLUMNS // 2, TERMINAL_LINES // 2, "Paused")
	print_at_coordinate(TERMINAL_COLUMNS // 2, TERMINAL_LINES // 2 + 1, "Press Enter To Continue")
	input()





def keyboard_thread():
	global DIRECTION, SPEED
	PAUSED = False
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



def die():
	print_at_coordinate(SNAKE_CORDS[-1][0], SNAKE_CORDS[-1][1], f"{Fore.RED}X{Fore.RESET}")
	time.sleep(2)
	clear()
	border()
	print_at_coordinate(TERMINAL_COLUMNS // 2, TERMINAL_LINES // 2, "DIED")
	print_at_coordinate(TERMINAL_COLUMNS // 2, TERMINAL_LINES // 2 + 1, f"SCORE: {SCORE}")
	print_at_coordinate(0, TERMINAL_LINES - 3, "")
	input("Press Enter To Exit...")
	exit()


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
	f = open("log.txt", "w")
	while True:
		f.write(str(SNAKE_CORDS))
		f.write("\n")
		clear()
		print(" " * ((TERMINAL_COLUMNS // 2) - 2), end="")
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
			SPEED = MSPEED + 0.04
		else:
			SPEED = MSPEED

		for CORD in SNAKE_CORDS:
			if CORD[0] == 1 or CORD[1] == 2 or CORD[0] == TERMINAL_COLUMNS - 1 or CORD[1] == TERMINAL_LINES - 1:
				die()

			if 2 in set([SNAKE_CORDS.count(n) for n in SNAKE_CORDS]):
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

#def menu():
	


if __name__ == "__main__":
	
	INC = 0
	DIRECTION = "up"
	LENGTH = 7
	SCORE = 0
	MSPEED = 0.07
	SPEED = MSPEED
	TERMINAL_SIZE = os.get_terminal_size()
	TERMINAL_LINES = int(TERMINAL_SIZE.lines)
	TERMINAL_COLUMNS = int(TERMINAL_SIZE.columns)
	SNAKE_CORDS = [[TERMINAL_COLUMNS // 2, TERMINAL_LINES // 2]]
	FOOD_CORDS = [random.randint(2, TERMINAL_COLUMNS - 1), random.randint(3, TERMINAL_LINES - 3)]
	key_thread = threading.Thread(target=keyboard_thread, daemon = True)
	key_thread.start()
	main()
