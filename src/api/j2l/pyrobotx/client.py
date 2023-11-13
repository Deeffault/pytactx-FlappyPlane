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

# Allow import without error 
# "relative import with no known parent package"
# In vscode, add .env file with PYTHONPATH="..." 
# with the same dir to allow intellisense
import sys
import os
__workdir__ = os.path.dirname(os.path.abspath(__file__))
__libdir__ = os.path.dirname(__workdir__)
sys.path.append(__libdir__)

os.system("export LANG=en_US.UTF-8")
os.system("pip install paho-mqtt pillow requests")

import random
import copy
import requests
import uuid
import time
import traceback
import threading
import io
import json
from paho.mqtt.client import Client
from datetime import datetime
from PIL import Image
from typing import Any, Callable

from pyrobotx.robot import IRobot, RobotEvent
import pymusx.converter as msx
import pychromatx.converter as cmx
import pyanalytx.logger as anx

class DefaultClientSettings:
	melodySizeLimit = 100 # In tone number
	melodyDurationLimit = 10000 # In msecs
	isConnectedTimeout = 10000 # In msecs
	dtTx = 100 # In msecs
	dtPing = 5000 # In msecs
	dtSleepUpdate = 100 # In msecs
	batteryMax = 3900 # In mV
	batteryMin = 3500 # In mV

class EventObservable:
	def __init__(self, events:list[str]):
		self.__onEventCallbacks : dict[str, Callable[[Any,str,Any], None] or None] = {}
		for eventName in events:
			self.__onEventCallbacks[eventName] = None
	def addEventListener(self,eventName:str, callback:Callable[[Any,str,Any], None]) -> None:
		if ( eventName not in self.__onEventCallbacks ):
			anx.warning("⚠️ Cannot add event listener for event "+eventName)
			anx.warning("⚠️ Can only add event on "+str(self.__onEventCallbacks.keys()))
			return
		self.__onEventCallbacks[eventName] = callback
	def notify(self, eventName:str, value:Any or None=None) -> None:
		if ( eventName not in self.__onEventCallbacks ):
			anx.warning("⚠️ Cannot notify event "+eventName)
			anx.warning("⚠️ Can only notify event on "+str(self.__onEventCallbacks.keys()))
			return
		if ( self.__onEventCallbacks[eventName] != None ):
			try:
				self.__onEventCallbacks[eventName](self, eventName, value)
			except Exception as e:
				anx.debug("⚠️ Exception during "+eventName+" event notification : "+str(e))
				anx.debug(traceback.format_exc())

class RobotEventManager(EventObservable):
	def __init__(self, robot:IRobot):
		self.__robot:IRobot = robot
		super().__init__(RobotEvent.__dict__.values())
	def onUpdated(self):
		try:
			self.__robot._onUpdated()
			self.notify(RobotEvent.updated, None)
		except Exception as e:
			anx.error("⚠️ Exception during _onUpdated call : "+str(e))
			anx.error(traceback.format_exc())
	def onImageReceived(self, img:Image):
		try:
			self.__robot._onImageReceived(img)
			self.notify(RobotEvent.imageReceived, img)
		except Exception as e:
			anx.debug("⚠️ Exception during _onImageReceived call : "+str(e))
			anx.debug(traceback.format_exc())
	def onArenaConnected(self, arenaName:str):
		anx.info("🟢 Arena "+arenaName+" connected")
		try:
			self.__robot._onConnectedToArena()
			self.notify(RobotEvent.arenaConnected, None)
		except Exception as e:
			anx.error("⚠️ Exception during _onConnectedToArena call : "+str(e))
			anx.error(traceback.format_exc())
	def onArenaDisconnected(self, arenaName:str):
		anx.info("🔴 Arena "+arenaName+" disconnected")
		try:
			self.__robot._onDisconnectedFromArena()
			self.notify(RobotEvent.arenaDisconnected, None)
		except Exception as e:
			anx.error("⚠️ Exception during _onDisconnectedFromArena call : "+str(e))
			anx.error(traceback.format_exc())
	def onRobotConnected(self):
		anx.info("🟢 Robot "+str(self.__robot.getRobotId())+" connected")
		try:
			self.__robot._onConnectedToRobot()
			self.notify(RobotEvent.robotConnected, None)
		except Exception as e:
			anx.error("⚠️ Exception during _onConnectedToRobot call : "+str(e))
			anx.error(traceback.format_exc())
	def onRobotDisconnected(self):
		anx.info("🔴 Robot "+str(self.__robot.getRobotId())+" disconnected")
		try:
			self.__robot._onDisconnectedFromRobot()
			self.notify(RobotEvent.robotDisconnected, None)
		except Exception as e:
			anx.error("⚠️ Exception during _onDisconnectedFromRobot call : "+str(e))
			anx.error(traceback.format_exc())
	def onRobotChanged(self, robotState:dict[str,Any]):
		anx.debug("🤖 Robot changed: "+str(robotState))
		try:
			self.__robot._onRobotChanged(robotState)
			self.notify(RobotEvent.robotChanged, robotState)
		except Exception as e:
			anx.debug("⚠️ Exception during _onRobotChanged call : "+str(e))
			anx.debug(traceback.format_exc())
	def onArenaChanged(self, arenaState:dict[str,Any]):
		anx.debug("🎲 Arena changed: "+str(arenaState))
		try:
			self.__robot._onArenaChanged(arenaState)
			self.notify(RobotEvent.arenaChanged, arenaState)
		except Exception as e:
			anx.error("⚠️ Exception during _onArenaChanged call : "+str(e))
			anx.error(traceback.format_exc())
	def onPlayerChanged(self, playerState:dict[str,Any]):
		anx.debug("♟️ Player changed: "+str(playerState))
		try:
			self.__robot._onPlayerChanged(playerState)
			self.notify(RobotEvent.playerChanged, playerState)
		except Exception as e:
			anx.error("⚠️ Exception during _onPlayerChanged call : "+str(e))
			anx.error(traceback.format_exc())

class RobotStateParser:
	def __init__(self):
		self.__robotSensorsState = {}
	def fromDict(self, robotState:dict[str,Any]):
		for key,value in robotState.items():
			self.__robotSensorsState[key] = copy.deepcopy(value)
	def toDict(self):
		return self.__robotSensorsState
	def getRobotId(self) -> str :
		if ( "uid" not in self.__robotSensorsState ):
			return ""
		return self.__robotSensorsState["uid"]
	def getBatteryVoltage(self) -> int :
		if ( "battery" not in self.__robotSensorsState or "voltage" not in self.__robotSensorsState["battery"] ):
			return 0
		return self.__robotSensorsState["battery"]["voltage"]
	def getBatteryLevel(self, voltage=None) -> int :
		if ( voltage == None ):
			voltage = self.getBatteryVoltage()
		if ( voltage > DefaultClientSettings.batteryMax ): return 100
		elif ( voltage < DefaultClientSettings.batteryMin ): return 0
		else:
			return int(100*(voltage-DefaultClientSettings.batteryMin) / (DefaultClientSettings.batteryMax-DefaultClientSettings.batteryMin))
	def getFrontLuminosity(self) -> int :
		if ( "photoFront" not in self.__robotSensorsState or "lum" not in self.__robotSensorsState["photoFront"] ):
			return 0
		return self.__robotSensorsState["photoFront"]["lum"]
	def getFrontLuminosityLevel(self, luminosity=None) -> int :
		if ( luminosity == None ):
			luminosity = self.getFrontLuminosity()
		return int(100*luminosity/255)
	def getBackLuminosity(self) -> int :
		if ( "photoBack" not in self.__robotSensorsState or "lum" not in self.__robotSensorsState["photoBack"] ):
			return 0
		return self.__robotSensorsState["photoBack"]["lum"]
	def getBackLuminosityLevel(self, luminosity=None) -> int :
		if ( luminosity == None ):
			luminosity = self.getBackLuminosity()
		return int(100*luminosity/255)
	def getTimestamp(self) -> int :
		if ( "t" not in self.__robotSensorsState ):
			return 0
		return self.__robotSensorsState["t"]

class RobotRequestBuilder:
	def __init__(self):
		self.__animDuration:int = 0
		self.__robotActuatorsRequest:dict[str,Any] = {}
		self.__fromLedAnimationToLedA = {
			"static": "0",
			"fade": "1",
			"twinkle": "2",
			"hue": "3"
		}
	def reset(self):
		self.__robotActuatorsRequest = {} 
		if ( self.__animDuration > 0 ):
			time.sleep(self.__animDuration/1000.0)
			self.__animDuration = 0
	def toDict(self):
		return self.__robotActuatorsRequest
	def toURI(self, url):
		req = self.__robotActuatorsRequest
		params = []
		if ( "led" in req ):
			if ( "rgb" in req["led"] ):
				params.append("ledr="+str(req["led"]["rgb"][0]))
				params.append("ledg="+str(req["led"]["rgb"][1]))
				params.append("ledb="+str(req["led"]["rgb"][2]))
			if ( "duration" in req["led"] ):
				params.append("ledt="+str(req["led"]["duration"]))
			if ( req["led"]["animation"] != "custom" and 
       			 req["led"]["animation"] in self.__fromLedAnimationToLedA ):
				params.append("leda="+self.__fromLedAnimationToLedA[req["led"]["animation"]])
			elif ( req["led"]["animation"] == "custom" ):
				animStr = "led=["
				nColors = len(req["led"]["colors"])
				for i in range(nColors):
					r,g,b,t = req["led"]["colors"][i]
					animStr +="["+str(r)+","+str(g)+","+str(b)+","+str(t)+"]"
					if ( i < nColors-1 ):
						animStr+=","
				animStr += "]"
				params.append(animStr)
		if ( "buzzer" in req ):
			nTones = len(req["buzzer"])
			if ( nTones == 1 ):
				f,t = req["buzzer"][0]
				params.append("tonef="+str(f))
				params.append("tonet="+str(t))
			elif ( nTones > 1 ):
				animStr = "buzzer=["
				for i in range(nTones):
					f,t = req["buzzer"][i]
					animStr +="["+str(f)+","+str(t)+"]"
					if ( i < nTones-1 ):
						animStr+=","
				animStr += "]"
				params.append(animStr)
		if ( "motor" in req ):
			nMoves = len(req["motor"])
			if ( nMoves == 1 ):
				l,r,t = req["motor"][0]
				params.append("motorleft="+str(l))
				params.append("motorright="+str(r))
			elif ( nMoves > 1 ):
				animStr = "motor=["
				for i in range(nMoves):
					l,r,t = req["motor"][i]
					animStr +="["+str(l)+","+str(r)+","+str(t)+"]"
					if ( i < nMoves-1 ):
						animStr+=","
				animStr += "]"
				params.append(animStr)
		uri = url
		nparams = len(params)
		if ( nparams > 0 ):
			uri+= "?"
			for i in range(nparams-1):
				uri+=params[i]+"&"
			uri += params[nparams-1]
		return uri
	def setMotorSpeed(self, leftPower:int, rightPower:int, durationInMsecs:int=1000):
		if ( leftPower < -100 or rightPower < -100 or leftPower > 100 or rightPower > 100):
			anx.warning("⚠️ Motor speed should be between -100 and +100!")
			return
		if ( type(durationInMsecs)!=int or durationInMsecs < 0 or durationInMsecs > 10000 ):
			anx.warning("⚠️ Incorrect motor speed duration. Should be a positive integer value in ms lesser than 10000 !")
			return
		self.__robotActuatorsRequest["motor"] = [[leftPower,rightPower,durationInMsecs]]
	def setMotorAnimation(self, moves:list[tuple[int,int,int]]):
		for move in moves:
			if ( len(move) != 3 ):
				anx.warning("⚠️ Incorrect move in motor animation. Should be a list of tuples of 3 params : speedMotorLeft, speedMotorRight, durationInMs !")
				return
			for i in range(2):
				if ( type(move[i])!=int or move[i] < -100 or move[i] > 100 ):
					anx.warning("⚠️ Incorrect move in motor animation. Move speed should be an integer value between -100 (backward) and 100 (forward) !")
					return
			if ( type(move[2])!=int or move[2] < 0 or move[2] > 10000 ):
				anx.warning("⚠️ Incorrect move in motor animation. Move duration should be a positive integer value in ms lesser than 10000 !")
				return
		self.__robotActuatorsRequest["motor"] = moves
	def setLedColor(self, r:int, g:int, b:int):
		if ( r < 0 or g < 0 or b < 0 or r > 255 or g > 255 or b > 255 ):
			anx.warning("⚠️ LED RGB should be between 0 and 255!")
			return
		self.__robotActuatorsRequest["led"] = {
			"animation":"static",
			"rgb":[r,g,b],
			"repeat":0,
			"duration":0
		}
	def setLedTwinkle(self, r:int, g:int, b:int, periodInMsecs:int, repeat:int=0):
		if ( r < 0 or g < 0 or b < 0 or r > 255 or g > 255 or b > 255 ):
			anx.warning("⚠️ LED RGB should be between 0 and 255!")
			return
		if ( periodInMsecs < 0 or periodInMsecs > 65535):
			anx.warning("⚠️ LED twinkle period should be between 0 and 65535 ms!")
			return
		if ( repeat < 0 or repeat > 65535):
			anx.warning("⚠️ LED twinkle repeat should be between 0 (means forever) and 65535 ms!")
			return
		self.__robotActuatorsRequest["led"] = {
			"animation":"twinkle",
			"rgb":[r,g,b],
			"duration":periodInMsecs, 
			"repeat":repeat
		}
	def setLedFade(self, r:int, g:int, b:int, periodInMsecs:int, repeat:int=0):
		if ( r < 0 or g < 0 or b < 0 or r > 255 or g > 255 or b > 255 ):
			anx.warning("⚠️ LED RGB should be between 0 and 255!")
			return
		if ( periodInMsecs < 0 or periodInMsecs > 65535):
			anx.warning("⚠️ LED fade period should be between 0 and 65535 ms!")
			return
		if ( repeat < 0 or repeat > 65535):
			anx.warning("⚠️ LED fade repeat should be between 0 (means forever) and 65535 ms!")
			return
		self.__robotActuatorsRequest["led"] = {
			"animation":"fade",
			"rgb":[r,g,b],
			"duration":periodInMsecs, 
			"repeat":repeat
		}
	def setLedHue(self, periodInMsecs:int, repeat:int=0):
		if ( periodInMsecs < 0 or periodInMsecs > 65535):
			anx.warning("⚠️ LED HUE period should be between 0 and 65535 ms!")
			return
		if ( repeat < 0 or repeat > 65535):
			anx.warning("⚠️ LED HUE repeat should be between 0 (means forever) and 65535 ms!")
			return
		self.__robotActuatorsRequest["led"] = {
			"animation":"hue",
			"duration":periodInMsecs, 
			"repeat":repeat
		}
	def setLedAnimation(self, colors:list[tuple[int,int,int,int]], repeat:int=0):
		if ( repeat < 0 or repeat > 65535):
			anx.warning("⚠️ LED animation repeat should be between 0 (means forever) and 65535 ms!")
			return
		for color in colors:
			if ( len(color) != 4 ):
				anx.warning("⚠️ Incorrect color in led animation. Should be a list of tuples of 4 params : r,g,b, duration !")
				return
			for i in range(3):
				if ( type(color[i])!=int or color[i] < 0 or color[i] > 255 ):
					anx.warning("⚠️ Incorrect color in led animation. Color rgb should be a positive integer value between 0 (dark) and 255 (bright) !")
					return
			if ( type(color[3])!=int or color[3] < 0 or color[3] > 10000 ):
				anx.warning("⚠️ Incorrect color in led animation. Color duration should be a positive integer value in ms lesser than 10000 !")
				return
		self.__robotActuatorsRequest["led"] = {
			"animation":"custom",
			"repeat":repeat,
			"colors":colors
		}
	def playMelody(self, tones:list[tuple[int or str,int]]):
		if ( len(tones) <= 0 ):
			anx.warning("⚠️ No tone in melody!")
			return
		if ( len(tones) > DefaultClientSettings.melodySizeLimit ):
			anx.warning("⚠️ Too much tones in melody!")
			return
		duration = 0
		tonesHzMs = []
		for tone in tones:
			if ( len(tone) != 2 ):
				anx.warning("⚠️ Incorrect tone in melody. Should be a list of tuples of 2 params : frequency, duration !")
				return
			toneHeight = tone[0]
			toneDuration = tone[1]
			if ( type(toneDuration)!=int or toneDuration < 0 or toneDuration > 10000 ):
				anx.warning("⚠️ Incorrect duration in melody. Should be a positive integer value in ms lesser than 10000 !")
				return
			toneHeight = msx.toneToFreq(toneHeight)
			if ( toneHeight == None ):
				return
			# freq as index
			tonesHzMs.append((toneHeight,toneDuration))
			duration += toneDuration
		if ( duration > DefaultClientSettings.melodyDurationLimit ):
			anx.warning("⚠️ Melody duration is too long!")
			return
		self.__animDuration = duration
		self.__robotActuatorsRequest["buzzer"] = tonesHzMs

class RobotPrinter:
	def __init__(self, robot, welcome:bool=True):
		self.__robot = robot
		if ( welcome ):
			self.welcome()
	def welcome(self):
		print("Hi there 👋")
		print("Turn on your Ova to make it sing like a diva 🎤")
		print("Then wait until your hear the congrat jingle 🎵")
		print("You don't have a robot ? Follow the link 👉 https://jusdeliens.com/ova")
	def print(self):
		if self.__robot.isConnectedToRobot():
			print("🟢 Robot connected")
		else:
			print("🔴 Robot disconnected")
		if self.__robot.isConnectedToArena():
			print("🟢 Arena connected")
		else:
			print("🔴 Arena disconnected")
		print("🎲 Arena state: ", self.__robot.getArenaState())
		print("♟️ Player state: ", self.__robot.getPlayerState())
		print("🤖 Robot state: ", self.__robot.getRobotState())
		print("⬆️ Photo front lum: ", self.__robot.getFrontLuminosity())
		print("⬇️ Photo back lum: ", self.__robot.getBackLuminosity())
		print("🔋 Battery voltage: ", self.__robot.getBatteryVoltage())
		print("⏱️ Timestamp: ", self.__robot.getTimestamp(),"ms")
		print("📸 Camera img "+str(self.__robot.getImageWidth())+"x"+str(self.__robot.getImageHeight())+" shot after "+str(self.__robot.getImageTimestamp())+" ms")
		print("")

class CameraReader:
	def __init__(self, imgOutputPath):
		self.__camImg:Image = None
		self.__prevImgRx: int = 0
		self.__camImgOutputPath = imgOutputPath
		self.__bufImgComplete = []
		self.__bufImgMutex = threading.Lock()
		self.__bufImg = []
		self.__bufImgOffset = 0
		self.__bufImgExpectedLength = 0
		self.__dealImgAsChunk = False
		self.__startTime = datetime.now()
	def setOuputPath(self, path=str or None):
		self.__camImgOutputPath = path
	def getImage(self) -> Image:
		return self.__camImg
	def onFullImageReceived(self, data:bytes):
		with self.__bufImgMutex:
			self.__dealImgAsChunk = False
			self.__bufImgComplete = data
			self.__bufImg = []
	def onChunkImageReceived(self, data:bytes):
		"""To be called when rx payload on image topic. Returns True if all chunks received"""
		payloadLen = len(data)
		self.__dealImgAsChunk = True
		if ( payloadLen < 3 ):
			anx.debug("⚠️ Rx image corrupted. Payload len too small")
			return False
		imgLen = int.from_bytes(data[0:4],'big', signed=False)
		chunkOfs = int.from_bytes(data[4:8],'big', signed=False)
		chunkLen = int.from_bytes(data[8:12],'big', signed=False)
		anx.debug("📡 Rx image ["+str(chunkOfs)+":"+str(chunkOfs+chunkLen)+"] / "+str(imgLen))
		chunkImg = data[12:]
		if ( chunkOfs == 0 ):
			self.__bufImgOffset = 0
			self.__bufImgExpectedLength = imgLen
		elif ( imgLen != self.__bufImgExpectedLength or self.__bufImgOffset != chunkOfs ):
			anx.debug("⚠️ Rx image corrupted. Expected "+str(self.__bufImgOffset)+"/"+str(self.__bufImgExpectedLength)+" instead of rx "+str(chunkOfs)+"/"+str(imgLen))
			return False
		self.__bufImg.append(chunkImg)
		self.__bufImgOffset += chunkLen
		if ( self.__bufImgOffset == self.__bufImgExpectedLength ):
			with self.__bufImgMutex:
				self.__bufImgComplete = self.__bufImg.copy()
				self.__bufImg = []
				return True
		return False
	def update(self) -> int:
		"""Swap buf img and write into file, then return the number of bytes read"""
		lenImage = len(self.__bufImgComplete)
		try:
			with self.__bufImgMutex:
				if ( len(self.__bufImgComplete) > 0 ):
					if ( self.__dealImgAsChunk ):
						self.__camImg = Image.open(io.BytesIO(b''.join(self.__bufImgComplete)))
					else:
						self.__camImg = Image.open(io.BytesIO(self.__bufImgComplete))
					self.__bufImgComplete = []
					self.__prevImgRx = (datetime.now() - self.__startTime).total_seconds() * 1000
					if ( self.__camImgOutputPath != None ):
						try:
							self.__camImg.save(self.__camImgOutputPath)
							anx.debug("📸 Save camera image in "+str(os.getcwd())+"\\"+str(self.__camImgOutputPath))
						except Exception as e:
							anx.debug("⚠️ Fail to write "+str(self.__camImgOutputPath)+" : "+str(e))
							anx.debug(traceback.format_exc())
					anx.debug("🖼️ Camera img received: "+str(self.__camImg.width)+"x"+str(self.__camImg.height))
		except Exception as e:
			anx.debug("⚠️ Rx image corrupted. Fail to swap buffer : "+str(e))
			anx.debug(traceback.format_exc())
			return 0
		return lenImage
	def getImageWidth(self) -> int :
		if ( self.__camImg == None ):
			return 0
		return self.__camImg.width
	def getImageHeight(self) -> int :
		if ( self.__camImg == None ):
			return 0
		return self.__camImg.height
	def getImageTimestamp(self) -> int :
		return self.__prevImgRx
	def getImagePixelRGB(self, x:int,y:int) -> tuple[int,int,int] :
		if ( x < 0 or x >= self.__camImg.width or y < 0 or y >= self.__camImg.height ):
			return (0,0,0)
		r,g,b = self.__camImg.getpixel((x, y))
		return (r,g,b)
	def getImagePixelLuminosity(self, x:int,y:int) -> int :
		if ( x < 0 or x >= self.getImageWidth() or y < 0 or y >= self.getImageHeight() ):
			return 0
		r,g,b = self.__camImg.getpixel((x, y))
		h,s,l = cmx.RGBToHSL(r,g,b)
		return l

class OvaClientHttp(IRobot):
	def __init__(self, 
		  routeSensors,
		  routeCamera,
		  routeActuators,
	      url:str="http://192.168.4.1", 
	      imgOutputPath:str or None="img.jpeg", 
		  verbosity:int=3, 
		  welcomePrint=True
		):
		"""
		Build an IRobot http client to communicate directly to ova 
		using http requests/API.

		To be able to use the robot http API, you must
		- either be connected on the same LAN and the same subnet
		to be able to get and request the ip address of your robot.
		- or be connected on the access point of your robot, in this case,
		its url to join it would be http://192.168.4.1

		# Arguments

		* `url` - The http url to join ova on a LAN or WAN network, e.g. http://192.168.4.1
		* `verbosity` - The level of logs as an int. See Verbosity class for more info.
		* `imgOutputPath` - The path (either absolute or relative) where to save camera image on each update call
		* `welcomePrint` - True to print a nice message in the begining to welcome and guide you
		"""
		anx.setVerbosity(verbosity)
		if ( "http://" not in url ):
			url = "http://" + url
		self.__url = url
		self.__robotSensorsState : RobotStateParser = RobotStateParser()
		self.__robotActuatorsRequest : RobotRequestBuilder = RobotRequestBuilder()
		self.__events : RobotEventManager = RobotEventManager(self)
		self.__cameraReader = CameraReader(imgOutputPath)
		self.__printer = RobotPrinter(self, welcomePrint)
		self.__prevTx: int = datetime.fromtimestamp(0)
		self.__dtTxToWait: int = DefaultClientSettings.dtTx
		self.__prevRxFromRobot: int = datetime.fromtimestamp(0)
		self.__robotSensorsStateRoute = routeSensors
		self.__robotCamRoute = routeCamera
		self.__robotControlRoute = routeActuators
		self.__wasConnectedToRobot = False
	def addEventListener(self,eventName:str, callback:Callable[[Any,str,Any], None]) -> None:
		self.__events.addEventListener(eventName, callback)
	def connect(self) -> bool :
		anx.warning("Connect not implemented for ova http client")
		return False
	def disconnect(self) -> bool :
		anx.warning("Disconnect not implemented for ova http client")
		return False
	def isConnectedToArena(self) -> bool:
		return False
	def isConnectedToRobot(self) -> bool:
		dtRx = (datetime.now() - self.__prevRxFromRobot).total_seconds() * 1000
		return dtRx < DefaultClientSettings.isConnectedTimeout
	def update(self, enableSleep=True):
		self.__events.onUpdated()
		now = datetime.now()
		self._onUpdateSensors(self.__url+self.__robotSensorsStateRoute, now)
		self._onUpdateCamera(self.__url+self.__robotCamRoute, now)
		# Tx requests
		dtTx = (now-self.__prevTx).total_seconds() * 1000
		if ( dtTx > self.__dtTxToWait ):
			self.__prevTx = now
			self._onUpdateRequests(self.__url+self.__robotControlRoute, self.__robotActuatorsRequest, now)
		if (enableSleep):
			time.sleep(DefaultClientSettings.dtSleepUpdate/1000)
	def getRobotId(self) -> str :
		return self.__robotSensorsState.getRobotId()
	def getBatteryVoltage(self) -> int :
		return self.__robotSensorsState.getBatteryVoltage()
	def getBatteryLevel(self) -> int :
		return self.__robotSensorsState.getBatteryLevel()
	def getFrontLuminosity(self) -> int :
		return self.__robotSensorsState.getFrontLuminosity()
	def getFrontLuminosityLevel(self) -> int :
		return self.__robotSensorsState.getFrontLuminosityLevel()
	def getBackLuminosity(self) -> int :
		return self.__robotSensorsState.getBackLuminosity()
	def getBackLuminosityLevel(self) -> int :
		return self.__robotSensorsState.getBackLuminosityLevel()
	def getTimestamp(self) -> int :
		return self.__robotSensorsState.getTimestamp()
	def getImageWidth(self) -> int :
		return self.__cameraReader.getImageWidth()
	def getImageHeight(self) -> int :
		return self.__cameraReader.getImageHeight()
	def getImageTimestamp(self) -> int :
		return self.__cameraReader.getImageTimestamp()
	def getImagePixelRGB(self, x:int,y:int) -> tuple[int,int,int] :
		return self.__cameraReader.getImagePixelRGB(x,y)
	def getImagePixelLuminosity(self, x:int,y:int) -> int :
		return self.__cameraReader.getImagePixelLuminosity(x,y)
	def getRobotState(self) -> dict[str,Any] :
		return self.__robotSensorsState.toDict()
	def getPlayerState(self) -> dict[str,Any] :
		return {}
	def getArenaState(self) -> dict[str,Any] :
		return {}
	def setMotorSpeed(self, leftPower:int, rightPower:int, durationInMsecs:int=1000):
		self.__robotActuatorsRequest.setMotorSpeed(leftPower,rightPower,durationInMsecs)
	def setMotorAnimation(self, moves:list[tuple[int,int,int]]):
		self.__robotActuatorsRequest.setMotorAnimation(moves)
	def setLedColor(self, r:int, g:int, b:int):
		self.__robotActuatorsRequest.setLedColor(r,g,b)
	def setLedTwinkle(self, r:int, g:int, b:int, periodInMsecs:int, repeat:int=0):
		self.__robotActuatorsRequest.setLedTwinkle(r,g,b,periodInMsecs,repeat)
	def setLedFade(self, r:int, g:int, b:int, periodInMsecs:int, repeat:int=0):
		self.__robotActuatorsRequest.setLedFade(r,g,b,periodInMsecs,repeat)
	def setLedHue(self, periodInMsecs:int, repeat:int=0):
		self.__robotActuatorsRequest.setLedHue(periodInMsecs,repeat)
	def setLedAnimation(self, colors:list[tuple[int,int,int,int]], repeat:int=0):
		self.__robotActuatorsRequest.setLedAnimation(colors)
	def playMelody(self, tones:list[tuple[int or str,int]]):
		self.__robotActuatorsRequest.playMelody(tones)
	def requestPlayer(self, key, value) -> None :
		anx.warning("requestPlayer not implemented for ova http client")
	def requestArena(self, key, value) -> None :
		anx.warning("requestArena not implemented for ova http client")
	def print(self) -> None:
		self.__printer.print()
	def _onUpdateSensors(self, url:str, now=None):
		if (now == None):
			now = datetime.now()
		try:
			r = requests.get(url)
			if ( r.status_code != 200 ):
				anx.warning("Return "+str(r.status_code)+" during tx "+url)
			else:
				anx.debug("📡 Rx state of "+str(len(r.text))+" byte(s): "+r.text)
				try:
					if ( self.__wasConnectedToRobot == False ):
						self.__wasConnectedToRobot = True
						self.__events.onRobotConnected()
					newRobotState = json.loads(r.text)
					oldState = self.__robotSensorsState.toDict()
					if ( newRobotState != oldState ):
						self.__robotSensorsState.fromDict(newRobotState)
						self.__events.onRobotChanged(self.__robotSensorsState.toDict())
					self.__prevRxFromRobot = now
				except Exception as e:
					anx.error("⚠️ Exception during loading json from "+url+" : "+str(e))
					anx.error(traceback.format_exc())
		except Exception as e:
			anx.error("⚠️ Exception during rx "+url+" : "+str(e))
			anx.error(traceback.format_exc())
			if ( self.__wasConnectedToRobot == True and self.isConnectedToRobot() == False ):
				self.__wasConnectedToRobot = False
				self.__events.onRobotDisconnected()
	def _onUpdateCamera(self, url:str, now=None):
		if (now == None):
			now = datetime.now()
		try:
			r = requests.get(url)
			if ( r.status_code != 200 ):
				anx.warning("Return "+str(r.status_code)+" during tx "+url)
			else:
				anx.debug("📡 Rx cam jpg img of "+str(len(r.content))+" byte(s)")
				try:
					self.__cameraReader.onFullImageReceived(r.content)
					if ( self.__cameraReader.update() > 0 ):
						self.__events.onImageReceived(self.__cameraReader.getImage())
				except Exception as e:
					anx.error("⚠️ Exception during cam img loading : "+str(e))
					anx.error(traceback.format_exc())
		except Exception as e:
			anx.error("⚠️ Exception during rx "+url+" : "+str(e))
			anx.error(traceback.format_exc())
	def _onUpdateRequests(self, url:str, request:RobotRequestBuilder, now=None):
		if (now == None):
			now = datetime.now()
		try:
			content = request.toDict()
			if ( len(content) > 0 ):
				anx.debug("📡 Tx request to "+url+" : "+str(content))
				r = requests.post(url, json=content)
				if ( r.status_code != 200 ):
					anx.warning("Return "+str(r.status_code)+" during tx "+url)
				else:
					request.reset()
		except Exception as e:
			anx.error("⚠️ Exception during tx "+url+" : "+str(e))
			anx.error(traceback.format_exc())

class OvaClientHttpV1(OvaClientHttp):
	def __init__(self, url:str or None=None, imgOutputPath:str or None="img.jpeg", verbosity:int=3, welcomePrint=True):
		"""
		Build an IRobot http client to communicate directly to ova,
		for ovaOS 1.x.x versions only, using http requests

		# Arguments

		* `url` - The http url to join ova on a LAN or WAN network, e.g. http://192.168.4.1
		* `verbosity` - The level of logs as an int. See Verbosity class for more info.
		* `imgOutputPath` - The path (either absolute or relative) where to save camera image on each update call
		* `welcomePrint` - True to print a nice message in the begining to welcome and guide you
		"""
		anx.setVerbosity(verbosity)
		super().__init__(
			routeSensors="/api/robot",
			routeCamera="/cam/jpg",
			routeActuators="/robot",
			url=url,
			imgOutputPath=imgOutputPath,
			verbosity=verbosity,
			welcomePrint=welcomePrint,
		)
	def getRobotId(self) -> str :
		state = self.getRobotState()
		if ( "esp" not in state or "id" not in state["esp"] ):
			return ""
		return state["esp"]["id"]
	def getBatteryVoltage(self) -> int :
		state = self.getRobotState()
		if ( "sensors" not in state or 
      		"battery" not in state["sensors"] or 
			"voltage" not in state["sensors"]["battery"] ):
			return 0
		return state["sensors"]["battery"]["voltage"]
	def getBatteryLevel(self, voltage) -> int :
		if ( voltage == None ):
			voltage = self.getBatteryVoltage()
		return super().getBatteryLevel(voltage)
	def getFrontLuminosity(self) -> int :
		state = self.getRobotState()
		if ( "sensors" not in state or 
      		"photoFront" not in state["sensors"] or 
			"lum" not in state["sensors"]["photoFront"] ):
			return 0
		return state["sensors"]["photoFront"]["lum"]
	def getFrontLuminosityLevel(self, lum) -> int :
		if ( lum == None ):
			lum = self.getFrontLuminosity()
		return super().getFrontLuminosityLevel(lum)
	def getBackLuminosity(self) -> int :
		state = self.getRobotState()
		if ( "sensors" not in state or 
      		"photoBack" not in state["sensors"] or 
			"lum" not in state["sensors"]["photoBack"] ):
			return 0
		return state["sensors"]["photoBack"]["lum"]
	def getBackLuminosityLevel(self) -> int :
		if ( lum == None ):
			lum = self.getBackLuminosity()
		return super().getBackLuminosityLevel(lum)
	def setMotorAnimation(self, moves:list[tuple[int,int,int]]):
		if ( len(moves) > 1 ):
			anx.warning("setMotorAnimation implemented for only 1 move in ova http client v1")
		self.__robotActuatorsRequest.playMelody(moves)
	def setLedAnimation(self, colors:list[tuple[int,int,int,int]], repeat:int=0):
		anx.warning("setLedAnimation not implemented in ova http client v1")
	def playMelody(self, tones:list[tuple[int or str,int]]):
		if ( len(tones) > 1 ):
			anx.warning("playMelody implemented for only 1 tone in ova http client v1")
		self.__robotActuatorsRequest.playMelody(tones)
	def _onUpdateRequests(self, url:str, request:RobotRequestBuilder,now=None):
		if (now == None):
			now = datetime.now()
		try:
			if ( len(request.toDict()) > 0 ):
				url = request.toURI(url)
				anx.debug("📡 Tx request "+url)
				r = requests.get(url)
				if ( r.status_code != 200 ):
					anx.warning("Return "+str(r.status_code)+" during tx "+url)
				else:
					request.reset()
		except Exception as e:
			anx.error("⚠️ Exception during tx "+url+" : "+str(e))
			anx.error(traceback.format_exc())

class OvaClientHttpV2(OvaClientHttp):
	def __init__(self, url:str or None=None, imgOutputPath:str or None="img.jpeg", verbosity:int=3, welcomePrint=True):
		"""
		Build an IRobot http client to communicate directly to ova,
		from ovaOS 2.x.x versions and above, using http requests.

		# Arguments

		* `url` - The http url to join ova on a LAN or WAN network, e.g. http://192.168.4.1
		* `verbosity` - The level of logs as an int. See Verbosity class for more info.
		* `imgOutputPath` - The path (either absolute or relative) where to save camera image on each update call
		* `welcomePrint` - True to print a nice message in the begining to welcome and guide you
		"""
		anx.setVerbosity(verbosity)
		super().__init__(
			routeSensors="/api/robot",
			routeCamera="/api/robot/camera",
			routeActuators="/api/robot",
			url=url,
			imgOutputPath=imgOutputPath,
			verbosity=verbosity,
			welcomePrint=welcomePrint
		)

class OvaClientMqtt(IRobot):
	def __init__(self,robotId:str or None=None, arena:str or None=None, username:str or None=None, password:str or None=None, server:str or None=None, port:int=1883, imgOutputPath:str or None="img.jpeg", autoconnect:bool=True, useProxy:bool=True, verbosity:int=3, clientId:str or None=None, welcomePrint=True):
		"""
		Build a mqtt client to communicate with an ova robot through a mqtt broker
		
		To join a public arena using mqtt.jusdeliens.com as server/broker, 
		note that only read operations on robot will be allowed by default.
		To be granted write authorization on a robot in an arena, an arena admin
		must allow it. More informations on https://play.jusdeliens.com 

		In order to read/write from/to your robot as you wish, 
		you may  
		- deploy your own mqtt broker on your own machine (mosquitto for instance)
		- or use OvaClientHttp according to your ovaOS version
		- or connect to the access point of your robot and enter this url in a chrome webbrowser
		http://192.168.4.1 to program it directly in IDEAL
		
		# Arguments

		* `robotId` - The unique name of the robot to control (e.g. ovaxxxxxxxxxxxx) as str
		* `clientId` - The name of the ovamqttclient used for logging in the broker. Leave None will use a random one
		* `arena` - The name of the arena to join as str
		* `username` - The username to join the server as str
		* `password` - The password to join the server as str
		* `server` - The ip address of the server (e.g. 192.168.x.x) or a domain name (e.g. mqtt.jusdeliens.com) as str
		* `port` - The port of the server (e.g. 1883) as an int
		* `autoconnect` - If True, connect to the broker during init. If False, you should call update or connect yourself after init.
		* `useProxy` - If False, send request directly to robot through broker only. If true, sending to server proxy, which then redirect to robot.
		* `verbosity` - The level of logs as an int. See Verbosity class for more info.
		* `imgOutputPath` - The path (either absolute or relative) where to save camera image on each update call
		* `welcomePrint` - True to print a nice message in the begining to welcome and guide you
		"""
		anx.setVerbosity(verbosity)
		self.__printer = RobotPrinter(self, welcomePrint)
		if ( arena == None or username == None or password == None or server == None):
			print("Enter your credentials to connect to your robot")
		while ( robotId == None or len(robotId) > 32 or len(robotId) == 0 ):
			robotId=input("🤖 robot id (< 32 characters): ")
		while ( server == None or len(server) == 0 ):
			server=input("🌐 server address: ")
			port=int(input("🌐 server port: "))
		if ( arena == None ):
			arena=input("🎲 arena: ")
		if ( username == None ):
			username=input("🧑 username: ")
		if ( password == None ):
			password=input("🔑 password: ")
		self.__startTime = datetime.now()
		
		userLogin=""
		try: userLogin=str(os.getlogin()) 
		except: ...
		macAddr=""
		try: macAddr=str(hex(uuid.getnode())) 
		except: ...

		if ( clientId == None ):
			clientId = "OvaClientMqtt-"+robotId+"-"+userLogin+"-"+macAddr+"-"+str(random.randint(0,99999))

		self.__id : str = clientId
		self.__arena : str = arena 
		self.__idRobot : str = robotId 
		self.__isConnectedToRobot : bool = False
		self.__isConnectedToArena : bool = False
		self.__reqArena = {}
		self.__reqPlayer = {}
		self.__robotActuatorsRequest : RobotRequestBuilder = RobotRequestBuilder()
		self.__robotSensorsState : RobotStateParser = RobotStateParser()
		self.__cameraReader : CameraReader = CameraReader(imgOutputPath)
		self.__bufRobotStateMutex = threading.Lock()
		self.__bufRobotState = {}
		self.__rxFromRobot: bool = False
		self.__bufPlayerStateMutex = threading.Lock()
		self.__bufPlayerState = []
		self.__playerState = {}
		self.__rxFromPlayer: bool = False
		self.__bufArenaStateMutex = threading.Lock()
		self.__bufArenaState = []
		self.__arenaState = {}
		self.__rxFromArena: bool = False
		self.__prevRxFromRobot: int = datetime.fromtimestamp(0)
		self.__prevRxFromArena: int = datetime.fromtimestamp(0)
		self.__prevTx: int = datetime.fromtimestamp(0)
		self.__prevPing: int = datetime.fromtimestamp(0)
		self.__dtTxToWait: int = DefaultClientSettings.dtTx
		self.__useProxy = useProxy
		self.__isConnectedToBroker: bool = False
		self.__serverAddress: str = server
		self.__username: str  or  None = username
		self.__password: str  or  None = password
		self.__serverPort: int = port
		self.__isLoopStarted : bool = False
		self.__events : RobotEventManager = RobotEventManager(self)
		self.__topicImgStream : str = ""
		self.__topicRobotState : str = ""
		self.__topicPlayerState : str = ""
		self.__topicArenaState : str = ""
		self.__topicArenaRequest : str = ""
		self.__topicPlayerRequest : str = ""
		self.__topicRobotRequest : str = ""
		self.__topicsToSubcribe = []
		self.__client: Client or None = None
		self.__useClientThreadLoop:bool = True
		self.__clientThreadLoop:threading.Thread or None = None
		self.__changeRobot(robotId, autoconnect)

	def addEventListener(self,eventName:str, callback:Callable[[Any,str,Any], None]) -> None:
		self.__events.addEventListener(eventName, callback)

	def connect(self) -> bool :
		if self.__isLoopStarted and self.__isConnectedToBroker:
			return False
		if (self.__username is not None and self.__password is not None):
			self.__client.username_pw_set(self.__username, self.__password)
		try:
			if ( self.__isConnectedToBroker == False ):
				anx.info("⏳ Connecting "+str(self.__id)+" to broker "+self.__serverAddress+":"+str(self.__serverPort)+" ...")
				self.__client._connect_timeout = 5.0
				rc=self.__client.connect(self.__serverAddress, self.__serverPort)
				#OvaClientMqtt.__onConnect(self.__client, self, None, rc) # TODO to remove if using loopstart loopstop
			if ( self.__isLoopStarted == False ):
				anx.info("⏳ Starting mqtt thread loop ...")
				if ( self.__useClientThreadLoop ):
					self.__client.loop_start()
					anx.info("🟢 Started mqtt loop")
					self.__isLoopStarted = True
				else:
					self.__clientThreadLoop = threading.Thread(target=self.__clientLoop)
					self.__clientThreadLoop.start()
			time.sleep(2)
			return rc == 0
		except:
			return False

	def disconnect(self) -> None :
		if self.__isConnectedToBroker:
			anx.info("⏳ Disconnecting "+str(self.__id)+" from broker...")
			self.__client.disconnect()
		if self.__isLoopStarted: 
			anx.info("⏳ Stopping mqtt thread loop ...")
			self.__isLoopStarted = False	
			if ( self.__useClientThreadLoop ):
				self.__client.loop_stop()
				anx.info("🔴 Stopped mqtt thread loop")
			else:
				self.__clientThreadLoop.join()

	def isConnectedToArena(self) -> bool:
		dtRx = (datetime.now() - self.__prevRxFromArena).total_seconds() * 1000
		return self.__isConnectedToBroker and dtRx < DefaultClientSettings.isConnectedTimeout
	def isConnectedToRobot(self) -> bool:
		dtRx = (datetime.now() - self.__prevRxFromRobot).total_seconds() * 1000
		return self.__isConnectedToBroker and dtRx < DefaultClientSettings.isConnectedTimeout

	def update(self, enableSleep=True) -> None:
		if ( self.__isConnectedToBroker == False ):
			self.connect()
		self.__events.onUpdated()
		
		# Rx states and stream
		if ( self.__rxFromRobot ):
			self.__rxFromRobot = False
			# Triggers on connected event
			if ( self.__isConnectedToRobot == False ):
				self.__isConnectedToRobot = True
				self.__events.onRobotConnected()
			# Swap bug img and sensor states 
			if ( self.__cameraReader.update() > 0 ):
				self.__events.onImageReceived(self.__cameraReader.getImage())
			try:
				with self.__bufRobotStateMutex:
					oldState = self.__robotSensorsState.toDict()
					if ( self.__bufRobotState != oldState ):
						self.__robotSensorsState.fromDict(self.__bufRobotState)
						self.__bufRobotState = {}
						self.__events.onRobotChanged(self.__robotSensorsState.toDict())
			except:
				anx.debug("⚠️ Rx robot state corrupted. Fail to swap buffer.")
		elif ( self.__isConnectedToRobot == True and self.isConnectedToRobot() == False ):
			self.__isConnectedToRobot = False
			self.__events.onRobotDisconnected()
		if ( self.__rxFromPlayer ):
			self.__rxFromPlayer = False
			try:
				with self.__bufPlayerStateMutex:
					if ( self.__bufPlayerState != self.__playerState ):
						for key,value in self.__bufPlayerState.items():
							self.__playerState[key] = value
						self.__bufPlayerState = {}
						self.__events.onPlayerChanged(self.__playerState)
			except:
				anx.debug("⚠️ Rx player state corrupted. Fail to swap buffer.")
		if ( self.__rxFromArena ):
			self.__rxFromArena = False
			# Triggers on connected event
			if ( self.__isConnectedToArena == False ):
				self.__isConnectedToArena = True
				self.__events.onArenaConnected(self.__arena)
			try:
				with self.__bufArenaStateMutex:
					if ( self.__bufArenaState != self.__arenaState ):
						for key,value in self.__bufArenaState.items():
							self.__arenaState[key] = value
						self.__bufArenaState = {}
						self.__events.onArenaChanged(self.__arenaState)
			except:
				anx.debug("⚠️ Rx player state corrupted. Fail to swap buffer.")
		elif ( self.__isConnectedToArena == True and self.isConnectedToArena() == False ):
			self.__isConnectedToArena = False
			self.__events.onArenaDisconnected(self.__arena)

		# Tx requests
		dtTx = (datetime.now()-self.__prevTx).total_seconds() * 1000
		if ( dtTx > self.__dtTxToWait ):
			self.__prevTx = datetime.now()
			robotReqTopicsToPub = [self.__topicPlayerRequest]
			if ( self.__useProxy == False ):
				robotReqTopicsToPub.append(self.__topicRobotRequest)
			reqsToTx = [
				(self.__robotActuatorsRequest.toDict(), robotReqTopicsToPub),
				(self.__reqPlayer, [self.__topicPlayerRequest]),
				(self.__reqArena, [self.__topicArenaRequest])
			]
			for req in reqsToTx:
				request, topicsToPub = req
				if ( len(request) == 0 ):
					continue
				payloadStr = json.dumps(request)
				payloadBytes = str.encode(payloadStr)
				for topic in topicsToPub:
					anx.debug("📡 Tx "+str(self.__id)+" to topic "+str(topic)+": "+str(len(payloadBytes))+" byte(s)")
					self.__client.publish(topic, payloadBytes)

			self.__reqArena = {}
			self.__reqPlayer = {}
			self.__robotActuatorsRequest.reset()

		# Ping server
		dtPing = (datetime.now()-self.__prevPing).total_seconds() * 1000
		if ( dtPing > DefaultClientSettings.dtPing ):
			self.__prevPing = datetime.now()
			payloadStr = json.dumps({"ping":True})
			payloadBytes = str.encode(payloadStr)
			topicsToPub = [self.__topicPlayerRequest]
			for topic in topicsToPub:
				anx.debug("📡 Ping "+str(self.__id))
				self.__client.publish(topic, payloadBytes)

		if (enableSleep):
			time.sleep(DefaultClientSettings.dtSleepUpdate/1000)

	def getRobotId(self) -> str :
		return self.__idRobot
	def getBatteryVoltage(self) -> int :
		return self.__robotSensorsState.getBatteryVoltage()
	def getBatteryLevel(self) -> int :
		return self.__robotSensorsState.getBatteryLevel()
	def getFrontLuminosity(self) -> int :
		return self.__robotSensorsState.getFrontLuminosity()
	def getFrontLuminosityLevel(self) -> int :
		return self.__robotSensorsState.getFrontLuminosityLevel()
	def getBackLuminosity(self) -> int :
		return self.__robotSensorsState.getBackLuminosity()
	def getBackLuminosityLevel(self) -> int :
		return self.__robotSensorsState.getBackLuminosityLevel()
	def getTimestamp(self) -> int :
		return self.__robotSensorsState.getTimestamp()
	def getTimestamp(self) -> int :
		t = self.__robotSensorsState.getTimestamp()
		if ( t == 0 ):
			return (self.__prevRxFromArena-self.__startTime).total_seconds() * 1000
		return t
	def getImageWidth(self) -> int :
		return self.__cameraReader.getImageWidth()
	def getImageHeight(self) -> int :
		return self.__cameraReader.getImageHeight()
	def getImageTimestamp(self) -> int :
		return self.__cameraReader.getImageTimestamp()
	def getImagePixelRGB(self, x:int,y:int) -> tuple[int,int,int] :
		return self.__cameraReader.getImagePixelRGB(x,y)
	def getImagePixelLuminosity(self, x:int,y:int) -> int :
		return self.__cameraReader.getImagePixelLuminosity(x,y)
	def getRobotState(self) -> dict[str,Any] :
		return self.__robotSensorsState.toDict()
	def getPlayerState(self) -> dict[str,Any] :
		return self.__playerState
	def getArenaState(self) -> dict[str,Any] :
		return self.__arenaState

	def setMotorSpeed(self, leftPower:int, rightPower:int, durationInMsecs:int=1000):
		self.__robotActuatorsRequest.setMotorSpeed(leftPower,rightPower,durationInMsecs)
	def setMotorAnimation(self, moves:list[tuple[int,int,int]]):
		self.__robotActuatorsRequest.setMotorAnimation(moves)
	def setLedColor(self, r:int, g:int, b:int):
		self.__robotActuatorsRequest.setLedColor(r,g,b)
	def setLedTwinkle(self, r:int, g:int, b:int, periodInMsecs:int, repeat:int=0):
		self.__robotActuatorsRequest.setLedTwinkle(r,g,b,periodInMsecs,repeat)
	def setLedFade(self, r:int, g:int, b:int, periodInMsecs:int, repeat:int=0):
		self.__robotActuatorsRequest.setLedFade(r,g,b,periodInMsecs,repeat)
	def setLedHue(self, periodInMsecs:int, repeat:int=0):
		self.__robotActuatorsRequest.setLedHue(periodInMsecs,repeat)
	def setLedAnimation(self, colors:list[tuple[int,int,int,int]], repeat:int=0):
		self.__robotActuatorsRequest.setLedAnimation(colors)
	def playMelody(self, tones:list[tuple[int or str,int]]):
		self.__robotActuatorsRequest.playMelody(tones)

	def requestPlayer(self, key, value) -> None :
		self.__reqPlayer[key] = value
	def requestArena(self, key, value) -> None :
		self.__reqArena[key] = value
	def prompt(self, jsonReq:str) -> bool:
		try:
			self.__robotActuatorsRequest = json.loads(jsonReq)
			return True
		except:
			return False
	def print(self) -> None:
		self.__printer.print()
		
	def __changeRobot(self, robotId, autoconnect):
		anx.info("⏳ Connecting to robot "+str(robotId)+" ...")
		self.disconnect()
		self.__idRobot : str = robotId 
		self.__prevRxFromRobot: int = datetime.fromtimestamp(0)
		self.__topicImgStream : str  = "optx/clients/stream/"+self.__idRobot
		self.__topicRobotState : str  = "robotx/clients/state/"+self.__idRobot
		self.__topicPlayerState : str  = "ludx/clients/state/"+self.__arena+"/"+self.__id
		self.__topicArenaState : str  = "ludx/server/state/"+self.__arena
		self.__topicArenaRequest : str  = "ludx/server/request/"+self.__arena
		self.__topicPlayerRequest : str  = "ludx/clients/request/"+self.__arena+"/"+self.__id
		self.__topicRobotRequest : str  = "robotx/clients/request/"+self.__idRobot
		self.__topicsToSubcribe = [self.__topicImgStream, self.__topicRobotState, self.__topicPlayerState, self.__topicArenaState]
		self.__client: Client = Client(self.__id, userdata=self)
		self.__client.on_message = OvaClientMqtt.__onMessage
		self.__client.on_connect = OvaClientMqtt.__onConnect
		self.__client.on_disconnect = OvaClientMqtt.__onDisconnect
		self.__client.on_subscribe = OvaClientMqtt.__onSubscribe
		self.__client.on_unsubscribe = OvaClientMqtt.__onUnsubscribe
		if ( autoconnect ):
			self.connect()
	def __clientLoop(self):
		anx.info("🟢 Started mqtt loop")
		self.__isLoopStarted = True
		try:
			while ( self.__isLoopStarted ):
				self.__client.loop()
				time.sleep(0.1)
		except:
			anx.error("⚠️💔 CRITICAL ERROR in mqtt loop")
		anx.info("🔴 Stopped mqtt thread loop")
		self.__isLoopStarted = False
	def __onChunkImageReceived(self, data:bytes):
		"""Called when rx payload on image topic"""
		if ( self.__cameraReader.onChunkImageReceived(data) ):
			self.__rxFromRobot = True
	def __onSensorsReceived(self, data:bytes):
		"""Called when rx payload on sensors topic"""
		self.__prevRxFromRobot = datetime.now()
		newState = {}
		# Parse json payload
		try:
			payloadLen = len(data)
			if ( payloadLen <= 0 ):
				return
			payloadStr = data.decode()
			newState = json.loads(payloadStr)
			anx.debug("📡 Rx state of "+str(payloadLen)+" byte(s): "+payloadStr)
		except:
			anx.debug("⚠️ Rx state failed to parse json")
		with self.__bufRobotStateMutex:
			self.__bufRobotState = newState
			self.__rxFromRobot = True
	def __onPlayerStateReceived(self, data:bytes):
		"""Called when rx payload on player state topic"""
		self.__prevRxFromArena = datetime.now()
		newState = {}
		# Parse json payload
		try:
			payloadLen = len(data)
			if ( payloadLen <= 0 ):
				return
			payloadStr = data.decode()
			newState = json.loads(payloadStr)
			anx.debug("📡 Rx state of "+str(payloadLen)+" byte(s): "+payloadStr)
		except:
			anx.debug("⚠️ Rx state failed to parse json")
		with self.__bufPlayerStateMutex:
			self.__bufPlayerState = newState
			self.__rxFromPlayer = True
	def __onArenaStateReceived(self, data:bytes):
		"""Called when rx payload on arena state topic"""
		self.__prevRxFromArena = datetime.now()
		newState = {}
		# Parse json payload
		try:
			payloadLen = len(data)
			if ( payloadLen <= 0 ):
				return
			payloadStr = data.decode()
			newState = json.loads(payloadStr)
			anx.debug("📡 Rx state of "+str(payloadLen)+" byte(s): "+payloadStr)
		except:
			anx.debug("⚠️ Rx state failed to parse json")
		with self.__bufArenaStateMutex:
			self.__bufArenaState = newState
			self.__rxFromArena = True
	def __onMessage(client, userdata, message):
		"""Called when rx message from mqtt broker"""
		rxTopic = message.topic
		rxPayload = message.payload
		if ( rxTopic == userdata.__topicImgStream ):
			userdata.__onChunkImageReceived(rxPayload)
		elif ( rxTopic == userdata.__topicRobotState ):
			userdata.__onSensorsReceived(rxPayload)
		elif ( rxTopic == userdata.__topicPlayerState ):
			userdata.__onPlayerStateReceived(rxPayload)
		elif ( rxTopic == userdata.__topicArenaState ):
			userdata.__onArenaStateReceived(rxPayload)
		else:
			anx.debug("📡 Rx "+userdata.__id+" on topic "+rxTopic+": "+str(len(rxPayload))+" byte(s)")
	def __onConnect(client, userdata, flags, rc):
		"""Called after a connection to mqtt broker is requested"""
		if ( rc == 0 ):
			if ( userdata.__isConnectedToBroker == False ):
				userdata.__isConnectedToBroker = True
				anx.info("🟢 Connected "+userdata.__id+" to broker")
				for topic in userdata.__topicsToSubcribe:
					anx.info("⏳ Subscribing "+userdata.__id+" to topic "+topic)
					userdata.__client.subscribe(topic)
				pingRequest = json.dumps({"ping": True})
				topicsToPub = [userdata.__topicPlayerRequest]
				if ( userdata.__useProxy == False ):
					topicsToPub.append(userdata.__topicRobotRequest)
				for topic in topicsToPub:
					anx.debug("📡 Tx "+str(userdata.__id)+" to topic "+str(topic)+": "+str(len(pingRequest))+" byte(s)")
					userdata.__client.publish(topic, pingRequest)
		else:
			anx.error("❌ FAIL to connected "+userdata.__id+" to broker")
	def __onDisconnect(client, userdata, rc):
		"""Called when disconnected from mqtt broker"""
		anx.info("🔴 Disconnected "+userdata.__id+" from broker")
		userdata.__isConnectedToBroker = False
	def __onSubscribe(client, userdata, mid, granted_qos):
		"""Called after suscribed on mqtt topic"""
		anx.info("🔔 Subscribed "+userdata.__id+" to topic "+str(mid))
	def __onUnsubscribe(client, userdata, mid):
		"""Called after unsuscribed from mqtt topic"""
		anx.info("🔔 Unsubscribed "+userdata.__id+" from topic "+str(mid))	