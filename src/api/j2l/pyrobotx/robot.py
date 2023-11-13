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
from PIL import Image
from typing import Any, Callable

class RobotEvent:
	robotConnected = "robotConnected"
	robotDisconnected = "robotDisconnected"
	arenaConnected = "arenaConnected"
	arenaDisconnected = "arenaDisconnected"
	updated = "updated"
	robotChanged = "robotChanged"
	playerChanged = "playerChanged"
	arenaChanged = "arenaChanged"
	imageReceived = "imageReceived"

class IRobot:
	def addEventListener(self,eventName:str, callback:Callable[[Any,str,Any], None]) -> None:
		"""
		Subscribe to event to call the specified callback
		as soon as a event occurs
		"""
		...
	def changeRobot(self, robotId:str, autoconnect:bool):
		"""
		Connect to a new robot id.
		"""
		...
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
	def request(self, key:str, value:Any) -> None:
		"""
		Send a request to arena (when useProxy is True) 
		or to robot (if useProxy is False)
		"""
		...
	def getRobotId(self) -> str :
		"""
		Returns the unique id of the robot
		"""
		...
	def getBatteryVoltage(self) -> int :
		"""
		Returns the battery voltage in mV.
		"""
		...
	def getBatteryLevel(self, voltage=None) -> int :
		"""
		Returns the battery level from 0 (empty) to 100 (fully charged).
		if a voltage value is specified, level percent is assessed from it,
		otherwise, percent is assessed from last voltage value updated 
		"""
		...
	def getFrontLuminosity(self) -> int :
		"""
		Returns the front sensor luminosity from 0 (dark) to 255 (bright)
		"""
		...
	def getFrontLuminosityLevel(self, lum=None) -> int :
		"""
		Returns the front sensor luminosity from 0 (dark) to 100 (bright)
		if a lum value is specified, level percent is assessed from it,
		otherwise, percent is assessed from last luminosity value updated 
		"""
		...
	def getBackLuminosity(self) -> int :
		"""
		Returns the back sensor luminosity from 0 (dark) to 255 (bright)
		"""
		...
	def getBackLuminosityLevel(self, lum=None) -> int :
		"""
		Returns the back sensor luminosity from 0 (dark) to 100 (bright)
		if a lum value is specified, level percent is assessed from it,
		otherwise, percent is assessed from last luminosity value updated 
		"""
		...
	def getTimestamp(self) -> int :
		"""
		Returns the last timestamp received from Ova,
		i.e. the time elapsed in milliseconds since the boot of the robot
		"""
		...
	def getImageWidth(self) -> int :
		"""
		Returns the width of the last image captured during the last update
		in pixels. 0 If no image captured.
		"""
		...
	def getImageHeight(self) -> int :
		"""
		Returns the height of the last image captured during the last update
		in pixels. 0 If no image captured.
		"""
		...
	def getImageTimestamp(self) -> int :
		"""
		Returns the time elapsed in milliseconds between 
		the last time an image has been captured from the robot 
		and the creating of the robot class.
		"""
		...
	def getImagePixelRGB(self, x:int, y:int) -> tuple[int,int,int] :
		"""
		Returns the RGB code of the pixel at the specified x,y location.
		Returns (0,0,0) if the specified cordinate is invalid.
		"""
		...
	def getImagePixelLuminosity(self, x:int, y:int) -> int :
		"""
		Returns the luminosity from 0 (dark) to 100 (bright) of the pixel at the specified x,y location.
		Returns 0 if the specified cordinate is invalid.
		"""
		...
	def getRobotState(self) -> dict[str,Any] :
		"""
		Returns the infos of the robot as a dict
		"""
		...
	def getPlayerState(self) -> dict[str,Any] :
		"""
		Returns the infos of the player connected to ova in the arena
		"""
		...
	def getArenaState(self) -> dict[str,Any] :
		"""
		Returns the infos of the arena
		"""
		...
	def setMotorSpeed(self, left:int, right:int, durationInMsecs:int=0) -> None:
		"""
		Changes the speed of the 2 motors on the robot.
		The requested speeds will be send the next update call 

		# Arguments

		* `left` - The speed from -100 (backward) to 100 (forward) on the left wheel
		* `right` - The speed from -100 (backward) to 100 (forward) on the right wheel
		* `durationInMsecs` - The motors will be on during this duration in milliseconds.
		0 means forever. 
		"""
		...
	def setMotorAnimation(self, moves:list[tuple[int,int,int]]) -> None:
		"""
		Changes the speed of the 2 motors on the robot,
		following specified moves during the specified duration for each color.
		The requested animation will be started the next update call 

		# Arguments

		* `moves` - A list motor requests to be played in the same order from index 0,
		to the end of the list, each request as a tuple of 3 integer values
		(speedMotorLeft,speedMotorRight,durationInMsecs). 
		The speed of each motor should be from -100 (backward) to 100 (forward).
		"""
		...
	def setLedColor(self, r:int, g:int, b:int) -> None:
		"""
		Changes the color of the RGB led on the top of the robot
		The requested color will be send the next update call 

		# Arguments

		* `r` - The red from 0 to 255
		* `g` - The green from 0 to 255
		* `b` - The blue from 0 to 255
		"""
		...
	def setLedTwinkle(self, r:int, g:int, b:int, periodInMsecs:int, repeat:int=0):
		"""
		Twinkle the color of the RGB led on the top of the robot.
		The requested rgb animation will be started the next update call, 
		then will stop after 'repeat' time if a >0 value is specified. 

		# Arguments

		* `r` - The red from 0 to 255
		* `g` - The green from 0 to 255
		* `b` - The blue from 0 to 255
		* `periodInMsecs` - The LED will light on during periodInMsecs/2, 
		then light off during periodInMsecs/2
		* `repeat` - The number of time the animation will be repeated. 
		0 means repeat forever
		"""
		...
	def setLedFade(self, r:int, g:int, b:int, periodInMsecs:int, repeat:int=0):
		"""
		Fade in and out the color of the RGB led on the top of the robot.
		The requested rgb animation will be started the next update call, 
		then will stop after 'repeat' time if a >0 value is specified. 

		# Arguments

		* `r` - The red from 0 to 255
		* `g` - The green from 0 to 255
		* `b` - The blue from 0 to 255
		* `periodInMsecs` - The LED will smoothly light on during periodInMsecs/2, 
		then smoothly light off during periodInMsecs/2
		* `repeat` - The number of time the animation will be repeated. 
		0 means repeat forever
		"""
		...
	def setLedHue(self, periodInMsecs:int, repeat:int=0):
		"""
		Change the color of the RGB led on the top of the robot following hue wheel.
		The requested animation will be started the next update call, 
		then will stop after 'repeat' time if a >0 value is specified. 

		# Arguments

		* `periodInMsecs` - The LED will go from red to green during periodInMsecs/3, 
		to blue during periodInMsecs/3, to red during periodInMsecs/3
		* `repeat` - The number of time the animation will be repeated. 
		0 means repeat forever
		"""
		...
	def setLedAnimation(self, colors:list[tuple[int,int,int,int]], repeat:int=1):
		"""
		Change the colors of the RGB led on the top of the robot, 
		following specified colors during the specified duration for each color.
		The requested animation will be started the next update call, 
		then will stop after 'repeat' time if a >0 value is specified. 

		# Arguments

		* `colors` - A list color to be played in the same order from index 0,
		to the end of the list, each color as a tuple of 4 integer values
		(red,green,blue,durationInMsecs)  
		* `repeat` - The number of time the animation will be repeated. 
		0 means repeat forever
		"""
		...
	def playMelody(self, tones:list[tuple[int or str,int]]) -> None:
		"""
		Plays a melody of tones with the buzzer of the robot.
		The requested melody will be send the next update call 

		# Arguments

		* `tones` - A list of tones to be played in the same order from index 0,
		to the end of the list. Each tone must be a tuple of two parms :
		(ToneHeight, DurationInMilliseconds) 
		ToneHeight can be either
		- a str for an anglosaxon tone (i.e. A4, D#5, Gb7) 
		- a int for a frequency in Hz (i.e. 440) 
		- a int for a tone index (i.e. 0 for A4, 1 for A#4, 2 for B4 ...) 
		Duration should be an int 
		"""
		...
	def requestPlayer(self, key:str, value:Any) -> None :
		"""
		Generic method to request arena to do something on the player
		"""
		...
	def requestArena(self, key:str, value:Any) -> None :
		"""
		Generic method to request arena to do something
		"""
		...
	def _onConnectedToRobot(self) -> None:
		"""
		Called on update() call when the client is connected to the robot
		In order to use this method, follow these steps:
			1. Create your own robot class that inherits from OvaClientMqtt 
			2. Create a __init__ method and calls super().__init__(...) at the end
			2. Rewrite this method to override its behaviour
			3. Instanciate the robot class
			4. Call update() from OvaClientMqtt periodically in the main loop
		"""
		...
	def _onDisconnectedFromRobot(self) -> None:
		"""
		Called on update() call when the client is disconnected from the robot
		In order to use this method, follow these steps:
			1. Create your own robot class that inherits from OvaClientMqtt 
			2. Create a __init__ method and calls super().__init__(...) at the end
			2. Rewrite this method to override its behaviour
			3. Instanciate the robot class
			4. Call update() from OvaClientMqtt periodically in the main loop
		"""
		...
	def _onConnectedToArena(self):
		"""Called after the client is connected to the arena"""
		...
	def _onDisconnectedFromArena(self):
		"""Called after the client is disconnected from the arena"""
		...
	def _onUpdated(self) -> None:
		"""
		Called each time update() function is called"
		In order to use this method, follow these steps:
			1. Create your own robot class that inherits from OvaClientMqtt 
			2. Create a __init__ method and calls super().__init__(...) at the end
			2. Rewrite this method to override its behaviour
			3. Instanciate the robot class
			4. Call update() from OvaClientMqtt periodically in the main loop
		"""
		...
	def _onRobotChanged(self, robotState:dict[str,Any]) -> None:
		"""
		Called on update() call each time new state is received from the robot
		In order to use this method, follow these steps:
			1. Create your own robot class that inherits from OvaClientMqtt 
			2. Create a __init__ method and calls super().__init__(...) at the end
			2. Rewrite this method to override its behaviour
			3. Instanciate the robot class
			4. Call update() from OvaClientMqtt periodically in the main loop
			
		# Arguments

		* `robotState` - The new sensor's states and other attributes of the robot
		as a dict of str key and any typed value
		"""
		...
	def _onPlayerChanged(self, playerState:dict[str,Any]) -> None:
		"""
		Called on update() call each time new state is received from the player 
		in the game.
		In order to use this method, follow these steps:
			1. Create your own robot class that inherits from OvaClientMqtt 
			2. Create a __init__ method and calls super().__init__(...) at the end
			2. Rewrite this method to override its behaviour
			3. Instanciate the robot class
			4. Call update() from OvaClientMqtt periodically in the main loop
			
		# Arguments

		* `playerState` - The new player's states and other attributes of the player
		as a dict of str key and any typed value
		"""
		...
	def _onArenaChanged(self, arenaState:dict[str,Any]) -> None:
		"""
		Called on update() call each time new state is received from the arena game.
		In order to use this method, follow these steps:
			1. Create your own robot class that inherits from OvaClientMqtt 
			2. Create a __init__ method and calls super().__init__(...) at the end
			2. Rewrite this method to override its behaviour
			3. Instanciate the robot class
			4. Call update() from OvaClientMqtt periodically in the main loop
			
		# Arguments

		* `arenaState` - The new arena's states and other attributes of the arena
		as a dict of str key and any typed value
		"""
		...
	def _onImageReceived(self, img:Image) -> None:
		"""
		Called on update() call each time new complete image is received from the robot.
		In order to use this method, follow these steps:
			1. Create your own robot class that inherits from OvaClientMqtt 
			2. Create a __init__ method and calls super().__init__(...) at the end
			2. Rewrite this method to override its behaviour
			3. Instanciate the robot class
			4. Call update() from OvaClientMqtt periodically in the main loop
			
		# Arguments

		* `img` - A pillow Image instance on which you could do various operations. 
		For more info, see https://pillow.readthedocs.io/en/stable/reference/Image.html
		"""
		...
