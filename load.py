# load.py module
import game
import json
FLAGS = [
	0,		# load flag
]

def f_log(v):
	print(v[0])

def f_set(v):
	FLAGS[int(v[0])] = int(v[1])

def f_load(v):
	pass

def f_flags(v):
	print(str(FLAGS))
