import os
from betaseries import *

file_name = '108-Argentina.mkv'
new_dir = r'/Volumes/DD2/Videos/Series/Dexter/Saison 1/'

listF = os.listdir(new_dir)

def parseurfile(file_name):
	
	info = file_name.split("-")
	episode = 0
	tr = 0
	season = 0
	# Premiere partie contient le numero
	# Deuxieme le nom de l'episode
	nb = info[0]
	lon = len(nb)
	if lon == 3:
		episode = int(nb[1])*10 + int(nb[2])
		season = int(nb[0])
	elif lon == 4:
		episode = int(nb[2])*10 + int(nb[3])
		season = int(nb[0])*10 + int(nb[1])
	else:
		print('Format non reconnu')
		


	return episode,season

B = BetaSeries('')
for f in listF:
	var = f.split('.')
	print(var)
	if var[-1] == 'avi' or var[-1] == 'mkv':
		episode,season = parseurfile(f)
		
		obj = B.getSubtitle('dexter',season,episode)
		name_srt = obj['0'].download(new_dir)
		os.rename(new_dir + name_srt,str(new_dir) + str(f) + '.srt')
	

