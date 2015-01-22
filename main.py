from lib.betaseries import *

B = BetaSeries()
B.key = '245d8c3b4a91'
l = Show.search('Dexter')
print(l)
s = l[0].get_episode()._get_subtitles()[0]
s.download()
s.extract()
