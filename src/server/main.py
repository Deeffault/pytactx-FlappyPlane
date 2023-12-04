from dotenv import load_dotenv
import os

load_dotenv()

AGENT_PASSWORD = os.getenv('__AGENT_PASSWORD__')
SERVER = os.getenv('__SERVER__')
USERNAME = os.getenv('__USERNAME__')
ARENA = os.getenv('__ARENA__')
ARBITRE_USERNAME = os.getenv('__ARBITRE_USERNAME__')

import sys

sys.path.append("src/")

import api.j2l.pytactx.agent as pytactx
from abc import ABC, abstractmethod

# Create the agent
agent = pytactx.Agent(playerId=ARBITRE_USERNAME,
                      arena=ARENA,
                      username=USERNAME,
                      password=AGENT_PASSWORD,
                      server=SERVER,
                      verbosity=2)

class IObstacle(ABC):
    @abstractmethod
    def move(self):
        """moves the obstacle"""
        pass
    
    @abstractmethod
    def push_agents(self):
        """pushes the agents that are in the same cell as the obstacle"""
        pass
    
    @abstractmethod
    def is_out_of_bound(self):
        """returns whether the obstacle is out of bound or not so that it can be removed from the game"""
        pass
    
class TowerObstacle(IObstacle):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        
    def move(self):
        height_up = self.y
        height_down = ROWS - self.y - self.z
        
        global map
        #global mapFriction
        if self.x >= 0 and self.x < COLUMNS:
            for i in range(ROWS):
                map[i][self.x] = 0
                #mapFriction[i][self.x] = 0
        self.x -= 1
        if self.x >= 0 and self.x < COLUMNS:
            for i in range(ROWS):
                if i >= self.y and i < self.y + self.z:
                    map[i][self.x] = 0
                elif i < self.y:
                    map[i][self.x] = 5 + min(i, 3) if self.y >= 4 else 5 + i + (4 - self.y)
                else:
                    map[i][self.x] = (min(ROWS - i - 1, 3) + 1) if ROWS - self.y - self.z >= 4 else (ROWS - i - 1 + (4 - ROWS + self.y + self.z) + 1)
                #mapFriction[i][self.x] = 0 if i == self.y else 1
                
        agent.ruleArena("map", map)
        #agent.ruleArena("mapFriction", mapFriction)
    def push_agents(self):
        for player in agent.range:
            playerdata = agent.range[player]
            if playerdata['x'] == self.x and (playerdata['y'] < self.y or playerdata['y'] >= (self.y + self.z)):
                push_agent(player)
    
    def is_out_of_bound(self):
        return self.x < 0

def push_agent(player):
    playerdata = agent.range[player]
    if playerdata['x'] == 0:
        agent.rulePlayer(player, "life", 0)
    else:
        for player2 in agent.range:
            playerdata2 = agent.range[player2]
            if playerdata2['x'] == playerdata['x'] - 1 and playerdata2['y'] == playerdata['y']:
                push_agent(player2)
        agent.rulePlayer(player, "x", agent.range[player]['x'] - 1)

COLUMNS = 16
ROWS = 9

agent.ruleArena("gridColumns", COLUMNS)
agent.ruleArena("gridRows", ROWS)

# Map background
agent.ruleArena("bgImg", "https://cdn.discordapp.com/attachments/1173930308039610378/1173936773903175730/background.png")

# Max move box
agent.ruleArena("dxMax", COLUMNS)
agent.ruleArena("dyMax", ROWS)


# Map array
map = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
agent.ruleArena("map", map)

# Map collision array
mapFriction = [0, 1, 1, 1, 1, 1, 1, 1, 1]
agent.ruleArena("mapFriction", mapFriction)

# Map texture array
agent.ruleArena("mapImgs", [
    "",
    "https://cdn.discordapp.com/attachments/1173930308039610378/1173995601373970493/Tower_1.png",
    "https://cdn.discordapp.com/attachments/1173930308039610378/1173995601688547358/Tower_2.png",
    "https://cdn.discordapp.com/attachments/1173930308039610378/1173995602095374366/Tower_3.png",
    "https://cdn.discordapp.com/attachments/1173930308039610378/1173995602363826268/Tower_4.png",
    "https://cdn.discordapp.com/attachments/1173930308039610378/1174012156585451610/Reverse-Tower_1.png",
    "https://cdn.discordapp.com/attachments/1173930308039610378/1174012156820336740/Reverse-Tower_2.png",
    "https://cdn.discordapp.com/attachments/1173930308039610378/1174012157105553498/Reverse-Tower_3.png",
    "https://cdn.discordapp.com/attachments/1173930308039610378/1174012157491425361/Reverse-Tower_4.png"
])

# Player texture array
agent.ruleArena("pImgs", ["https://cdn.discordapp.com/attachments/1173930308039610378/1173931307613552661/Variant2.png"])

# Collision dmg
agent.ruleArena("hitCollision", [0])

obstacles = []

i = 0
# Main loop
while True:
    # Get the game state
    from time import sleep
    agent.update()
    sleep(1)
    agent.update()
    print([(obs.x, obs.y) for obs in obstacles])
    
    obstacles_to_delete = []
    for obstacle in obstacles:
        obstacle.move()
        if obstacle.is_out_of_bound():
            obstacles_to_delete.append(obstacle)
        else:
            obstacle.push_agents()
    
    for obstacle in obstacles_to_delete:
        obstacles.remove(obstacle)
    
    from random import randint
    if i % 4 == 0:
        obstacles.append(TowerObstacle(COLUMNS, randint(0, ROWS - 2), 2))
    
    agent.moveTowards(0, 0)
    i+=1
    
    if "toto" in agent.range:
        print("toto")
        print(agent.range["toto"]['x'])
        print(agent.range["toto"]['y'])
    