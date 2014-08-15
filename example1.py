# Example 1:
# How to use the API

# Import the library
from betaseries import *

# Create an object with the API key
B = BetaSeries()
B.key = '245d8c3b4a91'

# Search for a serie in the database:
# Look at all the shows with the keyword
result = Show.search('Dexter')
for i in result:
    print(i.data['title'])

print("\n")


