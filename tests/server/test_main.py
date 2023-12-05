import sys
sys.path.append('src/')
sys.path.append('src/server/')
sys.path.append('src/api/')

import os
import unittest

from dotenv import load_dotenv
from server.main import TowerObstacle
from api.flappyplane import Plane
from time import sleep

load_dotenv()

ARBITRE_USERNAME = os.getenv('__ARBITRE_USERNAME__')
ARENA = os.getenv('__ARENA__')
USERNAME = os.getenv('__USERNAME__')
AGENT_PASSWORD = os.getenv('__AGENT_PASSWORD__')
SERVER = os.getenv('__SERVER__')




def createAgent(name) -> Plane:
    """
    Creates a new plane
    """
    return Plane(playerId=name, 
                arena=ARENA, 
                username=USERNAME, 
                password=AGENT_PASSWORD, 
                server=SERVER
                )

class TestTowerObstacle(unittest.TestCase):
    """
    Tests the Plane class from flappyplane
    """

    def setUp(self):
        self.agent = createAgent("07012003")  
        self.agentTest = createAgent("toto")
        self.agent.update()  
        self.agentTest.update
        sleep(3)
        
    def testMove(self):
        pass
    
    def testPushAgents(self):
        pass
    
    def testPushAgent(self, agent):
        pass
    
    def testScoreboard(self):
        pass
    


if __name__ == '__main__':
    unittest.main()