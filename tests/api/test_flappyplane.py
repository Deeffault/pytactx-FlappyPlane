import sys
sys.path.append('src/')
sys.path.append('src/api/')

import os
import unittest

from dotenv import load_dotenv
from api.flappyplane import Plane


load_dotenv()

ARENA = os.getenv('__ARENA__')
USERNAME = os.getenv('__USERNAME__')
AGENT_PASSWORD = os.getenv('__AGENT_PASSWORD__')
SERVER = os.getenv('__SERVER__')
PORT = os.getenv('__PORT__')



def createAgent(playerId:str) -> Plane:
    """
    Creates a new plane
    """
    return Plane(playerId=playerId, 
                arena=ARENA, 
                username=USERNAME, 
                password=AGENT_PASSWORD, 
                server=SERVER,
                port=PORT,
                )

class TestFlappyPlane(unittest.TestCase):
    """
    Tests the Plane class from flappyplane
    """
    def setUp(self):
        self.agent = createAgent("agentTest")
        self.agent.update()

    def test_move(self):
        agentX = self.agent.getX()
        agentY = self.agent.getY()
        self.agent.move(1, 1)
        self.agent.update()
        self.assertEqual(self.agent.getX(), agentX + 1, "The agent should have moved to the right")
        self.assertEqual(self.agent.getY(), agentY + 1, "The agent should have moved to the bottom")

if __name__ == '__main__':
    unittest.main()


