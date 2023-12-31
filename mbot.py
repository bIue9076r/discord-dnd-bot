import json
import os.path
import discord
import roll
import game
import load
import save

tok = str(open('tok.txt').read())
GSAVEPATH = './saves/index.txt'

intents = discord.Intents.default()
intents.message_content = True
intents.emojis = True

client = discord.Client(intents=intents)

# global tables
prefixes = [
	"~","+","!",
	"=","$",
	"%","&",
	"-",":",
	".","?",
	"\\","/","]",
	"|","}"
]

def splitStr(s):
	ret = [""]
	o = ""
	index = 0
	literal = False
	escape = False
	
	for i in range(0,len(s)):
		if (s[i] == " " and not literal):
			if (o != ""):
				o = ""
				ret.append("")
				index = index + 1
		elif (s[i] == '\\' and not escape):
			escape = True
		elif (s[i] == '"' and not escape):
			literal = not literal
		else:
			o = o + s[i]
			ret[index] = o
			escape = False
	
	return ret;

def dictlog(d):
	print(json.dumps(d, indent=4))

def f_splitStr(s):
	tret = [0,None]
	ret = [""]
	to = [None]
	o = ""
	tindex = 1
	index = 0
	literal = False
	
	for i in range(0,len(s)):
		if(i == len(s) - 1 and s[i] == "\n"):
			break;
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

async def b_help(message,args):
	await message.channel.send(
	"```txt\n"+
	"echo:    ~echo    ...\n"+
	"echok:   ~echok   ...\n"+
	"about:   ~about\n"+
	"save:    ~save <file> <game>\n"
	"load:    ~load <file>"
	"games:   ~games\n"+
	"start:   ~start   <name>\n"+
	"end:     ~end     <game>\n"+
	"join:    ~join    <game> <name>\n"+
	"quit:    ~quit    <game>\n"+
	"roll:    ~roll    <dice>\n"+
	"action:  ~action  <game> <name> <op> <vars> ...\n"+
	"stats:   ~stats   <game> <name>\n"+
	"players: ~players <game>\n\naliases:\n"+
	"h:       alias of help\n"+
	"g:       alias of games\n"+
	"s:       alias of start\n"+
	"e:       alias of end\n"+
	"j:       alias of join\n"+
	"q:       alias of quit\n"+
	"r:       alias of roll\n"+
	"a:       alias of action\n"+
	"st:      alias of stats\n"+
	"p:       alias of players\n"+
	"```"
	)

async def b_help_d(message,args):
	await message.channel.send("comand in progress")
	await b_help(message,args)

async def b_echo(message,args):
	if (len(args) < 1):
		await message.channel.send("Usage: ~echo ...")
		return;
	p = ""
	for i in range(0,len(args)):
		p = p + args[i] + " "
	await message.channel.send(p)
	await message.delete()

async def b_echo_k(message,args):
	if (len(args) < 1):
		await message.channel.send("Usage: ~echo ...")
		return;
	p = ""
	for i in range(0,len(args)):
		p = p + args[i] + " "
	await message.channel.send(p)

async def b_about(message,args):
	await message.channel.send(
	f"```txt\n"+
	f"Version:   2.0 (Save & Load)\n"+
	f"Prefixes:  ~!=#$%&-.>?\n"+
	f"user:      {client.user}\n"+
	f"channel:   {message.channel.id}\n"+
	f"guild:     {message.guild.id}\n"+
	f"```"
	)

async def b_save(message,args):
	if (len(args) < 2):
		await message.channel.send("Usage: ~save <file> <game>")
		return;
	
	mg = message.guild.id
	mch = message.channel.id
	
	if(args[1] == "ALL" or args[1] == "all"):
		await message.channel.send(f"Attempting to save games at \"{args[0]}\"")
		ret = save.G_save(args[0])
		if(ret[0]):
			await message.channel.send(f"Saved all games at \"{args[0]}\"")
		return;
	
	await message.channel.send(f"Attempting to save \"{args[1]}\" at \"{args[0]}\"")
	save.startSave(args[0])
	ret = save.saveGame(mg,mch,args[0],args[1])
	save.closeSave(args[0])
	if(ret[0]):
		await message.channel.send(f"Saved \"{args[1]}\" at \"{args[0]}\"")
	return;

async def b_load(message,args):
	if (len(args) < 1):
		await message.channel.send("Usage: ~load <file>")
		return;
	
	await message.channel.send(f"Attempting to load \"{args[0]}\"")
	l_f = open(args[0],'r+')
	f_pmes(str(l_f.read()))
	await message.channel.send(f"Loaded \"{args[0]}\"")
	return;

async def b_start(message,args):
	if (len(args) < 1):
		await message.channel.send("Usage: ~start <name>")
		return;
	mg = message.guild.id
	mch = message.channel.id
	ma = message.author.id
	mn = args[0]
	
	res = game.startGame(mg,mch,ma,mn)
	if(res[0]):
		await message.channel.send(f"Game created ({mn})\nCommander: {message.author}")
	else:
		await message.channel.send(f"Game Not created: {res[1]}")

async def b_end(message,args):
	if (len(args) < 1):
		await message.channel.send("Usage: ~end <name>")
		return;
	mg = message.guild.id
	mch = message.channel.id
	ma = message.author.id
	mn = args[0]
	
	res = game.endGame(mg,mch,ma,mn)
	if(res[0]):
		await message.channel.send(f"Game ended ({mn})")
	else:
		await message.channel.send(f"Game Not ended: {res[1]}")

async def b_join(message,args):
	if (len(args) < 2):
		await message.channel.send("Usage: ~join <game> <name>")
		return;
	mg = message.guild.id
	mch = message.channel.id
	ma = message.author.id
	mn = args[0]
	pn = args[1]
	
	res = game.joinGame(mg,mch,ma,mn,pn)
	if(res[0]):
		await message.channel.send(f"Game joined ({mn}) as {pn}")
	else:
		await message.channel.send(f"Game Not joined: {res[1]}")

async def b_quit(message,args):
	if (len(args) < 1):
		await message.channel.send("Usage: ~quit <name>")
		return;
	mg = message.guild.id
	mch = message.channel.id
	ma = message.author.id
	mn = args[0]
	
	res = game.quitGame(mg,mch,ma,mn)
	if(res[0]):
		await message.channel.send(f"Game quit ({mn})")
	else:
		await message.channel.send(f"Game Not quit: {res[1]}")

async def b_games(message,args):
	mg = message.guild.id
	mch = message.channel.id
	s = "```txt\n"
	n = "No current games\n"
	for i in range(len(game.active_games)):
		isg = (game.active_games[i]["guild"] == str(mg))
		isch = (game.active_games[i]["channel"] == str(mch))
		if(isg and isch):
			ind = game.active_games[i]
			s = s + f"{ind['commander']['name']}: {len(ind['players'])} players\n"
	
	if (s == "```txt\n"):
		s = s + n
	
	s = s + "\n```"
	await message.channel.send(s)

async def b_roll(message,args):
	if (len(args) < 1):
		await message.channel.send("Usage: ~roll <dice>")
		return;
	# types of inputs
	# NdNxN
	res = roll.parse_ndnxn(args[0])
	
	if (res[0]):
		ret = 0
		for i in range(res[3]):
			ret = ret + (roll.roll(res[2]) * res[1])
		
		await message.channel.send(f"{args[0]} returns {ret}")
	else:
		await message.channel.send(f"Failed to roll: {res[1]}")

async def b_act(message,args):
	if (len(args) < 3):
		await message.channel.send("Usage: ~action <game> <name> <op> <vars> ...")
		return;
	
	mg = message.guild.id
	mch = message.channel.id
	
	res = game.act(mg,mch,args[2],args[3:],args[0],args[1])
	if(not res[0]):
		await message.channel.send(f"{res[1]}")
		return;
	await message.channel.send(f"{args[2]} completed")

async def b_stats(message,args):
	if (len(args) < 2):
		await message.channel.send("Usage: ~stats <game> <name>")
		return;
	mg = message.guild.id
	mch = message.channel.id
	mgn = args[0]
	mpn = args[1]
	
	s = f"```txt\n\"{mpn}\" stats:\n"
	
	res = game.stats(mg,mch,mgn,mpn)
	
	if(not res[0]):
		await message.channel.send(f"{res[1]}")
		return;
		
	for x in res[1]:
		s = s + f"{x}: {res[1][x]}\n"
	
	s = s + "\n```"
	await message.channel.send(s)

async def b_players(message,args):
	if (len(args) < 1):
		await message.channel.send("Usage: ~players <game>")
		return;
	mg = message.guild.id
	mch = message.channel.id
	mgn = args[0]
	
	s = f"```txt\n\"{mgn}\" players:\n"
	
	res = game.players(mg,mch,mgn)
	
	if(not res[0]):
		await message.channel.send(f"{res[1]}")
		return;
	
	for x in range(len(res[1])):
		s = s + f"{res[1][x]['name']}\n"
	
	s = s + "\n```"
	await message.channel.send(s)


async def d_data(message,args):
	dictlog(game.active_games)
	print("\n")
	dictlog(game.agame_index)
	
	await message.delete()

cmds = {
	"help":		b_help,
	"echo":		b_echo,
	"echok":	b_echo_k,
	"about":	b_about,
	"save":		b_save,
	"load":		b_load,
	"start":	b_start,
	"end":		b_end,
	"join":		b_join,
	"quit":		b_quit,
	"games":	b_games,
	"roll":		b_roll,
	"action":	b_act,
	"stats":	b_stats,
	"players":	b_players,
	"s":		b_start,
	"e":		b_end,
	"j":		b_join,
	"q":		b_quit,
	"g":		b_games,
	"r":		b_roll,
	"a":		b_act,
	"p":		b_players,
	"st":		b_stats,
	"h":		b_help,
	"heal":		b_help_d,
	"hurt":		b_help_d,
	"debug":	d_data,
}

f_cmds = {
	"f_set":	load.f_set,
	"f_load":	load.f_load,
	"f_flags":	load.f_flags,
	"f_log":	load.f_log,
	"f_end":	load.f_end,
}

async def pmes(message):
	if (message.content[0] in prefixes):
		mtbl = splitStr(message.content[1:])
		comand = mtbl[0]	# string
		args = mtbl[1:]		# table
		
		if (comand in cmds):
			await cmds[comand](message,args)
		else:
			await message.channel.send(f"invalid command")

def f_pmes(data):
	mtbl = f_splitStr(data)
	cmlen = mtbl[0]
	comands = mtbl[1:]	# string tables
	
	for i in range(0,cmlen):
		if (comands[i][0] in f_cmds):
			args = comands[i][1:]		# string tables table
			f_cmds[comands[i][0]](args)

@client.event
async def on_ready():
	if(os.path.isfile(GSAVEPATH)):	# if global save
		mindex = open(GSAVEPATH,'r+')
		f_pmes(str(mindex.read()))
	
	print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
	if (message.author == client.user):
		return;
	
	await pmes(message)

client.run(tok)
