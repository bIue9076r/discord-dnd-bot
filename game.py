# game.py module
active_games = [];
# active game = [
#	guild: 0x012345
#	channel: 0x01234567
#	commander: [
#		{userid: 0x012345, name: "name"};
#	];
#	players: [
#		{userid: 0x012345, stats: []};
#	];
#];

agame_index = {};
# (entry) = index

def nop(v):
	return [""]

def shp(v):
	return ["Hp",int(v[0])]

def sets(v):
	return [v[0],v[1]]

ops = {
	"nop": 		nop,
	"shp":		shp,
	"set":		sets,
}

def checkDup(n):
	for i in range(len(active_games)):
		idp = (active_games[i]["commander"]["name"] == str(n))
		if (idp):
			return True;
	return False;

def checkDupPlr(i,p):
	for j in range(len(active_games[i]["players"])):
		idp = (active_games[i]["players"][j]["userid"] == str(p))
		if (idp):
			return True;
	return False;

def getIndexName(g,ch,n):
	for i in range(len(active_games)):
		isg =  (active_games[i]["guild"] == str(g))
		isch = (active_games[i]["channel"] == str(ch))
		idp = (active_games[i]["commander"]["name"] == str(n))
		if (isg and isch and idp):
			return i;
	return -1;

def getPlayerIndex(g,ch,p):
	for i in range(len(active_games)):
		isg =  (active_games[i]["guild"] == str(g))
		isch = (active_games[i]["channel"] == str(ch))
		
		for j in range(len(active_games[i]["players"])):
			idp = (active_games[i]["players"][j]["userid"] == str(p))
			if (isg and isch and idp):
				return j;
	return -1;

def getPlayerIndexName(pn,i):
	for j in range(len(active_games[i]["players"])):
		isp = (active_games[i]["players"][j]["name"] == str(pn))
		if (isp):
			return j;
	return -1;

def getIndex(g,ch,c,n):
	for i in range(len(active_games)):
		isg =  (active_games[i]["guild"] == str(g))
		isch = (active_games[i]["channel"] == str(ch))
		isc =  (active_games[i]["commander"]["userid"] == str(c))
		isn =  (active_games[i]["commander"]["name"] == str(n))
		if (isg and isch and isc and isn):
			return i;
	return -1;

def updateIndexes():
	for i in range(len(active_games)):
		ig = active_games[i]["guild"]
		ich = active_games[i]["channel"]
		ic = active_games[i]["commander"]["userid"]
		inm = active_games[i]["commander"]["name"]
		key = str(ig) + str(ich) + str(ic) + str(inm)
		
		agame_index[key] = i

def startGame(g,ch,c,n="main"):	
	if (not checkDup(n)):
		agme = {
			"guild":		str(g),
			"channel":		str(ch),
			"commander":	{
				"userid": str(c), "name": str(n)
			},
			"players":		[
				#{"userid": 0x0,"stats": []}
			],
		};
		
		active_games.append(agme)
		ag_index = getIndex(str(g),str(ch),str(c),str(n))
		
		if (ag_index > -1):
			agame_index[str(g) + str(ch) + str(c) + str(n)] = ag_index
			return [True];
		else:
			return [False,"unable to start game"];
	else:
		return [False,"duplicate game"];

def endGame(g,ch,c,n="main"):
	gchcn = str(g) + str(ch) + str(c) + str(n)
	agi = agame_index[gchcn]
	
	if(agi != None):
		tgm = active_games[agi]
		active_games.remove(tgm)
		agame_index[gchcn] = None
		updateIndexes()
		return [True];
	else:
		return [False,"no game to end"];

def joinGame(g,ch,p,n="main",pn="noob"):
	agi = getIndexName(str(g),str(ch),str(n))
	
	if(agi > -1):
		if (not checkDupPlr(agi,str(p))):
			player = {
				"userid": str(p),
				"name": str(pn),
				"stats": {},
			}
			
			active_games[agi]["players"].append(player)
			return [True];
		else:
			return [False,"you are already playing that game"]
	else:
		return [False,"no game to join"]

def quitGame(g,ch,p,n="main"):
	agi = getIndexName(str(g),str(ch),str(n))
	api = getPlayerIndex(str(g),str(ch),str(p))
	
	if(agi > -1):
		if(api > -1):
			player = active_games[agi]["players"][api]
			
			active_games[agi]["players"].remove(player)
			return [True];
		else:
			return [False,"you are not playing that game"]
	else:
		return [False,"no game to quit"]

def act(g,ch,op="nop",v=[0],n="main",pn="noob"):
	if(not(op in ops)):
		return [False, "Invalid operation"]
	agi = getIndexName(str(g),str(ch),str(n))
	if(agi < 0):
		return [False,"you are not hosting that game"]
	api = getPlayerIndexName(str(pn),agi)
	if(api < 0):
		return [False,"that player is not in the party"]
	res = ops[op](v)
	
	if (len(res) != 0 and res[0] != ""):
		active_games[agi]["players"][api]["stats"][res[0]] = res[1]
	
	return [True];

def stats(g,ch,n="main",pn="noob"):
	agi = getIndexName(str(g),str(ch),str(n))
	if(agi < 0):
		return [False,"that game does not exist"];
	api = getPlayerIndexName(str(pn),agi)
	if(api < 0):
		return [False,"that player is not in the party"];
	
	return [True,active_games[agi]["players"][api]["stats"]];	

def players(g,ch,n="main"):
	agi = getIndexName(str(g),str(ch),str(n))
	if(agi < 0):
		return [False,"that game does not exist"];
	
	return [True,active_games[agi]["players"]];
