# Example 2:
# Take a directory path
# For each folder, check if the name exist on the database (same name)
# Produce a html report with all the shows + description + banner

from lib.betaseries import *
import os

B = BetaSeries()
B.key = '245d8c3b4a91'
new_dir = r'/Volumes/DD2/Videos/Series/'

listF = os.listdir(new_dir)

F = open('content.html','w')	
F.write('<html><head><meta charset="utf-8"></head><body>')
for i in listF:
	new_p = new_dir + i
	
	if not os.path.isfile(new_p):
		answer = B.search(i)
		
		if answer != None:
			# Print debug 
			print(answer.title)

			# Write in html file
			F.write('<h1>' + str(answer.title) + '</h1>')
			val = B.get_show(answer.url)
			F.write('<p>' + str(val.description) + '</p>')
			F.write('<img src="' + str(val.banner) + '" />')

F.write('</body></html>')
F.close()