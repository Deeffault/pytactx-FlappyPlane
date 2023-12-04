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
import time

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
        self.agents_scored = []
        
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
        # Calculate the score of the agents in the same column as the obstacle or push them
        for player in agent.range:
            playerdata = agent.range[player]
            if playerdata['x'] != self.x:
                continue
            if (playerdata['y'] < self.y or playerdata['y'] >= (self.y + self.z)):
                push_agent(player)
            else:
                if player not in self.agents_scored:
                    if player not in scores:
                        scores[player] = 0
                    print(f"{player}: {scores[player]} + 1")
                    scores[player] += 1
                    self.agents_scored.append(player)
        
        # Remove the agents that are not alive anymore
        scored_players_to_remove = []
        for player in self.agents_scored:
            if player not in agent.range:
                scored_players_to_remove.append(player)
        for player in scored_players_to_remove:
            self.agents_scored.remove(player)
    
    def is_out_of_bound(self):
        return self.x < 0

def push_agent(player):
    playerdata = agent.range[player]
    if playerdata['x'] == 0:
        agent.rulePlayer(player, "life", 0)
        del scores[player]
    else:
        for player2 in agent.range:
            playerdata2 = agent.range[player2]
            if playerdata2['x'] == playerdata['x'] - 1 and playerdata2['y'] == playerdata['y']:
                push_agent(player2)
        agent.rulePlayer(player, "x", agent.range[player]['x'] - 1)

best_player_of_all_time = ""
best_score_of_all_time = 0

best_alive_player = ""
best_alive_score = 0

def update_best_scores():
    global best_player_of_all_time
    global best_score_of_all_time
    global best_alive_player
    global best_alive_score

    best_alive_score = 0
    best_alive_player = ""
    for player in agent.range:
        if player not in scores:
            scores[player] = 0
        if scores[player] > best_alive_score:
            best_alive_score = scores[player]
            best_alive_player = player
    
    if best_alive_score > best_score_of_all_time:
        best_score_of_all_time = best_alive_score
        best_player_of_all_time = best_alive_player
    
    agent.ruleArena("info", f"| 🏆 Best score of all time: {best_score_of_all_time} by {best_player_of_all_time or '💀'} | 👑 Best score of the current game: {best_alive_score} by {best_alive_player or '💀'}")

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

# Map breakable array
agent.ruleArena("mapBreakable", [False for i in range(9)])

# Map breakable array
agent.ruleArena("mapHit", [0 for i in range(9)])

# Player texture array
agent.ruleArena("pImgs", ["https://cdn.discordapp.com/attachments/1173930308039610378/1173931307613552661/Variant2.png"])

# Disable Brownian Map
agent.ruleArena("brownianMap", False)

# Collision dmg
agent.ruleArena("hitCollision", [0, 0, 0, 0, 0])

# Disable score calculation using KD
agent.ruleArena("score", "")

obstacles = []

scores = {}

# Création d'agents actualisés par l'arène elle-même
agents = {
    "Théo" : 0,
    "Teiva": 0, 
    "Augustin": 0
}
   
posX = 1
posY = 2
for agentId in agents.keys():
    agent.rulePlayer(agentId, "life", 100)
    agent.rulePlayer(agentId, "x", posX)
    agent.rulePlayer(agentId, "y", posY)
    agent.rulePlayer(agentId, "dir", 2)
    posY+=2

agent.setColor(255, 255, 0)

from time import time
i = 0
last_tick_time = time()
# Main loop
while True:
    # Get the game state
    from time import sleep
    update_best_scores()
    #agent.update()
    #new_tick_time = time()
    #delta = new_tick_time - last_tick_time
    #sleep(max(0.25 - delta, 0))
    #print(delta)
    #last_tick_time = time()
    agent.update()
    #print([(obs.x, obs.y) for obs in obstacles])
    
    obstacles_to_delete = []
    for obstacle in obstacles:
        if not obstacle.is_out_of_bound():
            obstacle.push_agents()
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
            
    #for player in agent.range:
    #    pass
        
    
    # if "toto" in scores:
    #     print("toto")
    #     print(scores["toto"])
    
