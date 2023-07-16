# save.py module
import game

def startSave(f="./save.txt"):
	file = open(f,'w+')
	file.write("f_set 0 1\nf_set 1 1")
	file.close()
	return [True, "Started File"]

def closeSave(f="./save.txt"):
	file = open(f,'a+')
	file.write("\nf_end")
	file.close()
	return [True, "Finished File"]

def G_save(f="./save.txt"):
	startSave(f)
	for i in game.active_games:
		g = i["guild"]
		ch = i["channel"]
		n = i["commander"]["name"]
		saveGame(g,ch,f,n)
	
	closeSave(f)
	return [True, "Saved All"]

def saveGame(g,ch,f="./save.txt",n="main"):
	agi = game.getIndexName(str(g),str(ch),str(n))
	if(agi < 0):
		return [False,"that game does not exist"];
	
	c = game.active_games[agi]["commander"]["userid"]
	
	file = open(f,'a+')
	file.write(f"\nf_load game {g} {ch} {c} {n}")
	file.close()
	
	for i in game.active_games[agi]["players"]:
		savePlayer(g,ch,f,n,i["name"])
	
	return [True, "Saved Game"]

def savePlayer(g,ch,f="./save.txt",n="main",pn="noob"):
	agi = game.getIndexName(str(g),str(ch),str(n))
	if(agi < 0):
		return [False,"that game does not exist"];
	api = game.getPlayerIndexName(str(pn),agi)
	if(api < 0):
		return [False,"that player is not exist"];
	
	p = game.active_games[agi]["players"][api]["userid"]
	
	file = open(f,'a+')
	file.write(f"\nf_load player {g} {ch} {p} {n} {pn}")
	file.close()
	
	for i in game.active_games[agi]["players"][api]["stats"]:
		saveStat(g,ch,f,n,pn,i)
	
	return [True, "Saved player"]

def saveStat(g,ch,f="./save.txt",n="main",pn="noob",s="hp"):
	agi = game.getIndexName(str(g),str(ch),str(n))
	if(agi < 0):
		return [False,"that game does not exist"];
	api = game.getPlayerIndexName(str(pn),agi)
	if(api < 0):
		return [False,"that player is not exist"];
	
	v1 = str(s)
	v2 = game.active_games[agi]["players"][api]["stats"][str(s)]
	
	file = open(f,'a+')
	file.write(f"\nf_load stat {g} {ch} {v1} {v2} {n} {pn}")
	file.close()
	return [True, "Saved stat"]
	