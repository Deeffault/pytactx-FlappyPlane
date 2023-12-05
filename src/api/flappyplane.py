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
            """
            Initializes a new instance of the FlappyPlane class.

            Args:
                playerId (str or None): The ID of the player. Defaults to None.
                arena (str or None): The name of the arena. Defaults to None.
                username (str or None): The username for authentication. Defaults to None.
                password (str or None): The password for authentication. Defaults to None.
                server (str or None): The server address. Defaults to None.
            """
            self.__agent = pytactx.Agent(playerId, arena, username, password, server, verbosity=2)

    def update(self) -> None:
        """
        Updates the state of the FlappyPlane game.

        This method is responsible for updating the agent's state and performing any necessary game logic.

        Returns:
            None
        """
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
            """
            Get the x-coordinate of the agent.

            Returns:
                int: The x-coordinate of the agent.
            """
            return self.__agent.x

    def getY(self) -> int:
            """
            Get the y-coordinate of the agent.

            Returns:
                int: The y-coordinate of the agent.
            """
            return self.__agent.y
    
    def getMap(self) -> tuple[tuple[int]]:
        """
        Returns the map of the FlappyPlane game.

        Returns:
            tuple[tuple[int]]: The map of the game, represented as a 2D tuple of integers.
        """
        return self.__agent.map

    
