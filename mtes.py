import load

def f_splitStr(s):
	tret = [0,None]
	ret = [""]
	to = [None]
	o = ""
	tindex = 1
	index = 0
	literal = False
	
	for i in range(0,len(s)):
		if (s[i] == "\n" and not literal):
			if (to != None and o != ""):
				o = ""
				ret = [""]
				index = 0
				to = [None]
				tret.append(None)
				tindex = tindex + 1
				tret[0] = tindex
		elif (s[i] == " " and not literal):
			if (o != ""):
				o = ""
				ret.append("")
				index = index + 1
		elif (s[i] == '"'):
			literal = not literal
		else:
			o = o + s[i]
			ret[index] = o
			to = ret
			tret[tindex] = to
			escape = False
	
	return tret;

f_cmds = {
	"f_set":	load.f_set,
	"f_load":	load.f_load,
	"f_flags":	load.f_flags,
	"f_log":	load.f_log,
}

def f_pmes(data):
	mtbl = f_splitStr(data)
	cmlen = mtbl[0]
	comands = mtbl[1:]	# string tables
	
	for i in range(0,cmlen):
		if (comands[i][0] in f_cmds):
			args = comands[i][1:]		# string tables table
			f_cmds[comands[i][0]](args)
	

mindex = open('./index.txt','a+')
#mindex.seek(0)
#print(f_splitStr(str(mindex.read())))

mindex.seek(0)
f_pmes(mindex.read())

load.game.startGame(0x1,0x12,0x1,"main")
# f_load <type>game <guild>g <channel>ch <commander>c <name>n

load.game.joinGame(0x1,0x12,0x2,"main","noob")
# f_load <type>player <guild>g <channel>ch <playerid>p <name>n <player_name>pn

load.game.act(0x1,0x12,"set",["l",100],"main","noob")
# f_load <type>stat <guild>g <channel>ch <value>v1 <value>v2 <name>n <player_name>pn
print(load.game.active_games)