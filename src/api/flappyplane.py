import j2l.pytactx.agent as pytactx 
from abc import ABC, abstractmethod

class IPlane (ABC):
    @abstractmethod
    def update(self) -> None:
        """
        Sends the agent's caracteristics and his requests to the server
        """
        pass

    @abstractmethod
    def move(self, px, py) -> None:
        """
        Moves the plane according to the px,py parameters
        With px, py between -1 and 1
        Send the request to the server, and the server moves the plane
        """
        pass

    @abstractmethod
    def getX(self) -> int:
        """
        Returns the plane's x position
        """
        pass

    @abstractmethod
    def getY(self) -> int:
        """
        Returns the plane's y position
        """
        pass
    
    @abstractmethod
    def getMap(self) -> tuple[tuple[int]]:
        """
        Returns the arena's map
        """
        pass
    
class Plane(IPlane):
    def __init__(self, playerId:str or None=None, arena:str or None=None, username:str or None=None, password:str or None=None, server:str or None=None) -> None:
        self.__agent = pytactx.Agent(playerId, arena, username, password, server, verbosity=2)

    def update(self) -> None:
        self.__agent.update()

    def move(self, px, py) -> None:
        '''
        0 ne bouge pas
        1 recule
        2+ avance
        '''
        px //= abs(px)
        py //= abs(py)
        self.__agent.setColor(px+2, py+2 , 0)

    def getX(self) -> int:
        return self.__agent.x

    def getY(self) -> int:
        return self.__agent.y
    
    def getMap(self) -> tuple[tuple[int]]:
        return self.__agent.map

    
