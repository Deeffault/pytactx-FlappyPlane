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
        """
        Set up the test environment before each test case.
        """
        self.obstacleMove = TowerObstacle(16,4,2)
        
        self.agent = createAgent("tata")
        self.obstaclePush = TowerObstacle(16,4,2)
        
        
    def testMove(self):
        """
        Test case for the move() method for the obstacles of the server.
        
        This test verifies that the obstacles correctly update their position after calling the move() method.
        It checks if the obstacles coordinates are updated correctly after moving to the right and bottom.
        """
        obstacleX = self.obstacleMove.x
        
        self.obstacleMove.move()

        self.assertEqual(self.obstacleMove.x,obstacleX - 1, "The obstacle should have moved to the left")
        
    
    def testPushAgents(self):
        """
        Test case for the pushAgents() method for the obstacles of the server.
        
        This test verifies that the obstacles correctly push the agents after calling the pushAgents() method.
        It checks if the agents coordinates are updated correctly after being pushed.
        """
        agentX = self.agent.getX()
        agentY = self.agent.getY()
        
        self.obstaclePush.main
        
        
        
        self.assertEqual(self.agent.getX(),agentX - 1, "The agent should have moved to the left")
        self.assertEqual(self.agent.getY(),agentY, "The agent should not have moved")

if __name__ == '__main__':
    unittest.main()