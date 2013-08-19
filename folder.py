import os

# Little function which get the season and episod number
# Support format : SSEE-Name or SEE-Name like 108 for season 1 episode 8
def parseurfile(file_name):
	try:
		info = file_name.split(" ")
		new_file_name = "".join(info)
		info = new_file_name.split("-")
		episode = 0
		season = 0
		nb = info[0]
		length = len(nb)
		if length == 3:
			episode = int(nb[1])*10 + int(nb[2])
			season = int(nb[0])
		elif length == 4:
			episode = int(nb[2])*10 + int(nb[3])
			season = int(nb[0])*10 + int(nb[1])
		else:
			print('Format non reconnu')
		
		# return episode and season number
		return episode,season
	except Exception as err:
		print('Fichier non pris en charge')

# Allow you to easily change a extension format for a file
def changeExtension(file_name,new_extension):
	info = file_name.split(".")
	info[-1] = new_extension
	new_file_name = ".".join(info)

	return new_file_name



