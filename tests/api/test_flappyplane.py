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
        self.agentTest = createAgent("toto")  
        self.agentTest.update()  
        sleep(3)

    def testMove(self):
        agentX = self.agentTest.getX()
        agentY = self.agentTest.getY()
        print(f"X {agentX}  Y {agentY}")
        print(f"X {self.agentTest.getX()}  Y {self.agentTest.getY()}")
        
        self.agentTest.update()
        self.agentTest.move(1, 0)
        print(f"X {agentX}  Y {agentY}")
        print(f"X {self.agentTest.getX()}  Y {self.agentTest.getY()}")

        self.agentTest.update()
        sleep(3)
        print(f"X {agentX}  Y {agentY}")
        print(f"X {self.agentTest.getX()}  Y {self.agentTest.getY()}")
        
        self.assertEqual(self.agentTest.getX(), agentX + 1, "The agent should have moved to the right")
        self.assertEqual(self.agentTest.getY(), agentY + 1, "The agent should have moved to the bottom")
            
# if __name__ == '__main__':
#     unittest.main()

agent = createAgent("toto")
agent2 = createAgent("totoLeRetour")
agent.update()
agent2.update()
i = 0

while True:
    agent.move(-1,0)    
    i += 1
    agent2.move(-1,0)    

    agent.update()
    agent2.update()
    



