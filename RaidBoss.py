import random
import re
import os

os.system('cls')

class log:
    f = lambda color: lambda string: print(color + string + "\33[0m")

    red = f("\33[31m")
    green = f("\33[32m")
    yellow = f("\33[33m")
    white = f("\33[37m")

class Ability:
    def __init__(self, dice, text):
        self.dice = dice
        self.text = text

def loadFile(level):
    #Load Boss File        
    file = open("Bosses\\" + level + ".txt")
    abilities = []

    for line in file.read().split("\n"):
        parts = line.split(" - ")
        dice = parts[0].split(",")
        abilities.append(Ability(dice, parts[1]))

    return abilities


players = ""
while not players.isnumeric():
    players = input("Starting new game, how many players? ")
    if not players.isnumeric():
        print("please enter a valid number")

players = int(players)

response = ""
abilities = []
multiplier = 20
while True:
    response = input("What level do you want to play? easy=e medium=m hard=h custom=c ")
    if response == "e" or response == "m" or response == "h" or response == "c":
        if response == "e":
            file = "easy"
        if response == "m":
            file = "medium"
            multiplier = 25
        elif response == "h":
            file = "hard"
            multiplier = 50
        elif response == "c":
            file = "custom"
            multiplier = 40

        abilities = loadFile(file)
        break


bossLife = multiplier * players
startingLife = bossLife
print("Raid monster starting life total is " + str(bossLife))
print("--------------------------------")

response = ""
turn = 1
log.white("Type 'end' at any time to end game")
while response != "end":
    log.green("------ Turn " + str(turn) + "------")

    response = input("Enter damage done to boss: ")
    if response.isnumeric():
        # if damage is numeric subtract it from bosses life total
        bossLife = bossLife - int(response)
        if bossLife <= 0:
            log.green("******* You Win ********")
            print("press enter to end program")
            # TODO - figure out how to ask about doing a new game
            x = input()
            break

    if turn == 1:
        print("Raid monster does nothing")
    else:
        rolls = 0
        #Calculate the number of rolls by which turn we are on
        # it is the turn divided by 2 rounded down
        if turn % 2 == 0:
            rolls = int(turn/2)
        else:
            rolls = int((turn-1)/2)
        
        for r in range(rolls):
            roll = random.randint(1,20)
            log.yellow("Raid monster rolled " + str(roll) + " on roll " + str(r+1) + " of " + str(rolls))

            for ability in abilities:
                if str(roll) in str(ability.dice):
                    text = ability.text
                    if "{X}" in text:
                        # simple replace of an X placeholder by the number of rolls
                        text = text.replace("{X}", str(rolls))
                    elif "Raid Monster gains" in text:
                        # life gain ability must be in this format to work
                        lifeIndex = text.index("life")
                        life = text[0:lifeIndex]
                        life = life.replace("The Raid Monster gains ", "")
                        life = int(life.strip())
                        bossLife = bossLife + life
                    elif "double" in text and "life" in text:
                        if startingLife / 2 > bossLife:
                            bossLife = bossLife * 2                            
                    if "{XP}" in text:
                        #special case in easy where the defenders are per player
                        tokens = rolls * players
                        text = text.replace("{XP}", str(tokens))
                        
                    # checks for X adding, multiplying, or subtracting by a single digit
                    # must be in format {X+1}, {X/2}, or {X*2}
                    # formula must be surround by {}, X must come first, followed by
                    # operation and then a single digit
                    addPattern = "\{X(\+|\*|/)\d{1}\}"
                    match = re.search(addPattern, text)
                    if match:
                        placeholder = match.group()
                        operation = placeholder[2:3]
                        value = placeholder[3:4]
                        
                        if operation == "+":
                            value = int(value) + rolls
                        elif operation == "*":
                            value = int(value) * rolls
                        elif operation == "/":
                            # can only divide by 2 for this game
                            if rolls % 2 == 0:
                                value = int(rolls / 2)
                            else:
                                # only rounds up
                                value = int((rolls + 1) / 2)
                        text = re.sub(addPattern, str(value), text)
                        
                    if "drains" in text:
                        # drain life ability subtracts X life from all players and boss gains X * players life
                        # for eacmple, drain 3 life with 3 players, boss gains 9 life
                        life = int(text[text.index("drains"):text.index("life")].replace("drains ", "").strip())
                        bossLife = bossLife + (life * players)

                    
                    log.red(text)
                    break

    log.white("Raid monster life = " + str(bossLife))
    turn = turn + 1