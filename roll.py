import random

def parse_ndnxn(nota):
	ind = -1
	dup = False
	for i in range(len(nota)):
		if (nota[i] == "d" or nota[i] == "D"):
			if (not dup):
				dup = True
				ind = i
			else:
				return [False,"Duplicate d/D"]
	
	if (ind == -1):
		return [False,"Invalid dice notation"]
	
	# NdNxN breaks into
	# [N,NxN]
	
	fir = nota[:ind]
	sec = nota[ind+1:]
	
	if (ind == 0):
		fir = "1"
	
	ind = -1
	dup = False
	for i in range(len(sec)):
		if (sec[i] == "x" or sec[i] == "X"):
			if (not dup):
				dup = True
				ind = i
			else:
				return [False,"Duplicate x/X"]
	
	dmul = int(fir)
	if (ind == -1):
		d = int(sec)
		mul = 1
	else:
		d = int(sec[:ind])
		mul = int(sec[ind+1:])
	
	return [True,dmul,d,mul]

def roll(dice=6):
	return random.randint(1,dice)
