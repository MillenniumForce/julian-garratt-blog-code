# This program was created by Julian Garratt
# Program created for Live Beyond Data Science

from random import randint
import sys
import statistics
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import heapq

def generateRoll():
    return randint(1,6)

def friendlyWon(friendly_dice_roll, enemy_dice_roll):
    if (friendly_dice_roll <= enemy_dice_roll): return False
    else: return True

class game: 
    def __init__(self, friendly_soldiers, enemy_soldiers):
        self.friendly_soldiers = friendly_soldiers
        self.enemy_soldiers = enemy_soldiers
        self.round = 0

    def no_friendly_dice(self): # get maximum number of friendly dice
        if self.friendly_soldiers >= 3: return 3 # dice roll is equal to 3 if they have more than 3 soldiers
        else: return self.friendly_soldiers-1 # else return dice roll as less than 3 (greater than 0) Note that its -1 as friendly must have at least 1 soldier
    
    def no_enemy_dice(self): # get maximum number of enemey dice
        if self.enemy_soldiers >= 2: return 2 # max that an enemy can roll is 2 
        else: return 1 
    
    def get_rolls(self, number_of_dice):
        dice_rolls = []
        for _ in range(0,number_of_dice): # get random rolls for each dice that the player has
            dice_rolls.append(generateRoll())
        return dice_rolls

    def process_battle(self, friendly_rolls, enemy_rolls): # get the maximum number of friendly soldiers lost given friendly rolls and enemy rolls
        battle_size = min(len(friendly_rolls), len(enemy_rolls)) # battle size determines how many dice can both players use (i.e. if enemy only has 2 dice then only best 2 friendly dice can be used)
        best_enemy_rolls = heapq.nlargest(battle_size, enemy_rolls) # get highest N enemy rolls
        best_friendly_rolls = heapq.nlargest(battle_size, friendly_rolls) # get highest N friendly rolls
        for i in range(0,battle_size): # check the highest enemy roll and friendly roll, then 2nd highest, 3rd....
            if friendlyWon(best_friendly_rolls[i], best_enemy_rolls[i]) is True: self.enemy_soldiers -= 1 # if friendly one then enemy loses a soldier
            else: self.friendly_soldiers -= 1 # if enemy one friendly loses a soldier

    def playGame(self):
        # Initialise record of soldiers to return
        friendly_soldiers = []
        rounds = []
        rounds.append(self.round)
        friendly_soldiers.append(self.friendly_soldiers)


        while (self.friendly_soldiers > 1 and self.enemy_soldiers > 0): ## while the game is playing do
            friendly_rolls = self.get_rolls(self.no_friendly_dice())
            enemy_rolls = self.get_rolls(self.no_enemy_dice())
            self.process_battle(friendly_rolls, enemy_rolls)
            self.round += 1
            friendly_soldiers.append(self.friendly_soldiers)
            rounds.append(self.round)
            print("Round = %d | Friendly Soldiers = %d Enemy Soldiers = %d" % (self.round, self.friendly_soldiers, self.enemy_soldiers))

        if self.friendly_soldiers == 1: return False # friendly lost (friendly cannot get to 0 when attacking)
        else: return True # friendly won 

if __name__ == "__main__":
    friendly_soldiers_list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    enemy_soldiers_list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]

    results = [[0 for i in range(len(friendly_soldiers_list)+1)] for j in range(len(enemy_soldiers_list)+1)]
    for _ in range(0,10001): # this controls how long the simulation will run for (10001 seems to be a good limit anything larger such as 100000 will take a significant amount of time approx 6 hrs)
        for friendly_soldiers in friendly_soldiers_list:
            for enemy_soldiers in enemy_soldiers_list:
                new_game = game(friendly_soldiers,enemy_soldiers)
                result = new_game.playGame()
                results[enemy_soldiers][friendly_soldiers] += result
    print(results)
    plt.pcolormesh(results, cmap = 'seismic')
    plt.xlim(1,len(friendly_soldiers_list)+1)
    plt.ylim(1,len(enemy_soldiers_list)+1)
    plt.xticks(np.linspace(1,16,16))
    plt.yticks(np.linspace(1,16,16))
    plt.xlabel("Friendly Armies")
    plt.ylabel("Enemy Armies")
    plt.title("Proportion of Friendly Wins")
    cbar = plt.colorbar(ticks = [0,(10001/2),10001])
    cbar.set_ticklabels(['low','medium','high'])
    plt.show()
        
