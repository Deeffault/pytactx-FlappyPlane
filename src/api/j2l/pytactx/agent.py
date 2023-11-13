# -*- coding: utf-8 -*-
#                           ██╗██████╗ ██╗           
#                           ██║╚════██╗██║           
#                           ██║ █████╔╝██║           
#                      ██   ██║██╔═══╝ ██║           
#                      ╚█████╔╝███████╗███████╗      
#                       ╚════╝ ╚══════╝╚══════╝      
#                       https://jusdeliens.com
#
# Designed with 💖 by Jusdeliens
# Under CC BY-NC-ND 3.0 licence 
# https://creativecommons.org/licenses/by-nc-nd/3.0/ 
__version__ = '1.0.0'

# Allow import without error 
# "relative import with no known parent package"
# In vscode, add .env file with PYTHONPATH="..." 
# with the same dir to allow intellisense
import os
import sys
__workdir__ = os.path.dirname(os.path.abspath(__file__))
__libdir__ = os.path.dirname(__workdir__)
sys.path.append(__libdir__)

from pyrobotx.robot import IRobot
import pyrobotx.client as rbx
import pyanalytx.logger as anx
from typing import Any, Callable
import copy
import traceback
import codecs
import time
import json
import base64
from datetime import datetime 
from random import randint
from threading import Timer
import inspect

class IAgentFr:
    def __init__(self):
        self.idClient : str = ""
        self.idJoueur : str = ""
        self.idRobot : str = ""
        self.equipe : int = 0
        self.profile : int = 0
        self.dtCreation : int = 0
        self.x : int = 0
        self.y : int = 0
        self.orientation : int = 0
        self.pose : tuple[int,int,int] = (0,0,0)
        self.vie : int = 100
        self.munitions : int = 10
        self.distance : int = 0
        self.couleur : tuple[int,int,int] = (0,255,0)
        self.infoJoueur = ""
        self.voisins : dict[str,Any] = {}
        self.score : int = 0
        self.classement : int = 0
        self.nTirs : int = 0
        self.nCollisions : int = 0
        self.nTirsRecus : int = 0
        self.nDeplacements : int = 0
        self.nMorts : int = 0
        self.nTues : int = 0
        self.nExecutions : int = 0
        self.jeu : dict[str,Any] = {}
        self.agents : list[str] = []
        self.robots : list[str] = []
        self.carte : tuple[tuple[int]] = []
        self.infoArene = ""
        self.jeuEnPause : bool = False
        self.tailleGrilleColonnes : int = 10
        self.tailleGrilleLignes : int = 10
        self.robot : IRobot = None
    def connecter(self) -> bool :
        """
        Connecte l'agent dans l'arene.
        Doit etre appele une seul fois apres la creation de l'agent
        """
        ...
    def disconnect(self) -> None :
        """
        Deconnecter l'agent de l'arene
        """
        ...
    def robotEstConnecte(self) -> bool :
        """
        Renvoie si oui ou non l'agent a un robot associe connecte
        """
        ...
    def areneEstConnecte(self) -> bool :
        """
        Renvoie si oui ou non l'agent est connecte a l'arene
        """
        ...
    def actualiser(self) -> None:
        """
        Recupere du serveur et met a jour l'etat de l'agent  
        Et envoie toutes les demandes en attentes au serveur
        """
        ...
    def tirer(self, gachette:bool=True, trajectoire:Callable[[int],int] or None=None) -> None:
        """
        Demander d'appuyer sur la gachette pour tirer en gachette (gachette=True)
        ou bien de relacher la gachette (gachette=False)
        La requete sera envoyee au prochain actualiser()
        """
        ...
    def deplacer(self,dx:int,dy:int) -> None:
        """
        Demander un deplacement relatif sur la grille autour de la derniere 
        position de l'agent selon les valeurs de dx dy
        La requete sera envoyee au prochain actualiser()
        """
        ...
    def deplacerVers(self,x:int,y:int) -> None:
        """
        Demander un deplacement unitaire vers la position en x,y absolute sur la grille
        La requete sera envoyee au prochain actualiser()
        """
        ...
    def orienter(self,dir:int) -> None:
        """
        Demander une rotation de l'agent sur la grille
        La valeur de dir doit etre entiere de 0 (est) a 3 (sud).
        La requete sera envoyee au prochain actualiser()
        """
    def changerArene(self,nomAttribut:str,valeurAttribut:Any) -> None:
        """
        Demander un changement de l'etat de l'arene
        La requete sera envoyee au prochain actualiser()
        """
        ...
    def changerJoueur(self,agentId:str, nomAttribut:str, valeurAttribut:Any) -> None:
        """
        Demander un changement de l'etat d'un joueur dans l'arene
        La requete sera envoyee au prochain actualiser()
        """
        ...
    def changerCouleur(self, r:int, g:int, b:int) -> None:
        """
        Demander un changement de la couleur avec un code rouge vert blue de 1 octet chacun
        La requete sera envoyee au prochain actualiser()
        """
        ...
    def sabonner(self,evenement:str, callback:Callable[[Any,str,Any,Any], None]) -> None:
        """
        S'abonne au changement d'un attribut de l'agent (evenement)
        Quand l'evenement surviendra, la callback specifiee sera appelee
        """
        ...
    def afficher(self) -> None:
        """
        Affiche l'etat actuel de l'agent dans la console
        """
        ...

class IAgent:
    def __init__(self):
        self.clientId : str = ""
        self.playerId : str = ""
        self.robotId : str = ""
        self.team : int = 0
        self.profile : int = 0
        self.x : int = 0
        self.y : int = 0
        self.dir : int = 0
        self.pose : tuple[int,int,int] = (0,0,0)
        self.dtCreated : int = 0
        self.life : int = 100
        self.ammo : int = 10
        self.isFiring : bool = False
        self.distance : int = 0
        self.color : tuple[int,int,int] = (0,255,0)
        self.infoPlayer = ""
        self.range : dict[str,Any] = {}
        self.score : int = 0
        self.rank : int = 0
        self.nFire : int = 0
        self.nHitFire : int = 0
        self.nCollision : int = 0
        self.nMove : int = 0
        self.nDeath : int = 0
        self.nKill : int = 0
        self.nExe : int = 0
        self.game : dict[str,Any] = {}
        self.players : list[str] = []
        self.robots : list[str] = []
        self.map : tuple[tuple[int]] = []
        self.infoArena = ""
        self.isGamePaused : bool = False
        self.gridColumns : int = 10
        self.gridRows : int = 10
        self.robot : IRobot = None
    def connect(self) -> bool :
        """
        Connect the client to the broker.
        Should be called once just after the __init__
        """
        ...
    def disconnect(self) -> None :
        """
        Disconnect the client from the broker.
        """
        ...
    def isConnectedToRobot(self) -> bool :
        """
        Returns whether the client is connected to the robot or not.
        """
        ...
    def isConnectedToArena(self) -> bool :
        """
        Returns whether the client is connected to the arena or not.
        """
        ...
    def update(self) -> None :
        """
        Fetch the last values of robot sensors from server
        And send buffered requests in one shot to limit bandwidth.
        To be call in the main loop at least every 10 msecs.
        """
        ...
    def fire(self,enable:bool=True, firepath:Callable[[int],int] or None=None) -> None:
        """
        Request a trigger pull lock (enable=True) or a fire hold (enable=False)
        The request will be send the next update() call
        """
        ...
    def move(self,dx:int,dy:int) -> None:
        """
        Request a relative moves on the grid around the previous agent position 
        according to the specified dx, dy values.
        The request will be send the next update() call
        """
        ...
    def moveTowards(self,x:int,y:int) -> None:
        """
        Request a one step move towards the specified x,y absolute direction on the grid.
        The request will be send the next update() call
        """
        ...
    def lookAt(self,dir:int) -> None:
        """
        Request a rotation of the agent on the grid.
        Dir should be integers values from 0 (east) to 3 (south).
        The request will be send the next update() call
        """
        ...
    def ruleArena(self, attributeName:str, attributeValue:Any) -> None:
        """
        Request a change of the arena state
        The request will be send the next update() call
        """
        ...
    def rulePlayer(self, agentId:str, attributeName:str, attributeValue:Any) -> None:
        """
        Request a change of a player state
        The request will be send the next update() call
        """
        ...
    def setColor(self, r:int, g:int, b:int) -> None:
        """
        Request a color change for the robot led
        The request will be send the next update() call
        """
        ...
    def addEventListener(self,attributeName:str, callback:Callable[[Any,str,Any,Any], None]) -> None:
        """
        Subscribe to attribute value change event to call the specified callback
        as soon as a change occurs on the specified attribute
        """
        ...
    def _onRobotIdChanged(self, valueBefore:int, valueAfter:int):
        """To be overidden"""
        ...
    def _onXChanged(self, valueBefore:int, valueAfter:int):
        """To be overidden"""
        ...
    def _onYChanged(self, valueBefore:int, valueAfter:int):
        """To be overidden"""
        ...
    def _onDirChanged(self, valueBefore:int, valueAfter:int):
        """To be overidden"""
        ...
    def _onAmmoChanged(self, valueBefore:int, valueAfter:int):
        """To be overidden"""
        ...
    def _onLifeChanged(self, valueBefore:int, valueAfter:int):
        """To be overidden"""
        ...
    def _onDistanceChanged(self, valueBefore:int, valueAfter:int):
        """To be overidden"""
        ...
    def _onRangeChanged(self, valueBefore:dict[str,Any], valueAfter:dict[str,Any]):
        """To be overidden"""
        ...
    def _onDead(self, valueBefore:int, valueAfter:int):
        """To be overidden"""
        ...
    def _onKill(self, valueBefore:int, valueAfter:int):
        """To be overidden"""
        ...
    def _onMove(self, valueBefore:int, valueAfter:int):
        """To be overidden"""
        ...
    def _onPublicMessageReceived(self, valueBefore:str, valueAfter:str):
        """To be overidden"""
        ...
    def _onPrivateMessageReceived(self, valueBefore:str, valueAfter:str):
        """To be overidden"""
        ...
    def _onPlayerNumberChanged(self, valueBefore:list[str], valueAfter:list[str]):
        """To be overidden"""
        ...
    def _onRobotNumberChanged(self, valueBefore:list[str], valueAfter:list[str]):
        """To be overidden"""
        ...
    def _onGamePauseChanged(self, valueBefore:bool, valueAfter:bool):
        """To be overidden"""
        ...
    def _onGridColumnsChanged(self, valueBefore:int, valueAfter:int):
        """To be overidden"""
        ...
    def _onGridRowsChanged(self, valueBefore:int, valueAfter:int):
        """To be overidden"""
        ...

def exploreSourcesDirs(rootpath, subdirs=[], takeOnlyExts=['.py','.json'], dontTakeExts=[], dontTakeFolders=["venv", "j2l"], takeHidden=False, recursive=True, explored={}):
    dirpath = os.path.join(rootpath, *subdirs)
    filenames = os.listdir(dirpath)
    for filefullname in filenames:
        filefullpath = os.path.join(dirpath, filefullname)
        filename, fileext = os.path.splitext(filefullname)
        if ( fileext in dontTakeExts ):
            continue # Not blacklist exts
        if ( len(fileext) > 0 and len(takeOnlyExts) > 0 and fileext not in takeOnlyExts ):
            continue # Only whitelist exts
        if ( recursive == False and len(fileext) == 0 ):
            continue # Recursive folder
        if ( len(filename) >= 2 and filename[0] == "." and filename[1] != "." and takeHidden == False):
            continue # No hidden folder
        if ( filename in dontTakeFolders and len(fileext) == 0 ):
            continue # No env folder
        if ( len(filename) >= 2 and filename[0] == "_" and filename[1] == "_" and takeHidden == False):
            continue # No hidden folder
        if ( len(fileext) == 0 ): # Recursive folder explore
            subdirsRecursive = subdirs.copy()
            subdirsRecursive.append(filefullname)
            exploreSourcesDirs(rootpath, subdirsRecursive, takeOnlyExts, dontTakeExts, dontTakeFolders, takeHidden, recursive, explored)
        else:
            with open(filefullpath, "r", encoding="utf-8") as src:
                explored[filefullpath.replace(rootpath, "")] = (
                    subdirs,
                    filename, fileext, 
                    os.path.getctime(filefullpath), 
                    os.path.getmtime(filefullpath), 
                    (base64.b64encode(src.read().encode('utf-8'))).decode('utf-8')
                )
    return explored

def fetchSources(dirpath=None):
    if ( dirpath == None ):
        dirpath = __workdir__
    # Find main.py
    depth, maxdepth = 0,3
    while depth < maxdepth:
        filenames = os.listdir(dirpath)
        if ( "main.py" in filenames ):
            break
        depth += 1
        dirpath = os.path.join(dirpath, "..")
    if ( depth == maxdepth ):
        anx.debug("main.py not found")
        return None
    anx.debug("Found main.py from agent.py at depth "+str(-depth))
    # Explorer all folders from main.py
    srcs = exploreSourcesDirs(dirpath)
    return srcs

class Agent(IAgent):
    def __init__(self,playerId:str or None=None, arena:str or None=None, username:str or None=None, password:str or None=None, server:str or None=None, port:int=1883, imgOutputPath:str or None="img.jpeg", autoconnect:bool=True, useProxy:bool=True, verbosity:int=3, robotId:str or None="_", welcomePrint:bool=True, sourcesdir:str or None=None):
        while ( playerId == None or len(playerId) > 32 or len(playerId) == 0 ):
            playerId=input("👾 id (< 12 characters): ")
        while ( server == None or len(server) == 0 ):
            server=input("🌐 url: ")
            port=int(input("📫 port: "))
        if ( arena == None ):
            arena=input("🎲 arena: ")
        if ( username == None ):
            username=input("🧑 username: ")
        if ( password == None ):
            password=input("🔑 password: ")

        if ( welcomePrint ):
            passwordParam = (base64.b64encode(password.encode('utf-8'))).decode('utf-8')
            print("Hi there 👋")
            print("To see the arena in your web browser 🎮, go to 👉 https://play.jusdeliens.com/?viewer=pytactx&arena="+str(arena)+"&url="+str(server)+"&usr="+str(username)+"&pseudo="+str(playerId))
            print("To learn more about how to dev your agent 💡, go to 👉 https://tutos.jusdeliens.com")
            print("To join next robots fights ⚔️, Follow the link 👉 https://jusdeliens.com")
        if ( sourcesdir == None ):
            callerstack = (inspect.stack()[1])
            sourcesdir = os.path.dirname(os.path.abspath(callerstack[1]))

        IAgent.__init__(self)
        self.__sourcesDir : str or None = sourcesdir
        self.__firstArenaRx : bool = False
        self.__playerReqBuf : dict[str,Any] = {}
        self.__firepath : Callable[[int],int] or None = None
        self.__playerKeyToAttribute = {
            "clientId": ("clientId", None),
            "playerId": ("playerId", None),
            "robotId": ("robotId", Agent._onRobotIdChanged),
            "team": ("team", None),
            "profile": ("profile", None),
            "dtCreated": ("dtCreated", None),
            "x": ("x", Agent._onXChanged),
            "y": ("y", Agent._onYChanged),
            "dir": ("dir", Agent._onDirChanged),
            "ammo": ("ammo", Agent._onAmmoChanged),
            "life": ("life", Agent._onLifeChanged),
            "d": ("distance", Agent._onDistanceChanged),
            "range": ("range", Agent._onRangeChanged),
            "fire": ("isFiring", None),
            "led": ("color", None),
            "info": ("infoPlayer", Agent._onPrivateMessageReceived),
            "score": ("score", None),
            "rank": ("rank", None),
            "nFire": ("nFire", None),
            "nHit": ("nHitFire", None),
            "nCollision": ("nCollision", None),
            "nMove": ("nMove", Agent._onMove),
            "nKill": ("nKill", Agent._onKill),
            "nExe": ("nExe", None),
            "nDeath": ("nDeath", Agent._onDead),
        }
        self.__gameKeyToAttribute = {
            "players": ("players", Agent._onPlayerNumberChanged),
            "robots": ("robots", Agent._onRobotNumberChanged),
            "map": ("map", None),
            "info": ("infoArena", Agent._onPublicMessageReceived),
            "gridColumns": ("gridColumns", Agent._onGridColumnsChanged),
            "gridRows": ("gridRows", Agent._onGridRowsChanged),
            "pause": ("isGamePaused", Agent._onGamePauseChanged),
        }
        self.__onAttributeChangeCallbacks : dict[str, Callable[[Agent,str,Any,Any], None]]= {}
        for attribute in self.__playerKeyToAttribute.values():
            self.__onAttributeChangeCallbacks[attribute[0]] = []
        self.robot : IRobot = rbx.OvaClientMqtt(robotId,arena,username,password,server,port,imgOutputPath,autoconnect,useProxy,verbosity,playerId,False)
        self.robot.addEventListener(rbx.RobotEvent.updated, self._onUpdated)
        self.robot.addEventListener(rbx.RobotEvent.robotConnected, self._onRobotConnected)
        self.robot.addEventListener(rbx.RobotEvent.playerChanged, self._onPlayerChanged)
        self.robot.addEventListener(rbx.RobotEvent.arenaChanged, self._onArenaChanged)

    def connect(self) -> bool :
        return self.robot.connect()
    def disconnect(self) -> None :
        self.robot.disconnect()
    def isConnectedToRobot(self) -> bool :
        return self.robot.isConnectedToRobot()
    def isConnectedToArena(self) -> bool :
        return self.robot.isConnectedToArena()
    def update(self,enableSleep=True) -> None :
        self.robot.update(enableSleep)
    
    def fire(self,enable:bool=True, firepath:Callable[[int],int] or None=None) -> None:
        if ( type(enable) is not bool ):
            anx.warning("⚠️ fire enable value must be bool !")
            return
        self.__firepath = firepath
        self.__playerReqBuf['fire'] = enable
        
    def move(self,dx:int,dy:int) -> None:
        if ( type(dx) is not int or type(dy) is not int ):
            anx.warning("⚠️ move dx,dy values must be integer !")
            return
        if ( dx == 0 and dy == 0 ):
            return
        self.__playerReqBuf['dx'] = dx
        self.__playerReqBuf['dy'] = dy

    def moveTowards(self,x:int,y:int) -> None:
        if ( type(x) is not int or type(y) is not int ):
            anx.warning("⚠️ moveTowards x,y values must be integer !")
            return
        if ( x < 0 or y < 0 ):
            anx.warning("⚠️ moveTowards x,y values must be postive !")
            return
        if ( x == self.x and y == self.y ):
            return
        self.__playerReqBuf['x'] = x
        self.__playerReqBuf['y'] = y

    def lookAt(self,dir:int) -> None:
        if ( type(dir) is not int ):
            anx.warning("⚠️ lookAt dir value must be integer !")
            return
        if ( dir < 0 or dir > 3 ):
            anx.warning("⚠️ lookAt dir value must be included in [0;3] !")
            return
        self.__playerReqBuf['dir'] = dir

    def ruleArena(self, attributeName:str, attributeValue:Any) -> None:
        if ( type(attributeName) is not str ):
            anx.warning("⚠️ ruleArena attributeName value must be str !")
            return
        if ( 'ruleArena' not in self.__playerReqBuf ):
            self.__playerReqBuf['ruleArena'] = {}
        self.__playerReqBuf['ruleArena'][attributeName] = attributeValue

    def rulePlayer(self, agentId:str, attributeName:str, attributeValue:Any) -> None:
        if ( type(agentId) is not str ):
            anx.warning("⚠️ rulePlayer agentId value must be str !")
            return
        if ( type(attributeName) is not str ):
            anx.warning("⚠️ rulePlayer attributeName value must be str !")
            return
        if ( agentId == None ):
            agentId = self.id
        if ( 'rulePlayer' not in self.__playerReqBuf ):
            self.__playerReqBuf['rulePlayer'] = {}
        if ( agentId not in self.__playerReqBuf['rulePlayer'] ):
            self.__playerReqBuf['rulePlayer'][agentId] = {}
        self.__playerReqBuf['rulePlayer'][agentId][attributeName] = attributeValue

    def setColor(self, r:int, g:int, b:int) -> None:
        if ( type(r) is not int or type(g) is not int or type(b) is not int ):
            anx.warning("⚠️ setColor r,g,b values must be integer !")
            return
        if ( r<0 or r>255 or g<0 or g>255 or b<0 or b>255 ):
            anx.warning("⚠️ setColor r,g,b values must be included in [0;255] !")
            return
        if ( r == self.color[0] and g == self.color[1] and b == self.color[2] ):
            return
        self.__playerReqBuf['led'] = [r,g,b]

    def addEventListener(self,attributeName:str, callback:Callable[[Any,str,Any,Any], None]) -> None:
        if ( attributeName not in self.__onAttributeChangeCallbacks ):
            anx.warning("⚠️ Cannot add event listener for attribute "+attributeName)
            anx.warning("⚠️ Can only add event on "+str(self.__onAttributeChangeCallbacks.keys()))
            return
        self.__onAttributeChangeCallbacks[attributeName].append(callback)

    def print(self):
        self.robot.print()
        print("👾  Name : "+str(self.playerId))
        print("🧭  Pose : "+str(self.x)+","+str(self.y)+","+str(self.dir))
        print("📏 Distance: "+str(self.distance))
        print("🔫 Ammo: "+str(self.ammo))
        print("❤️  Life: "+str(self.life))
        print("🎨 Color: 🔴"+str(self.color[0])+" 🟢"+str(self.color[1])+" 🔵"+str(self.color[2]))
        print("🔍 Range: "+str(self.range))
        print()

    def _onRobotIdChanged(self, valueBefore:int, valueAfter:int):
        self.robot.changeRobot(valueAfter, True)

    def _onUpdated(self, eventSrc:Any, eventName:str, eventValue:Any):
        if ( self.__firstArenaRx != None and self.__firstArenaRx == True ):
            self.__firstArenaRx = None
            self.robot.requestPlayer("nExe", fetchSources(self.__sourcesDir))
        if ( 'fire' in self.__playerReqBuf and self.__firepath != None ):
            x = self.x
            y = self.y
            gridDim = max((self.gridColumns, self.gridRows))
            t = 0
            pts = []
            while ( x >= 0 and x < self.gridColumns and y >= 0 and y < self.gridRows and t < gridDim): 
                if ( self.dir == 0 ):
                    fx = self.y - int(round(self.__firepath(x-self.x)))
                    n = len(pts)
                    for yfx in range(y-1, fx-1, -1):
                        pts.append((x,yfx))
                    if ( n == len(pts) ):
                        pts.append((x,y))
                    y = fx
                    x = x+1
                elif ( self.dir == 1 ):
                    fx = self.x - int(round(self.__firepath(self.y-y)))
                    n = len(pts)
                    for xfx in range(x-1, fx-1, -1):
                        pts.append((xfx,y))
                    if ( n == len(pts) ):
                        pts.append((x,y))
                    x = fx
                    y = y-1
                elif ( self.dir == 2 ):
                    fx = self.y + int(round(self.__firepath(self.x-x)))
                    n = len(pts)
                    for yfx in range(y+1, fx+1, 1):
                        pts.append((x,yfx))
                    if ( n == len(pts) ):
                        pts.append((x,y))
                    y = fx
                    x = x-1
                elif ( self.dir == 3 ):
                    fx = self.x + int(round(self.__firepath(y-self.y)))
                    n = len(pts)
                    for xfx in range(x+1, fx+1, 1):
                        pts.append((xfx,y))
                    if ( n == len(pts) ):
                        pts.append((x,y))
                    x = fx
                    y = y+1
                else:
                    break
                t = t+1
            anx.debug("Firing: "+str(pts))    
            self.__playerReqBuf['fire'] = pts        
        for requestKey, requestValue in self.__playerReqBuf.items():
            self.robot.requestPlayer(requestKey, requestValue)
        self.__playerReqBuf = {}

    def __afterRobotConnected(self):
        self.robot.setMotorSpeed(0,0)

    def _onRobotConnected(self, eventSrc:Any, eventName:str, playerState: dict[str, Any]) -> None:
        Timer(2, self.__afterRobotConnected).start()
        self.robot.setLedFade(64,128,255,700,4)
        self.robot.playMelody([('E4',30),('G4',30),('C5',30),('G4',30),('C5',30),('E5',30),('C5',30),('E5',30),('G5',30),('C6',30)])
        self.robot.setMotorSpeed(20,20)

    def _onPlayerChanged(self, eventSrc:Any, eventName:str, playerState: dict[str, Any]) -> None:
        for playerKey, playerValue in playerState.items():
            if ( playerKey not in self.__playerKeyToAttribute ):
                continue
            attributeName = self.__playerKeyToAttribute[playerKey][0]
            attributeValueBefore = copy.deepcopy(self.__dict__[attributeName])
            if ( attributeValueBefore == playerValue ):
                continue
            self.__dict__[attributeName] = copy.deepcopy(playerValue)
            anx.debug("♟️ Player attribute "+attributeName+" changed from "+str(attributeValueBefore)+" to "+str(self.__dict__[attributeName]))
            attributeClassCallback = self.__playerKeyToAttribute[playerKey][1]
            onChangeCallbacks = self.__onAttributeChangeCallbacks[attributeName]
            if ( attributeClassCallback != None ):
                attributeClassCallback(self, attributeValueBefore, self.__dict__[attributeName])
            for callback in onChangeCallbacks:
                callback(self, attributeName, attributeValueBefore, self.__dict__[attributeName])
    
    def _onArenaChanged(self, eventSrc:Any, eventName:str, arenaState:dict[str,Any]) -> None:
        if ( self.__firstArenaRx == False ):
            self.__firstArenaRx = True
        for gameKey, gameValue in arenaState.items():
            self.game[gameKey] = gameValue
            if ( gameKey not in self.__gameKeyToAttribute ):
                continue
            attributeName = self.__gameKeyToAttribute[gameKey][0]
            attributeValueBefore = copy.deepcopy(self.__dict__[attributeName])
            if ( attributeValueBefore == gameValue ):
                continue
            self.__dict__[attributeName] = copy.deepcopy(gameValue)
            anx.debug("🎲 Game attribute "+attributeName+" changed from "+str(attributeValueBefore)+" to "+str(self.__dict__[attributeName]))
            attributeClassCallback = self.__gameKeyToAttribute[gameKey][1]
            if ( attributeClassCallback != None ):
                attributeClassCallback(self, attributeValueBefore, self.__dict__[attributeName])
        
    def __run__(filepath:str="settings.json", agentInfos=None):
        """
        Launch agents from json file
        settings.json file describing the agents credentials ... with at least the following keys: 
        |_ 'lib':              A list of str of the name of lib directories dependencies. Do not include '' in the name of the lib.
        |_ 'logDir' :          The dirname of the dir that will include log files. Do not include abs path, only dir name.
        |_ 'restartOnExcept' : To enable auto retart when an exception is raised
        |_ 'verbosity' :       An integer to set the verbosity of the arena logs, from 0 (no log), to 4 (all)
        |_ 'playerId' :        The name of the agent
        |_ 'robotId' :         The name of the robot
        |_ 'factoryFolder' :   The folder in which an .py script describes the Arena class to instanciate
        |_ 'factoryFile' :     The .py script describing the Arena class to instanciate
        |_ 'factoryClass' :    The Arena class name to instanciate
        |_ 'username' :        To log in the mqtt broker
        |_ 'password' :        To log in the mqtt broker
        |_ 'brokerAddress' :   As url or ip address without including the protocol
        |_ 'brokerPort' : 	   To connect to mqtt broker on the specified brokerAddress
        """
        restartOnExcept = True
        agentInfos = {}
        anx.setVerbosity(anx.Verbosity.INFO)
        anx.info("⏳ Loading agent infos from "+str(filepath))
        try:
            with codecs.open(filepath, "r", "utf-8-sig") as file:
                content = file.read()
                agentInfos = json.loads(content)
                anx.info("⏳ Loading agent infos: "+str(agentInfos))
                file.close()
        except Exception as e:
            anx.error("❌ FAIL loading "+filepath+" : "+str(e))
            anx.error(traceback.format_exc())
        restartOnExcept = False
        if ( "restartOnExcept" in agentInfos ):
            restartOnExcept = agentInfos["restartOnExcept"]
        anx.setLogger(anx.FileLogger(
            anx.Verbosity.WARNING, 
            os.path.join(agentInfos["logDir"],agentInfos["arena"]+"_"+agentInfos["id"]+str(datetime.now()).replace(" ","_").replace(":","-")+".log"))
        )
        agentConstructor = getattr(
            getattr(
                __import__(agentInfos["factoryDir"], fromlist=[agentInfos["factoryFile"]]), 
                agentInfos["factoryFile"]
            ),
            agentInfos["factoryClass"]
        )
        anx.info("⏳ Agent "+str(agentInfos["playerId"])+" starting on "+str(agentInfos["brokerAddress"])+" with username "+str(agentInfos["username"]))
        agent = agentConstructor(
            playerId=agentInfos["playerId"],
            arena=agentInfos["arena"], 
            username=agentInfos["username"], 
            password=agentInfos["password"], 
            server=agentInfos["brokerAddress"], 
            port=agentInfos["brokerPort"], 
            verbosity=agentInfos["verbosity"],
            robotId=agentInfos["robotId"]
        )
        if ( restartOnExcept ):
            try:
                while True:
                    agent.update()
            except Exception as e:
                anx.error("🔴 EXCEPTION raised while updating agent: "+str(e))
                anx.error(traceback.format_exc())
                anx.error("Rebooting agent...")
                agent.disconnect()
                time.sleep(3)
        else:			
            while True:
                agent.update()
    
class AgentFr(IAgentFr):
    def __init__(self,nom:str or None=None, arene:str or None=None, username:str or None=None, password:str or None=None, url:str or None=None, port:int=1883, fluxImage:str or None="img.jpeg", autoconnect:bool=True, proxy:bool=True, verbosite:int=3, robotId:str or None="_", welcomePrint=True, sourcesdir:str or None=None):
        while ( nom == None or len(nom) > 32 or len(nom) == 0 ):
            nom=input("👾 pseudo (< 12 caracteres): ")
        while ( url == None or len(url) == 0 ):
            url=input("🌐 url: ")
            port=int(input("📫 port: "))
        if ( arene == None ):
            arene=input("🎲 arene: ")
        if ( username == None ):
            username=input("🧑 identifiant: ")
        if ( password == None ):
            password=input("🔑 mot de passe: ")
        if ( welcomePrint ):
            passwordParam = (base64.b64encode(password.encode('utf-8'))).decode('utf-8')
            print("Hey 👋")
            print("Pour visualiser l'arene de jeu 🎮, allez sur 👉 https://play.jusdeliens.com/?viewer=pytactx&arena="+str(arene)+"&url="+str(url)+"&usr="+str(username)+"&pseudo="+str(nom))
            print("Pour en savoir plus sur votre agent 💡, rdv sur 👉 https://tutos.jusdeliens.com")
            print("Pour participer aux prochains affrontements ⚔️, rendez-vous sur 👉 https://jusdeliens.com")
        if ( sourcesdir == None ):
            callerstack = (inspect.stack()[1])
            sourcesdir = os.path.dirname(os.path.abspath(callerstack[1]))
        super().__init__()
        self.__mapEnToFr = {
            "clientId":"idClient", "playerId":"idJoueur", "robotId":"idRobot", "team":"equipe", "profile":"profile", 
            "dtCreated":"dtCreation", "x":"x", "y":"y", "dir":"orientation", "pose":"pose",
            "life":"vie", "ammo":"munitions", "distance":"distance",
            "color":"couleur", "infoPlayer":"infoJoueur", "range":"voisins",
            "score":"score", "rank":"classement",
            "nFire":"nTirs", "nHitFire":"nTirsRecus", "nCollision":"nCollisions", "nMove":"nDeplacements", "nKill":"nTirs", "nDeath":"nMorts", "nExe":"nExecutions",
            "game":"jeu", "players":"agents", "robots":"robots", "map":"carte", "infoArena":"chatArena",
            "isGamePaused":"jeuEnPause", "gridColumns":"tailleGrilleColonnes", "gridRows":"tailleGrilleLignes"
        }
        self.__agent = Agent(nom, arene,username,password,url,port,fluxImage, autoconnect,proxy,verbosite, robotId, False, sourcesdir)
        self.robot = self.__agent.robot
    def connecter(self) -> bool :
        return self.__agent.connect()
    def deconnecter(self) -> None :
        self.__agent.disconnect()
    def robotEstConnecte(self) -> bool :
        return self.__agent.isConnectedToRobot()
    def areneEstConnecte(self) -> bool :
        return self.__agent.isConnectedToArena()
    def actualiser(self, activerSleep:bool=True):
        self.__agent.update(activerSleep)
        for enAttribute,frAttribute in self.__mapEnToFr.items():
            if ( enAttribute in self.__agent.__dict__ ):
                self.__dict__[frAttribute] = self.__agent.__dict__[enAttribute]
    def tirer(self, gachette:bool=True, trajectoire:Callable[[int],int] or None=None) -> None:
        self.__agent.fire(gachette, trajectoire)
    def deplacer(self,dx:int,dy:int) -> None:
        self.__agent.move(dx,dy)
    def deplacerVers(self,x:int,y:int) -> None:
        self.__agent.moveTowards(x,y)
    def orienter(self,dir:int) -> None:
        self.__agent.lookAt(dir)
    def changerArene(self,nomAttribut:str,valeurAttribut:Any) -> None:
        self.__agent.ruleArena(nomAttribut,valeurAttribut)
    def changerJoueur(self,agentId:str,nomAttribut:str,valeurAttribut:Any) -> None:
        self.__agent.rulePlayer(agentId,nomAttribut,valeurAttribut)
    def changerCouleur(self, r:int, g:int, b:int) -> None:
        self.__agent.setColor(r,g,b)
    def sabonner(self,evenement:str, callback:Callable[[Any,str,Any,Any], None]) -> None:
        self.__agent.addEventListener(evenement,callback)
    def afficher(self):
        print("👾  Joueur : "+str(self.idJoueur))
        print("🧭  Pose : "+str(self.x)+","+str(self.y)+","+str(self.orientation))
        print("📏 Distance: "+str(self.distance))
        print("🔫 Munitions: "+str(self.munitions))
        print("❤️  Vie: "+str(self.vie))
        print("🎨 Couleur: 🔴"+str(self.couleur[0])+" 🟢"+str(self.couleur[1])+" 🔵"+str(self.couleur[2]))
        print("🔍 Voisins: "+str(self.voisins))
        print()

class AgentFrCibleAleatoire(AgentFr):
    def __init__(self,nom:str or None=None, arene:str or None=None, username:str or None=None, password:str or None=None, url:str or None=None, port:int=1883, fluxImage:str or None="img.jpeg", autoconnect:bool=True, proxy:bool=True, verbosite:int=3, robotId:str or None="_"):
        super().__init__(nom=nom, arene=arene, username=username, password=password, url=url, port=port, fluxImage=fluxImage, autoconnect=autoconnect, proxy=proxy, verbosite=verbosite, robotId=robotId, 
                         sourcesdir=os.path.dirname(os.path.abspath((inspect.stack()[1])[1])))
        self.__cible = None
    def actualiser(self, activerSleep:bool=True):
        if ( self.__cible == None or (self.x == self.__cible[0] and self.y == self.__cible[1]) ):
            self.__cible = (randint(0,self.tailleGrilleColonnes-1), randint(0,self.tailleGrilleLignes-1))
            anx.info("Nouvelle cible: "+str(self.__cible))
        if ( self.distance != 0 ):
            self.tirer(True)
        else:
            self.tirer(False)
            self.deplacerVers(self.__cible[0], self.__cible[1])
            self.orienter((self.orientation + 1) % 4)
        return super().actualiser(activerSleep)
    
class AgentFrInoffensif(AgentFr):
    def __init__(self,nom:str or None=None, arene:str or None=None, username:str or None=None, password:str or None=None, url:str or None=None, port:int=1883, fluxImage:str or None="img.jpeg", autoconnect:bool=True, proxy:bool=True, verbosite:int=3,robotId:str or None="_"):
        super().__init__(nom=nom, arene=arene, username=username, password=password, url=url, port=port, fluxImage=fluxImage, autoconnect=autoconnect, proxy=proxy, verbosite=verbosite, robotId=robotId, 
                         sourcesdir=os.path.dirname(os.path.abspath((inspect.stack()[1])[1])))
    def actualiser(self, activerSleep:bool=True):
        self.orienter((self.orientation + 1) % 4)
        return super().actualiser(activerSleep)


if __name__ == '__main__':
    anx.warning("⚠️ Nothing to run from "+str(__file__))