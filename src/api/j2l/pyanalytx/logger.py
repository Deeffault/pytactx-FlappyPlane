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

import inspect
import time
import threading
import codecs
from pathlib import Path
from datetime import datetime 

class Verbosity:
	NONE = 0
	ERROR = 1
	WARNING = 2
	INFO = 3
	DEBUG = 4
	__fromStringToInt = {'none':0, 'error':1, 'warning':2, 'info':3, 'debug':4}
	__fromIntToString = ['none', 'error', 'warning', 'info', 'debug']
	def fromStringToInt(verbosity):
		if ( verbosity in Verbosity.__fromStringToInt ):
			return Verbosity.__fromStringToInt[verbosity]
		else:
			return 0
	def fromIntToString(verbosity):
		if ( verbosity >= 0 and verbosity < len(Verbosity.__fromIntToString) ):
			return Verbosity.__fromIntToString[verbosity]
		else:
			return "none"
class ILogger:
	def enable(self, isEnabled:bool):
		pass
	def setVerbosity(self, verbosity):
		pass
	def getVerbosity(self):
		pass
	def log(self, verbosity, message, caller, arg):
		pass
class ConsoleLogger(ILogger):
	def __init__(self, verbosity=Verbosity.ERROR, autoenable:bool=True):
		self.__verbosity = verbosity
		self.__start = int(1000*time.perf_counter())
		self.__isEnabled = False
		if ( autoenable ):
			self.enable(True)
	def enable(self,toEnable:bool):
		self.__isEnabled = toEnable
	def setVerbosity(self, verbosity):
		self.__verbosity = verbosity
	def getVerbosity(self):
		return self.__verbosity
	def log(self, verbosity, message, caller=None, previousFrame=None):
		if ( verbosity > self.__verbosity or self.__isEnabled == False ):
			return
		now = datetime.now()
		msEllapsedSinceStart = int(1000*time.perf_counter())-self.__start
		if ( previousFrame == None ):
			previousFrame = inspect.currentframe().f_back
		(filename, line_number, function_name, lines, index) = inspect.getframeinfo(previousFrame)
		#print(Verbosity.fromIntToString(verbosity)+'\t'+str(line_number)+':'+str(index)+'\t'+now.strftime("%m/%d/%Y-%H:%M:%S")+'-'+str(msEllapsedSinceStart)+'\t'+message)
		print(Verbosity.fromIntToString(verbosity)+'\t'+now.strftime("%m/%d/%Y-%H:%M:%S")+'-'+str(msEllapsedSinceStart)+'\t'+Path(filename).name+'\t'+str(line_number)+':'+str(index)+'\t'+function_name+'\t'+message+'\n')
class FileLogger(ILogger):
	def update(logger):
		while logger.__isEnabled:
			buf = []
			with logger.__bufLock:
				buf = logger.__buf.copy()
				logger.__buf = []
			try:
				with codecs.open(logger.__filepath, "a", "utf-8-sig") as f:
					for line in buf:
						print(line)
						f.write(line+"\n")
			except Exception as e:
				print(str(e))
			time.sleep(logger.__dtUpdate)
	def __init__(self, verbosity=Verbosity.ERROR, filepath="./io/pytactx.log", dtUpdateInSecs=1.0, autoenable=False):
		self.__verbosity = verbosity
		self.__filepath = filepath
		self.__dtUpdate = dtUpdateInSecs
		self.__start:int = int(1000*time.perf_counter())
		self.__buf:list[str] = []
		self.__isEnabled = False
		self.__bufLock:threading.Lock = threading.Lock()
		self.__thread = threading.Thread(target=FileLogger.update, args=(self,))
		if ( autoenable ):
			self.enable(True)
	def enable(self,toEnable:bool):
		if ( toEnable == self.__isEnabled ):
			return
		if ( toEnable ):
			self.__isEnabled = True
			self.__thread.start()
		else:
			self.__isEnabled = False
			self.__thread.join()
	def setVerbosity(self, verbosity):
		self.__verbosity = verbosity
	def getVerbosity(self):
		return self.__verbosity
	def log(self, verbosity, message, caller=None, previousFrame=None):
		if ( verbosity > self.__verbosity or self.__isEnabled == False ):
			return
		now = datetime.now()
		msEllapsedSinceStart = int(1000*time.perf_counter())-self.__start
		if ( previousFrame == None ):
			previousFrame = inspect.currentframe().f_back
		(filename, line_number, function_name, lines, index) = inspect.getframeinfo(previousFrame)
		#msgStr = Verbosity.fromIntToString(verbosity)+'\t'+str(line_number)+':'+str(index)+'\t'+now.strftime("%m/%d/%Y-%H:%M:%S")+'-'+str(msEllapsedSinceStart)+'\t'+message
		msgStr = Verbosity.fromIntToString(verbosity)+'\t'+now.strftime("%m/%d/%Y-%H:%M:%S")+'-'+str(msEllapsedSinceStart)+'\t'+Path(filename).name+'\t'+str(line_number)+':'+str(index)+'\t'+function_name+'\t'+message
		with self.__bufLock:
			self.__buf.append(msgStr)

class AnalytX:
	_defaultLogger = ConsoleLogger(Verbosity.WARNING)
def setLogger(logger):
	if ( AnalytX._defaultLogger != None ):
		AnalytX._defaultLogger.enable(False)
	AnalytX._defaultLogger = logger
	AnalytX._defaultLogger.enable(True)
	time.sleep(1.0)
def setVerbosity(verbosity, logger=None):
	if ( logger == None ):
		logger = AnalytX._defaultLogger
	logger.setVerbosity(verbosity)
def error(message, logger=None, caller=None):
	if ( logger == None ):
		logger = AnalytX._defaultLogger
	logger.log(Verbosity.ERROR, message, caller, inspect.currentframe().f_back)
def warning(message, logger=None, caller=None):
	if ( logger == None ):
		logger = AnalytX._defaultLogger
	logger.log(Verbosity.WARNING, message, caller, inspect.currentframe().f_back)
def info(message, logger=None, caller=None):
	if ( logger == None ):
		logger = AnalytX._defaultLogger
	logger.log(Verbosity.INFO, message, caller, inspect.currentframe().f_back)
def debug(message, logger=None, caller=None):
	if ( logger == None ):
		logger = AnalytX._defaultLogger
	logger.log(Verbosity.DEBUG, message, caller, inspect.currentframe().f_back)

if __name__ == '__main__':
    warning("⚠️ Nothing to run from lib "+str(__file__))