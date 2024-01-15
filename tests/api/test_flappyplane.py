import sys
sys.path.append('src/')
sys.path.append('src/api/')

import os
import unittest

from dotenv import load_dotenv
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

class TestFlappyPlane(unittest.TestCase):
    """
    Tests the Plane class from flappyplane
    """

    
    def setUp(self):
        """
        Set up the test environment before each test case.
        """
        self.agentTest = createAgent("tata")
        self.agentTest.update() 
        sleep(3)

    def testMove(self):
        """
        Test case for the move() method of the agent.

        This test verifies that the agent correctly updates its position after calling the move() method.
        It checks if the agent's X and Y coordinates are updated correctly after moving to the right and bottom.
        """
        
        agentX = self.agentTest.getX()
        agentY = self.agentTest.getY()   

        self.agentTest.move(0, 0)
        self.agentTest.update()
        
        self.assertEqual(self.agentTest.getX(), agentX - 1, "The agent should have moved to the right")
        self.assertEqual(self.agentTest.getY(), agentY - 1, "The agent should have moved to the bottom")

if __name__ == '__main__':
    unittest.main()



