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

#Load Boss File        
file = open("Bosses\\Boss1.txt")
abilities = []

for line in file.read().split("\n"):
    parts = line.split(" - ")
    dice = parts[0].split(",")
    abilities.append(Ability(dice, parts[1]))

# for a in abilities:
#     print(str(a.dice) + ": " + a.text)
players = ""
while not players.isnumeric():
    print("Starting new game, how many players?")
    players = input()
    if not players.isnumeric():
        print("please enter a valid number")

players = int(players)
bossLife = 20 * players
print("Boss starting life total is " + str(bossLife))

response = ""
turns = 1
while response != "end":
    log.green("------ Turn " + str(turns) + " boss life is " + str(bossLife) + "------")
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
                    
                    if "drains" in text:
                        life = int(text[text.index("drains"):text.index["life"]].replace("drains ", "").strip())
                        bossLife = bossLife + (life * players)

                    log.red(text)
                    break

    print("Enter damage to the boss or type 'end' to end game and press enter")
    response = input()
    if response.isnumeric():
        bossLife = bossLife - int(response)
        if bossLife <= 0:
            log.green("******* You Win ********")
            break

    turns = turns + 1