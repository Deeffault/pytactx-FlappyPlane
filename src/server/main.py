import os
from dotenv import load_dotenv
load_dotenv()

__arena__ = os.getenv('__ARENA__')
__username__ = os.getenv('__USERNAME__')
__password__ = os.getenv('__AGENT_PASSWORD__')
__server__ = os.getenv('__SERVER__')
__playerId__ = os.getenv('__ARBITRE_USERNAME__')

import sys
import time
sys.path.append("src/")
import api.j2l.pytactx.agent as pytactx


arbitre = pytactx.Agent(playerId=__playerId__,
	arena=__arena__,
	username=__username__,
	password=__password__,
	server=__server__,
	verbosity=2)

# Création d'agents actualisés par l'arène elle-même
agents = {
    "Théo" : 0,
    "Teiva": 0, 
    "Augustin": 0
}
      
posX = 1
posY = arbitre.game['gridRows'] / 4
for agentId in agents.keys():
    arbitre.rulePlayer(agentId, "life", 100)
    arbitre.rulePlayer(agentId, "x", posX)
    arbitre.rulePlayer(agentId, "y", posY)
    arbitre.rulePlayer(agentId, "dir", 2)
    posY+=2

# Affichage dans l'arène du début de la partie par l'arbitre
arbitre.ruleArena("info", "🟢 C'est parti !")
arbitre.setColor(255, 255, 0)
arbitre.update()

while True:
    sizeGridRows = arbitre.game['gridRows']
    sizeGridColumns = arbitre.game['gridColumns']
        
    arbitre.lookAt((arbitre.dir + 1) % 4)
    arbitre.update()
    

