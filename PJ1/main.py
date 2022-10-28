from numpy.random import rand, uniform
from ai import COLOR_BLACK, COLOR_WHITE

import final
import final2
import ai
import numpy as np
import random
import time
import argparse
DRAW = 0
WIN = 1
LOSE = -1

dim = 3
global_env = [[500,-45,10,5,5,10,-45,500],
                    [-45,5,1,1,1,1,5,-45],
                    [10,1,3,2,2,3,1,10],
                    [5,1,2,1,1,2,1,5],
                    [5,1,2,1,1,2,1,5],
                    [10,1,3,2,2,3,1,10],
                    [-45,5,1,1,1,1,5,-45],
                    [500,-45,10,5,5,10,-45,500]]

class Individual(object):
    def __init__(self, id:int, variable:np.ndarray, fitness=0):
        self.id = id
        self.variable = variable
        self.fitness = fitness
        pass

global id; id = 0
def count():
    global id
    id = id+1
    return id

def compete(variable1, type1=ai, variable2=None, type2=ai, is_random=False):
    player = type1.AI(8, COLOR_BLACK, 1, variable1, global_env)
    if is_random == False:
        opponent = type2.AI(8, COLOR_WHITE, 1, variable2, global_env)
    else:
        opponent = ai.RandomAI(8, COLOR_WHITE, 1, variable2, global_env)
    if is_random == True:
        return random.choice([-2, 0, 2])
    return twobattle(player, opponent)

def twobattle(player, opponent):
    player.color = COLOR_BLACK
    opponent.color = COLOR_WHITE
    r1 = battle(player, opponent, COLOR_BLACK)
    player.color = COLOR_WHITE
    opponent.color = COLOR_BLACK
    r2 = battle(player, opponent, COLOR_BLACK)
    return r1+r2

def battle(player, opponent, color):
    chessboard = np.zeros((8,8), dtype=int)
    chessboard[3][3] = chessboard[4][4] = COLOR_BLACK
    chessboard[3][4] = chessboard[4][3] = COLOR_WHITE
    result = DRAW
    cnt = 0
    while True:
        is_playing = False
        if color == player.color:
            list = player.go(chessboard)
            if len(list) > 0:
                chessboard = player.play(player.color, list[-1], chessboard)
                is_playing = True
        else:
            list = opponent.go(chessboard)
            if len(list) > 0:
                chessboard = opponent.play(opponent.color, list[-1], chessboard)
                is_playing = True
        color = -color
        print(chessboard)
        print(list)
        if is_playing == False:
            cnt += 1
        else:
            cnt = 0
        if cnt >= 2:
            pl_cnt = len(np.where(chessboard == player.color)[0])
            op_cnt = len(np.where(chessboard == opponent.color)[0])
            print(pl_cnt, op_cnt)
            if pl_cnt > op_cnt:
                result = LOSE
            elif pl_cnt < op_cnt:
                result = WIN
            else:
                result = DRAW
            break
    return result

def transform(env):
    temp = np.zeros((8,8))
    for i in range(4):
        for j in range(4):
            temp[7-i][j] = temp[7-i][7-j] = temp[i][7-j] = temp[i][j] = env[i][j]
    return temp

def rand_array():
    temp = np.zeros(dim)
    temp[2] = random.uniform(0, 1)
    temp[1] = random.uniform(0, temp[2])
    temp[0] = random.uniform(0, temp[1])
    return temp

def normal(v):
    temp = np.copy(v)
    if temp[0] >= 1:
        temp[0] = 1
    if temp[0] <= 0:
        temp[0] = 0
    if temp[1] >= 1:
        temp[1] = 1
    if temp[1] <= 0:
        temp[1] = 0
    if temp[2] >= 1:
        temp[2] = 1
    if temp[2] <= 0:
        temp[2] = 0
    temp = np.sort(temp)
    return temp

def climb(v, env, pos, weight):
    dv = np.zeros(dim)
    dv[pos] = weight
    delta = 0.25
    while dv[pos] > 0:
        dv[pos] = dv[pos] - delta
        tv1 = v+dv
        tv2 = v-dv
        player = ai.AI(8, COLOR_BLACK, 1, v, env)
        opponent1 = ai.AI(8, COLOR_WHITE, 1, tv1, env)
        opponent2 = ai.AI(8, COLOR_WHITE, 1, tv2, env)
        r1 = twobattle(player, opponent1)
        r2 = twobattle(player, opponent2)
        if r1 >= 0 and r2 < 0:
            v = tv2
        if r1 < 0 and r2 >= 0:
            v = tv1
        print(dv[pos], v)
    return v

def test():
    log = [[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,1,-1,0,0,0],[0,0,0,-1,-1,0,0,0],[0,0,0,0,-1,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]],[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,1,1,1,0,0],[0,0,0,-1,-1,0,0,0],[0,0,0,0,-1,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]],[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,-1,0,0,0],[0,0,0,1,-1,1,0,0],[0,0,0,-1,-1,0,0,0],[0,0,0,0,-1,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]],[[0,0,0,0,0,0,0,0],[0,0,0,1,0,0,0,0],[0,0,0,0,1,0,0,0],[0,0,0,1,-1,1,0,0],[0,0,0,-1,-1,0,0,0],[0,0,0,0,-1,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]],[[0,0,0,0,0,0,0,0],[0,0,0,1,0,0,0,0],[0,0,0,0,1,0,0,0],[0,0,-1,-1,-1,1,0,0],[0,0,0,-1,-1,0,0,0],[0,0,0,0,-1,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]],[[0,0,0,0,0,0,0,0],[0,0,0,1,0,0,0,0],[0,0,0,0,1,0,0,0],[0,0,-1,-1,-1,1,0,0],[0,0,0,-1,1,0,0,0],[0,0,0,1,-1,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]],[[0,0,0,0,0,0,0,0],[0,0,0,1,0,0,0,0],[0,0,0,0,1,0,0,0],[0,0,-1,-1,-1,1,0,0],[0,0,0,-1,-1,-1,0,0],[0,0,0,1,-1,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]],[[0,0,0,0,0,0,0,0],[0,0,0,1,0,0,0,0],[0,0,0,0,1,0,0,0],[0,0,-1,1,-1,1,0,0],[0,0,1,-1,-1,-1,0,0],[0,0,0,1,-1,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]],[[0,0,0,0,0,0,0,0],[0,0,0,1,0,0,0,0],[0,0,0,-1,1,0,0,0],[0,0,-1,-1,-1,1,0,0],[0,0,1,-1,-1,-1,0,0],[0,0,0,1,-1,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]],[[0,0,0,0,0,0,0,0],[0,0,0,1,0,0,0,0],[0,0,0,-1,1,0,0,0],[0,0,-1,-1,-1,1,0,0],[0,0,1,-1,-1,1,0,0],[0,0,0,1,1,1,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]],[[0,0,0,0,0,0,0,0],[0,0,0,1,0,0,0,0],[0,0,0,-1,1,0,0,0],[0,0,-1,-1,-1,1,0,0],[0,0,1,-1,-1,1,0,0],[0,0,0,-1,1,1,0,0],[0,0,0,-1,0,0,0,0],[0,0,0,0,0,0,0,0]],[[0,0,0,0,0,0,0,0],[0,0,0,1,0,0,0,0],[0,0,0,-1,1,0,0,0],[0,0,-1,-1,-1,1,0,0],[0,0,1,-1,-1,1,0,0],[0,0,0,1,1,1,0,0],[0,0,0,-1,1,0,0,0],[0,0,0,0,0,0,0,0]],[[0,0,0,-1,0,0,0,0],[0,0,0,-1,0,0,0,0],[0,0,0,-1,1,0,0,0],[0,0,-1,-1,-1,1,0,0],[0,0,1,-1,-1,1,0,0],[0,0,0,1,1,1,0,0],[0,0,0,-1,1,0,0,0],[0,0,0,0,0,0,0,0]],[[0,0,0,-1,0,0,0,0],[0,0,0,-1,0,0,0,0],[0,0,0,-1,1,0,0,0],[0,1,1,1,1,1,0,0],[0,0,1,-1,-1,1,0,0],[0,0,0,1,1,1,0,0],[0,0,0,-1,1,0,0,0],[0,0,0,0,0,0,0,0]],[[0,0,0,-1,0,0,0,0],[0,0,0,-1,0,0,0,0],[0,0,0,-1,1,0,0,0],[0,1,1,1,1,1,0,0],[0,0,1,-1,-1,1,0,0],[0,0,0,1,1,-1,0,0],[0,0,0,-1,1,0,-1,0],[0,0,0,0,0,0,0,0]],[[0,0,0,-1,0,0,0,0],[0,0,0,-1,0,0,0,0],[0,0,0,-1,1,0,0,0],[0,1,1,1,1,1,0,0],[0,0,1,-1,-1,1,1,0],[0,0,0,1,1,1,0,0],[0,0,0,-1,1,0,-1,0],[0,0,0,0,0,0,0,0]],[[0,0,0,-1,0,0,0,0],[0,0,0,-1,-1,0,0,0],[0,0,0,-1,-1,0,0,0],[0,1,1,1,-1,1,0,0],[0,0,1,-1,-1,1,1,0],[0,0,0,1,1,1,0,0],[0,0,0,-1,1,0,-1,0],[0,0,0,0,0,0,0,0]],[[0,0,0,-1,0,0,0,0],[0,0,0,-1,-1,1,0,0],[0,0,0,-1,1,0,0,0],[0,1,1,1,-1,1,0,0],[0,0,1,-1,-1,1,1,0],[0,0,0,1,1,1,0,0],[0,0,0,-1,1,0,-1,0],[0,0,0,0,0,0,0,0]],[[0,0,0,-1,0,0,0,0],[0,0,0,-1,-1,1,0,0],[0,0,0,-1,-1,-1,0,0],[0,1,1,1,-1,1,0,0],[0,0,1,-1,-1,1,1,0],[0,0,0,1,1,1,0,0],[0,0,0,-1,1,0,-1,0],[0,0,0,0,0,0,0,0]],[[0,0,0,-1,0,0,0,0],[0,0,1,1,1,1,0,0],[0,0,0,1,-1,-1,0,0],[0,1,1,1,1,1,0,0],[0,0,1,-1,-1,1,1,0],[0,0,0,1,1,1,0,0],[0,0,0,-1,1,0,-1,0],[0,0,0,0,0,0,0,0]],[[0,0,0,-1,0,0,-1,0],[0,0,1,1,1,-1,0,0],[0,0,0,1,-1,-1,0,0],[0,1,1,1,1,1,0,0],[0,0,1,-1,-1,1,1,0],[0,0,0,1,1,1,0,0],[0,0,0,-1,1,0,-1,0],[0,0,0,0,0,0,0,0]],[[0,0,0,-1,0,0,-1,0],[0,0,1,1,1,-1,0,0],[0,0,0,1,-1,1,0,0],[0,1,1,1,1,1,1,0],[0,0,1,-1,-1,1,1,0],[0,0,0,1,1,1,0,0],[0,0,0,-1,1,0,-1,0],[0,0,0,0,0,0,0,0]],[[0,0,0,-1,0,0,-1,0],[0,0,1,1,1,-1,-1,0],[0,0,0,1,-1,-1,0,0],[0,1,1,1,-1,1,1,0],[0,0,1,-1,-1,1,1,0],[0,0,0,1,1,1,0,0],[0,0,0,-1,1,0,-1,0],[0,0,0,0,0,0,0,0]],[[0,0,0,-1,0,0,-1,0],[0,0,1,1,1,1,1,1],[0,0,0,1,-1,-1,0,0],[0,1,1,1,-1,1,1,0],[0,0,1,-1,-1,1,1,0],[0,0,0,1,1,1,0,0],[0,0,0,-1,1,0,-1,0],[0,0,0,0,0,0,0,0]],[[0,0,0,-1,0,0,-1,0],[0,0,1,1,1,1,-1,1],[0,0,0,1,-1,-1,-1,0],[0,1,1,1,-1,-1,1,0],[0,0,1,-1,-1,1,1,0],[0,0,0,1,1,1,0,0],[0,0,0,-1,1,0,-1,0],[0,0,0,0,0,0,0,0]],[[0,0,0,-1,0,0,-1,0],[0,0,1,1,1,1,-1,1],[0,0,0,1,-1,-1,1,0],[0,1,1,1,-1,-1,1,1],[0,0,1,-1,-1,1,1,0],[0,0,0,1,1,1,0,0],[0,0,0,-1,1,0,-1,0],[0,0,0,0,0,0,0,0]],[[0,0,-1,-1,0,0,-1,0],[0,0,1,-1,1,1,-1,1],[0,0,0,1,-1,-1,1,0],[0,1,1,1,-1,-1,1,1],[0,0,1,-1,-1,1,1,0],[0,0,0,1,1,1,0,0],[0,0,0,-1,1,0,-1,0],[0,0,0,0,0,0,0,0]],[[0,0,-1,-1,0,0,-1,0],[0,0,1,-1,1,1,-1,1],[0,0,0,1,-1,-1,1,0],[0,1,1,1,-1,-1,1,1],[0,0,1,-1,-1,1,1,0],[0,0,0,1,1,1,0,0],[0,0,1,1,1,0,-1,0],[0,0,0,0,0,0,0,0]],[[0,0,-1,-1,0,0,-1,0],[0,0,1,-1,1,1,-1,1],[0,0,0,1,-1,-1,-1,-1],[0,1,1,1,-1,-1,1,1],[0,0,1,-1,-1,1,1,0],[0,0,0,1,1,1,0,0],[0,0,1,1,1,0,-1,0],[0,0,0,0,0,0,0,0]],[[0,0,-1,-1,0,0,-1,0],[0,0,1,-1,1,1,-1,1],[0,0,0,1,-1,-1,-1,-1],[0,1,1,1,-1,-1,1,1],[0,0,1,-1,-1,1,1,0],[0,0,0,1,1,1,0,0],[0,0,1,1,1,0,1,0],[0,0,0,0,0,0,0,1]],[[0,0,-1,-1,0,0,-1,-1],[0,0,1,-1,1,1,-1,-1],[0,0,0,1,-1,-1,-1,-1],[0,1,1,1,-1,-1,1,1],[0,0,1,-1,-1,1,1,0],[0,0,0,1,1,1,0,0],[0,0,1,1,1,0,1,0],[0,0,0,0,0,0,0,1]],[[0,-1,-1,-1,0,0,-1,-1],[0,0,-1,-1,1,1,-1,-1],[0,0,0,-1,-1,-1,-1,-1],[0,1,1,1,-1,-1,1,1],[0,0,1,-1,-1,1,1,0],[0,0,0,1,1,1,0,0],[0,0,1,1,1,0,1,0],[0,0,0,0,0,0,0,1]],[[0,-1,-1,-1,0,0,-1,-1],[0,1,1,1,1,1,-1,-1],[0,0,0,-1,-1,-1,-1,-1],[0,1,1,1,-1,-1,1,1],[0,0,1,-1,-1,1,1,0],[0,0,0,1,1,1,0,0],[0,0,1,1,1,0,1,0],[0,0,0,0,0,0,0,1]],[[0,-1,-1,-1,0,-1,-1,-1],[0,1,1,1,-1,-1,-1,-1],[0,0,0,-1,-1,-1,-1,-1],[0,1,1,1,-1,-1,1,1],[0,0,1,-1,-1,1,1,0],[0,0,0,1,1,1,0,0],[0,0,1,1,1,0,1,0],[0,0,0,0,0,0,0,1]],[[0,-1,-1,-1,1,-1,-1,-1],[0,1,1,1,1,1,-1,-1],[0,0,0,-1,1,-1,1,-1],[0,1,1,1,1,-1,1,1],[0,0,1,-1,1,1,1,0],[0,0,0,1,1,1,0,0],[0,0,1,1,1,0,1,0],[0,0,0,0,0,0,0,1]],[[0,-1,-1,-1,1,-1,-1,-1],[0,1,-1,1,1,1,-1,-1],[0,0,-1,-1,1,-1,1,-1],[0,1,1,1,1,-1,1,1],[0,0,1,-1,1,1,1,0],[0,0,0,1,1,1,0,0],[0,0,1,1,1,0,1,0],[0,0,0,0,0,0,0,1]],[[0,-1,-1,-1,1,-1,-1,-1],[0,1,-1,1,1,1,-1,-1],[0,0,-1,-1,1,-1,1,-1],[0,1,1,1,1,-1,1,1],[0,0,1,1,1,1,1,0],[0,0,1,1,1,1,0,0],[0,0,1,1,1,0,1,0],[0,0,0,0,0,0,0,1]],[[0,-1,-1,-1,1,-1,-1,-1],[-1,-1,-1,1,1,1,-1,-1],[0,0,-1,-1,1,-1,1,-1],[0,1,1,1,1,-1,1,1],[0,0,1,1,1,1,1,0],[0,0,1,1,1,1,0,0],[0,0,1,1,1,0,1,0],[0,0,0,0,0,0,0,1]],[[0,-1,-1,-1,1,-1,-1,-1],[-1,-1,-1,1,1,1,-1,-1],[0,1,1,1,1,-1,1,-1],[0,1,1,1,1,-1,1,1],[0,0,1,1,1,1,1,0],[0,0,1,1,1,1,0,0],[0,0,1,1,1,0,1,0],[0,0,0,0,0,0,0,1]],[[0,-1,-1,-1,1,-1,-1,-1],[-1,-1,-1,1,1,1,-1,-1],[-1,-1,-1,-1,-1,-1,1,-1],[0,1,1,1,1,-1,1,1],[0,0,1,1,1,1,1,0],[0,0,1,1,1,1,0,0],[0,0,1,1,1,0,1,0],[0,0,0,0,0,0,0,1]],[[1,1,1,1,1,-1,-1,-1],[-1,1,-1,1,1,1,-1,-1],[-1,-1,1,-1,-1,-1,1,-1],[0,1,1,1,1,-1,1,1],[0,0,1,1,1,1,1,0],[0,0,1,1,1,1,0,0],[0,0,1,1,1,0,1,0],[0,0,0,0,0,0,0,1]],[[1,1,1,1,1,-1,-1,-1],[-1,1,-1,1,1,1,-1,-1],[-1,-1,1,-1,-1,-1,1,-1],[0,1,1,1,1,-1,-1,-1],[0,0,1,1,1,1,1,-1],[0,0,1,1,1,1,0,0],[0,0,1,1,1,0,1,0],[0,0,0,0,0,0,0,1]],[[1,1,1,1,1,-1,-1,-1],[1,1,1,1,1,1,-1,-1],[1,1,1,-1,-1,-1,1,-1],[1,1,1,1,1,-1,-1,-1],[0,0,1,1,1,1,1,-1],[0,0,1,1,1,1,0,0],[0,0,1,1,1,0,1,0],[0,0,0,0,0,0,0,1]],[[1,1,1,1,1,-1,-1,-1],[1,1,1,1,1,1,-1,-1],[1,1,1,-1,-1,-1,1,-1],[1,1,1,1,-1,-1,-1,-1],[0,0,1,1,1,-1,-1,-1],[0,0,1,1,1,1,-1,0],[0,0,1,1,1,0,1,0],[0,0,0,0,0,0,0,1]],[[1,1,1,1,1,-1,-1,-1],[1,1,1,1,1,1,-1,-1],[1,1,1,1,-1,-1,1,-1],[1,1,1,1,1,-1,-1,-1],[0,0,1,1,1,1,-1,-1],[0,0,1,1,1,1,1,0],[0,0,1,1,1,0,1,1],[0,0,0,0,0,0,0,1]],[[1,1,1,1,1,-1,-1,-1],[1,1,1,1,1,1,-1,-1],[1,1,1,1,-1,-1,1,-1],[1,1,1,1,1,-1,-1,-1],[0,0,1,1,1,-1,-1,-1],[0,0,1,1,1,-1,-1,0],[0,0,1,1,1,-1,1,1],[0,0,0,0,0,0,0,1]],[[1,1,1,1,1,-1,-1,-1],[1,1,1,1,1,1,-1,-1],[1,1,1,1,-1,-1,1,-1],[1,1,1,1,1,-1,-1,-1],[0,0,1,1,1,-1,-1,-1],[0,0,1,1,1,-1,-1,0],[0,0,1,1,1,1,1,1],[0,0,0,0,0,0,1,1]],[[1,1,1,1,1,-1,-1,-1],[1,1,1,1,1,1,-1,-1],[1,1,1,1,-1,-1,1,-1],[1,1,1,1,-1,-1,-1,-1],[0,0,1,1,-1,-1,-1,-1],[0,0,1,1,-1,-1,-1,0],[0,0,1,1,-1,-1,1,1],[0,0,0,0,-1,0,1,1]],[[1,1,1,1,1,-1,-1,-1],[1,1,1,1,1,1,-1,-1],[1,1,1,1,1,-1,1,-1],[1,1,1,1,-1,1,-1,-1],[0,0,1,1,-1,-1,1,-1],[0,0,1,1,1,1,1,1],[0,0,1,1,-1,-1,1,1],[0,0,0,0,-1,0,1,1]],[[1,1,1,1,1,-1,-1,-1],[1,1,1,1,1,1,-1,-1],[1,1,1,1,1,-1,1,-1],[1,1,1,1,-1,1,-1,-1],[0,0,1,1,-1,-1,1,-1],[0,0,1,1,-1,1,1,1],[0,0,1,-1,-1,-1,1,1],[0,0,-1,0,-1,0,1,1]],[[1,1,1,1,1,-1,-1,-1],[1,1,1,1,1,1,-1,-1],[1,1,1,1,1,-1,1,-1],[1,1,1,1,-1,1,-1,-1],[0,0,1,1,-1,-1,1,-1],[0,0,1,1,-1,1,1,1],[0,0,1,1,1,-1,1,1],[0,0,-1,1,-1,0,1,1]],[[1,1,1,1,1,-1,-1,-1],[1,1,1,1,1,1,-1,-1],[1,1,1,1,1,-1,1,-1],[1,1,1,1,-1,1,-1,-1],[0,0,1,1,-1,-1,1,-1],[0,0,1,-1,-1,1,1,1],[0,0,-1,1,1,-1,1,1],[0,-1,-1,1,-1,0,1,1]],[[1,1,1,1,1,-1,-1,-1],[1,1,1,1,1,1,-1,-1],[1,1,1,1,1,-1,1,-1],[1,1,1,1,-1,1,-1,-1],[0,0,1,1,-1,-1,1,-1],[0,1,1,-1,-1,1,1,1],[0,0,1,1,1,-1,1,1],[0,-1,-1,1,-1,0,1,1]],[[1,1,1,1,1,-1,-1,-1],[1,1,1,1,1,1,-1,-1],[1,1,1,1,1,-1,1,-1],[1,1,1,1,-1,1,-1,-1],[0,0,1,1,-1,-1,1,-1],[0,1,1,-1,-1,1,1,1],[0,0,1,1,-1,-1,1,1],[0,-1,-1,1,-1,-1,1,1]],[[1,1,1,1,1,-1,-1,-1],[1,1,1,1,1,1,-1,-1],[1,1,1,1,1,-1,1,-1],[1,1,1,1,-1,1,-1,-1],[0,0,1,1,-1,-1,1,-1],[0,1,1,-1,-1,1,1,1],[0,0,1,1,-1,-1,1,1],[1,1,1,1,-1,-1,1,1]],[[1,1,1,1,1,-1,-1,-1],[1,1,1,1,1,1,-1,-1],[1,1,1,1,1,-1,1,-1],[1,1,1,1,-1,1,-1,-1],[0,0,1,1,-1,-1,1,-1],[-1,-1,-1,-1,-1,1,1,1],[0,0,1,1,-1,-1,1,1],[1,1,1,1,-1,-1,1,1]],[[1,1,1,1,1,-1,-1,-1],[1,1,1,1,1,1,-1,-1],[1,1,1,1,1,-1,1,-1],[1,1,1,1,-1,1,-1,-1],[1,0,1,1,-1,-1,1,-1],[-1,1,-1,-1,-1,1,1,1],[0,0,1,1,-1,-1,1,1],[1,1,1,1,-1,-1,1,1]],[[1,1,1,1,1,-1,-1,-1],[1,1,1,1,1,1,-1,-1],[1,1,1,1,1,-1,1,-1],[1,1,1,1,-1,1,-1,-1],[1,0,1,1,-1,-1,1,-1],[-1,1,-1,-1,-1,1,1,1],[0,-1,-1,-1,-1,-1,1,1],[1,1,1,1,-1,-1,1,1]],[[1,1,1,1,1,-1,-1,-1],[1,1,1,1,1,1,-1,-1],[1,1,1,1,1,-1,1,-1],[1,1,1,1,-1,1,-1,-1],[1,0,1,1,-1,-1,1,-1],[1,1,-1,-1,-1,1,1,1],[1,1,1,1,1,1,1,1],[1,1,1,1,-1,-1,1,1]],[[1,1,1,1,1,-1,-1,-1],[1,1,1,1,-1,1,-1,-1],[1,1,1,-1,1,-1,1,-1],[1,1,-1,1,-1,1,-1,-1],[1,-1,-1,-1,-1,-1,1,-1],[1,1,-1,-1,-1,1,1,1],[1,1,1,1,1,1,1,1],[1,1,1,1,-1,-1,1,1]]]
    log_cnt = 26
    print(np.array(log[log_cnt]))
    maxv = [0.3, 0.4, 0.5]
    max_env = global_env
    player = ai.AI(8, COLOR_WHITE, 1, maxv, max_env)
    chessboard = np.array(log[log_cnt])
    candidate_list = player.go(chessboard)
    print(candidate_list)
    # print(player.eval(player.color, candidate_list[-1], chessboard, candidate_list))
    # print(player.eval(player.color, (2, 0), chessboard, candidate_list))

def genetic_algorithm(population:list):
    for indiv in population:
        r = compete(indiv.variable, variable2=indiv.variable, type2=final)
        indiv.fitness += r
        if r > 0:
            print(indiv.id, 'new win!')
        elif r < 0:
            print(indiv.id, 'new lose!')
        else:
            print(indiv.id, 'draw!')
    for indiv in population:
        for _ in range(5):
            r_indiv = random.choice(population)
            r = compete(indiv.variable, r_indiv.variable, True)
            indiv.fitness += r
            r_indiv.fitness -= r
            if r > 0:
                print(indiv.id, r_indiv.id, 'win!')
            elif r < 0:
                print(indiv.id, r_indiv.id, 'lose!')
            else:
                print(indiv.id, r_indiv.id, 'draw!')
            print('player', indiv.id, 'fitness', indiv.fitness)
            print('player', r_indiv.id, 'fitness', r_indiv.fitness)
                
    def size(indiv):
        return indiv.fitness
    population.sort(key=size)
    for indiv in population:
        print(indiv.id, indiv.fitness, indiv.variable)
    return population

def mutate(population: list):
    def mate(indiv1, indiv2):
        return (indiv1.variable+indiv2.variable)/2
    def mut(variable:np.ndarray):
        v = np.copy(variable)
        v[0] += random.uniform(-0.01, 0.01)
        v[1] += random.uniform(-0.10, 0.10)
        v[2] += random.uniform(-0.25, 0.25)
        return v
    descs = []
    num = len(population)
    for _ in range(min(10, num // 2)):
        r1, r2 = None, None
        for _ in range(10):
            r1 = random.choice(population)
            r2 = random.choice(population)
            if abs(r1.fitness - r2.fitness) <= 5:
                break
        if r1 != None and r2 != None:
            r = Individual(count(), mate(r1, r2), (r1.fitness+r2.fitness)/2)
            descs.append(r)
    for indiv in population:
        v = indiv.variable
        v1 = normal(mut(v))
        v2 = normal(mut(v))
        descs.append(Individual(count(), v1, indiv.fitness))
        descs.append(Individual(count(), v2, indiv.fitness))
    return descs


def main(args):
    random.seed(a=None)
    if args.type == 'normal':
        fileName='note.txt'
        with open(fileName,'w',encoding='utf-8')as out:
            descendants = []
            population = []
            for i in range(10):
                indiv = Individual(count(), rand_array())
                population.append(indiv)
            descendants.append(population)
            while len(descendants) <= 5:
                population = genetic_algorithm(population)
                while len(population) > 20:
                    population.pop(0)
                print('remain %d species' % len(population), file=out)
                for indiv in population:
                    print(indiv.id, indiv.fitness, indiv.variable, file=out)
                population = mutate(population)
                print('generate %d children' % len(population), file=out)
                for indiv in population:
                    print(indiv.id, indiv.fitness, indiv.variable, file=out)
                descendants.append(population)
    elif args.type == 'test':
        test()
    elif args.type == 'climb':
        dict = {}
        # maxv = normal(np.random.randn(dim))
        maxv = [1.17239420e-05, 3.67396741e-01, 6.20597942e-01]
        # max_env = transform(np.random.randn(4,4)*10)
        max_env = [[500,-25,10,5,5,10,-25,500],
                    [-25,-45,1,1,1,1,-45,-25],
                    [10,1,3,2,2,3,1,10],
                    [5,1,2,1,1,2,1,5],
                    [5,1,2,1,1,2,1,5],
                    [10,1,3,2,2,3,1,10],
                    [-25,-45,1,1,1,1,-45,-25],
                    [500,-25,10,5,5,10,-25,500]]
        for i in range(3):
            for j in range(10):
                v = normal(np.random.randn(dim))
                player = ai.AI(8, COLOR_WHITE, 1, v, max_env)
                opponent = ai.AI(8, COLOR_BLACK, 1, maxv, max_env)
                r = twobattle(player, opponent)
                if r > 0:
                    maxv = v
                    print(v)
            # env = np.random.randn(4, 4)
            # print(env)
            # dict[player] += r
            # dict[opponent] -= r
            print("This is %d-th answer" % i)
            print("[", end="")
            for i in range(dim):
                print("%.2f" % maxv[i], end="")
                if i != 4:
                    print(", ", end="")
            print("]")
            print("[", end="")
            for i in range(8):
                print("[", end="")
                for j in range(8):
                    print("%.2f" % max_env[i][j], end="")
                    if j != 7:
                        print(", ", end="")
                print("]", end="")
                if i != 7:
                    print(",")
            print("]")

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        description='AI'
    )
    argparser.add_argument(
        '-t', '--type',
        default='normal',
    )

    args = argparser.parse_args()
    try:
        main(args)
    except KeyboardInterrupt:
        print('Cancelled by user. Bye!')