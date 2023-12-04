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
    
    agentTest = Plane
    
    def setUp(self):
        global agentTest
        agentTest = createAgent("toto")   
        agentTest.update()  

    def test_move(self):
        global agentTest
        agentX = agentTest.getX()
        agentY = agentTest.getY()
        print(f"X {agentX}  Y {agentY}")
        print(f"X {agentTest.getX()}  Y {agentTest.getY()}")
        
        agentTest.update()
        agentTest.move(1, 0)
        agentTest.update()
        print(f"X {agentX}  Y {agentY}")
        print(f"X {agentTest.getX()}  Y {agentTest.getY()}")
        sleep(3)
        print(f"X {agentX}  Y {agentY}")
        print(f"X {agentTest.getX()}  Y {agentTest.getY()}")
        
        self.assertEqual(agentTest.getX(), agentX + 1, "The agent should have moved to the right")
        self.assertEqual(agentTest.getY(), agentY + 1, "The agent should have moved to the bottom")
            
if __name__ == '__main__':
    unittest.main()

# agent = createAgent("toto")
# agent2 = createAgent("totoLeRetour")
# agent.update()
# agent2.update()
# i = 0

# while True:
#     agent.moveTowards(16,3)    
#     i += 1
#     agent2.moveTowards(16,4)    

#     sleep(1)
#     agent.update()
#     agent2.update()
    



