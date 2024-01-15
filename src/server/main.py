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
from random import randint

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
    
    @classmethod
    def tick(cls):
        """
        Perform a game tick, updating the positions of obstacles and removing obstacles that are out of bounds.
        """
        obstacles_to_delete = []
        for obstacle in obstacles:
            obstacle.move()
            if obstacle.is_out_of_bound():
                obstacles_to_delete.append(obstacle)
            else:
                obstacle.push_agents()
        
        for obstacle in obstacles_to_delete:
            obstacles.remove(obstacle)
        
        if tick_count % 4 == 0:
            obstacles.append(TowerObstacle(COLUMNS, randint(0, ROWS - 2), 2))

class TowerObstacle(IObstacle):
    def __init__(self, x, y, z):
        """
        Initialize the Obstacle object.

        Args:
            x (int): The x-coordinate of the obstacle.
            y (int): The y-coordinate of the obstacle.
            z (int): The z-coordinate of the obstacle.
        """
        self.x = x
        self.y = y
        self.z = z
        self.agents_scored = []
        
    def move(self):
        """
        Moves the obstacle to the left by one unit.

        This method updates the obstacle's position on the map by decrementing the x-coordinate by 1.
        It also updates the map accordingly, clearing the previous position and updating the new position.

        Parameters:
        None

        Returns:
        None
        """
        global map
        if self.x >= 0 and self.x < COLUMNS:
            for i in range(ROWS):
                map[i][self.x] = 0
        self.x -= 1
        if self.x >= 0 and self.x < COLUMNS:
            for i in range(ROWS):
                if i >= self.y and i < self.y + self.z:
                    map[i][self.x] = 0
                elif i < self.y:
                    map[i][self.x] = 5 + min(i, 3) if self.y >= 4 else 5 + i + (4 - self.y)
                else:
                    map[i][self.x] = (min(ROWS - i - 1, 3) + 1) if ROWS - self.y - self.z >= 4 else (ROWS - i - 1 + (4 - ROWS + self.y + self.z) + 1)
        agent.ruleArena("map", map)
        
    def push_agents(self):
        """
        Pushes the agents in the same column as the obstacle or calculates their score.

        This method iterates through the agents and checks if they are in the same column as the obstacle.
        If they are, it either pushes them or calculates their score based on their position relative to the obstacle.
        It also removes agents that are no longer alive from the list of scored agents.
        """
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
                    scores[player] += 1
                    agent.rulePlayer(player, "score", scores[player])
                    self.agents_scored.append(player)

        scored_players_to_remove = []
        for player in self.agents_scored:
            if player not in agent.range:
                scored_players_to_remove.append(player)
        for player in scored_players_to_remove:
            self.agents_scored.remove(player)
    
    def is_out_of_bound(self):
            """
            Check if the object is out of bounds.

            Returns:
                bool: True if the object is out of bounds, False otherwise.
            """
            return self.x < 0

def push_agent(player):
    """
    Pushes the agent/player to the left by decreasing its x-coordinate.
    If the agent/player reaches the leftmost position (x=0), it is considered dead and its life is set to 0.
    If there is another agent/player in the adjacent left position, the push_agent function is recursively called for that agent/player.
    
    Parameters:
        player (str): The identifier of the agent/player to be pushed.
    """
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
    """
    Update the best scores and best players of all time and the current game.

    This function iterates through the players in the agent's range and updates the best alive score and player.
    It also updates the best score of all time and the best player of all time if the current best alive score is greater.
    Finally, it prints the information about the best scores and players.

    Parameters:
        None

    Returns:
        None
    """
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

def process_agents_move():
    """
    Process the moves of the agents.

    This function iterates over each player in the agent range and updates their position based on the LED values.
    If the player's life is less than or equal to 0, the player is skipped.
    If the LED values are not both 0, the player's position is updated accordingly.
    If the new position is out of bounds, the player is skipped.
    If the new position is valid (map[n_pos[1]][n_pos[0]] == 0), the player's x, y, and LED values are updated.
    """
    for player in agent.range:
        playerdata = agent.range[player]
        if playerdata['life'] > 0 and (playerdata['led'][0] not in (0, 2) or playerdata['led'][1] not in (0, 2)):
            n_pos = [playerdata['x'], playerdata['y']]
            if playerdata['led'][0] not in (0, 2):
                n_pos[0] += (1 if playerdata['led'][0] >= 2 else -1)
            if playerdata['led'][1] not in (0, 2):
                n_pos[1] += (1 if playerdata['led'][1] >= 2 else -1)
            if n_pos[0] < 0 or n_pos[0] >= COLUMNS or n_pos[1] < 0 or n_pos[1] >= ROWS:
                print('hit map borders')
                continue
            met_someone = False
            for player2 in agent.range:
                if player == player2:
                    continue
                playerdata2 = agent.range[player2]
                if playerdata2['x'] == n_pos[0] and playerdata2['y'] == n_pos[1]:
                    met_someone = True
                    break
            if met_someone:
                print('hit someone')
                continue
            if map[n_pos[1]][n_pos[0]] == 0:
                print(n_pos)
                agent.rulePlayer(player, "x", n_pos[0])
                agent.rulePlayer(player, "y", n_pos[1])
        agent.rulePlayer(player, "color", [0, 0, tick_count%100])

def process_agent_respawn():
    for player in agent.range:
        playerdata = agent.range[player]
        if playerdata['life'] <= 0:
            agent.rulePlayer(player, "life", 100)
            agent.rulePlayer(player, "x", 1)
            agent.rulePlayer(player, "y", 2)
            agent.rulePlayer(player, "dir", 2)

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

# Make players immobile
agent.ruleArena("dxMax", [0, 100, 0, 0, 0])
agent.ruleArena("dyMax", [0, 100, 0, 0, 0])

obstacles = []

scores = {}

# Agents actuellement dans l'arène
agents = []

def process_agent_spawn():
    """
    Spawn agents in the arena.

    This function spawns agents in the arena by setting their life to 100 and their x and y coordinates to 1 and 2 respectively.
    It also sets their direction to 2 (down) and their LED values to [0, 0, time.time()].

    Parameters:
        None

    Returns:
        None
    """
    global agents

    posX = 1
    posY = 2
    for agentId in agent.range.keys():
        if agentId in agents:
            continue
        
        agents.append(agentId)
        agent.rulePlayer(agentId, "life", 100)
        agent.rulePlayer(agentId, "x", posX)
        agent.rulePlayer(agentId, "y", posY)
        agent.rulePlayer(agentId, "dir", 2)
        agent.rulePlayer(agentId, "led", [0, 0, time.time()])
        posY+=2
    
    agents = agent.range.keys()

agent.setColor(255, 255, 0)

tick_count = 0
last_tick_time = time.time()
# Main loop


def main_loop():
    # Get the game state
    agent.update()
    time.sleep(.5)
    agent.update()
    
    IObstacle.tick()
    process_agents_move()
    update_best_scores()
    
    agent.moveTowards(0, 0)
    tick_count+=1


if __name__ == '__main__':
    while True:
        main_loop()