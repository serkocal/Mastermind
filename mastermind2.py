import sys
import tty, termios
import random

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def check(code, guess):
    correct_place = 0
    correct_num = 0
    for i, j in zip(code, guess):
        if i == j:
            correct_place += 1

    for i in guess:
        if i in code:
            correct_num += 1
    correct_num -= correct_place

    return correct_place, correct_num

code = "".join(random.choices("12345678",k=4))

colors = {"1":"31",
          "2":"32",
          "3":"33",
          "4":"34",
          "5":"35",
          "6":"36",
          "7":"37",
          "8":"30"}

guess = ""
trys = 9
correct_place = 0
correct_num = 0
while True:
    while True:
        print("\x1b[2K\r\x1b[4D",end="")
        for i in guess:
            print(f"\x1b[1;{colors[i]}m{i}\a",end="",flush=True)

        c = getch()
        if c == "q":
            exit()
        if c == "\r":
            if len(guess) < 4:
                print("\a",end="",flush=True)
                continue
            break
        if c == "\x7f":
            guess = guess[:len(guess)-1]
            #print(guess)
            continue
        if len(guess) == 4:
            print("\a",end="",flush=True)
            continue
        guess += c

    if trys == 0:
        print("\r\x1b[0m")
        print(f"You failed code was ", end="")
        for i in code:
            print(f"\x1b[1;{colors[i]}m{i}\a",end="",flush=True)
        print()
        exit()
    trys -= 1
    if guess == code:
        print("\r\x1b[0m")
        print("You guessed correctly")
        exit()
    else:
        correct_place, correct_num = check(code, guess)
        print(" " + f"\x1b[1;41m " * correct_place + f"\x1b[1;47m " * correct_num + "\x1b[30;40m", flush=True)
        guess=""
        correct_num = 0
        correct_place = 0
