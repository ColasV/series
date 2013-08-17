# Example 1:
# How to use the API

# Import the library
from betaseries import *

# Create an object with the API key
B = BetaSeries('245d8c3b4a91')

# Search for a serie in the database:
# Look at all the shows with the keyword
result = B.search('NCIS')
for i in result:
	print(i['title'])

print("\n")

# Specific search:
# return a dictionnary with two element url and title
result_specific = B.searchSpecific('NCIS')
print(result_specific['title'])

# Get a show informations
# Need a show url
# Return a Show object
result_show = B.getShow(result_specific['url'])
print('Title : ' + result_show.title + "\n")
print('Description : ' + result_show.description)

# Download a subtitle
# Need the url show, season number, episode number and optionnal (VO|VF)
result_subtitle = B.getSubtitle(result_specific['url'],1,1,'VO')

# Get a list of Subtitle object
# Try to download the first one
# Download and unzip in your script folder
print ('Downloading : ' + result_subtitle[0].name)
result_subtitle[0].download()