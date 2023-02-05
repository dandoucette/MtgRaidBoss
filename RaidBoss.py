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
    response = input("What level do you want to play? (easy(e)/medium(m)/hard(h)) ")
    if response == "e" or response == "m" or response == "h":
        if response == "e":
            file = "easy"
        if response == "m":
            file = "medium"
            multiplier = 25
        elif response == "h":
            file = "hard"
            multiplier = 50

        abilities = loadFile(file)
        break


bossLife = multiplier * players
print("Boss starting life total is " + str(bossLife))
print("--------------------------------")

response = ""
turns = 1
log.white("Type 'end' at any time to end game")
while response != "end":
    log.green("------ Turn " + str(turns) + "------")

    response = input("Enter damage done to boss: ")
    if response.isnumeric():
        bossLife = bossLife - int(response)
        if bossLife <= 0:
            log.green("******* You Win ********")
            print("press enter to end program")
            x = input()
            break

    if turns == 1:
        print("Boss does nothing")
    else:
        rolls = 0
        if turns % 2 == 0:
            rolls = int(turns/2)
        else:
            rolls = int((turns-1)/2)
        
        for r in range(rolls):
            roll = random.randint(1,20)
            log.yellow("Boss rolled " + str(roll) + " on roll " + str(r+1) + " of " + str(rolls))

            for ability in abilities:
                if str(roll) in str(ability.dice):
                    text = ability.text
                    if "{X}" in text:
                        text = text.replace("{X}", str(rolls))
                    elif "{X/2}" in text:
                        if rolls % 2 == 0:
                            x = int(rolls / 2)
                        else:
                            x = int((rolls + 1) / 2)
                        text = text.replace("{X/2}", str(x))
                    elif "Raid Monster gains" in text:
                        lifeIndex = text.index("life")
                        life = text[0:lifeIndex]
                        life = life.replace("The Raid Monster gains ", "")
                        life = int(life.strip())
                        bossLife = bossLife + life
                    
                    if "{XP}" in text:
                        tokens = rolls * players
                        text = text.replace("{XP}", str(tokens))
                        
                    addPattern = "\{\d\+X\}"
                    match = re.search(addPattern, text)
                    if match:
                        placeholder = match.group()
                        value = placeholder[1:2]
                        value = int(value) + rolls
                        text = re.sub(addPattern, str(value), text)
                        
                    if "drains" in text:
                        life = int(text[text.index("drains"):text.index("life")].replace("drains ", "").strip())
                        bossLife = bossLife + (life * players)

                    
                    log.red(text)
                    break

    log.white("Boss life = " + str(bossLife))
    turns = turns + 1