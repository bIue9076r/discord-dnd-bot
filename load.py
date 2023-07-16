# load.py module
import game
import json
FLAGS = [
	0,		# load flag
	1,		# version
]

def f_end(v):
	pass # empty function to signal EOF

def f_log(v):
	print(v[0])

def f_set(v):
	FLAGS[int(v[0])] = int(v[1])

def f_load(v):
	f_type = v[0]
	if(f_type == "game"):
		# f_load <type>game <guild> <channel> <commander> <name>
		
		f_g = v[1]	# <guild>
		f_ch = v[2]	# <channel>
		f_c = v[3]	# <commander>
		f_n = v[4]	# <name>
		
		game.startGame(f_g,f_ch,f_c,f_n)
	elif(f_type == "player"):
		# f_load <type>player <guild> <channel> <playerid> <name> <player_name>
		
		f_g = v[1]	# <guild>
		f_ch = v[2]	# <channel>
		f_p = v[3]	# <playerid>
		f_n = v[4]	# <name>
		f_pn = v[5]	# <player_name>
		
		game.joinGame(f_g,f_ch,f_p,f_n,f_pn)
	elif(f_type == "stat"):
		# f_load <type>stat <guild> <channel> <value> <value> <name> <player_name>
		
		f_g = v[1]	# <guild>
		f_ch = v[2]	# <channel>
		f_v1 = v[3]	# <value>
		f_v2 = v[4]	# <value>
		f_n = v[5]	# <name>
		f_p = v[6]	# <playerid>
		
		game.act(f_g,f_ch,"set",[f_v1,f_v2],f_n,f_p)

def f_flags(v):
	print(str(FLAGS))
