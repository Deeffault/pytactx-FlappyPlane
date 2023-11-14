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

class Plane(IPlane):
    def __init__(self, playerId:str or None=None, arena:str or None=None, username:str or None=None, password:str or None=None, server:str or None=None, port:int or None=None) -> None:
        self.__agent = pytactx.Agent(playerId, arena, username, password, server, port, verbosity=2)

    def update(self) -> None:
        self.__agent.update()

    def move(self, px, py) -> None:
        self.__agent.move(px, py)

    def getX(self) -> int:
        return self.__agent.x

    def getY(self) -> int:
        return self.__agent.y