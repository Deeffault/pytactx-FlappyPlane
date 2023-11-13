import j2l.pytactx.agent as pytactx

agent = pytactx.AgentFr(nom=input("👾 id: "), arene="TheMatrX", username="demo",password=input("🔑 password: "), url="mqtt.jusdeliens.com", verbosite=3)

while True:
	agent.orienter((agent.orientation+1)%4)
	agent.actualiser()