import j2l.pytactx.agent as pytactx

agent = pytactx.Agent(playerId=input("👾 id: "),
						arena=input("🎲 arena: "),
						username="demo",
						password=input("🔑 password: "),
						server="mqtt.jusdeliens.com",
						verbosity=2)

def onAmmoChange(evSrc, evType, ammoBefore, ammoAfter):
	"""Play melody on fire"""
	if ( ammoBefore > ammoAfter ):
		agent.robot.playMelody([(freq,2) for freq in range(2000,200,-100)])
agent.addEventListener("ammo",onAmmoChange)

def onLifeChange(evSrc, evType, lifeBefore, lifeAfter):
	"""Play melody on lifes perdues"""
	if ( lifeBefore > lifeAfter ):
		agent.robot.playMelody([(tone,25) for tone in range(10,2,-1)])
agent.addEventListener("life",onLifeChange)

def onRobotConnected(evSrc, evType, nExeBefore, nExeAfter):
	"""Play melody on new run"""
	agent.robot.playMelody([('E4',30),('G4',30),('C5',30),('G4',30),('C5',30),('E5',30),('C5',30),('E5',30),('G5',30),('C6',30)])
agent.addEventListener("nExe",onRobotConnected)

while True:
	agent.lookAt((agent.orientation + 1) % 4)
	agent.update()