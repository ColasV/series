# Example 1:
# How to use the API

# Import the library
from betaseries import *

# Create an object with the API key
B = BetaSeries('245d8c3b4a91')

# Search for a serie in the database:
# Look at all the shows with the keyword
result = B.search_keyword('NCIS')
for i in result:
	print(i['title'])

print("\n")

# Specific search:
# return a dictionnary with two element url and title
result_specific = B.search('NCIS')
print(result_specific.title)

# Get a show informations
# Need a show url
# Return a Show object
result_show = B.get_show(result_specific.url)
print(result_show)
print('Description : ' + result_show.description)


# Download a subtitle
# Need the url show, season number, episode number and optionnal (VO|VF)
result_subtitle = B.get_subtitle(result_specific.url,1,1,SUB_FR)

# Get a list of Subtitle object
# Try to download the first one
# Download and unzip in your script folder
print ('Downloading : ' + result_subtitle[0].name)
result_subtitle[0].download()

# Get information about one episode
# Return an episode object
# Implement a str method
result_episode = B.get_episode('dexter',8,1)
print(result_episode)
print(result_episode.description)
