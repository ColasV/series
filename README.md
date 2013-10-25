BetaSeries
======
BetaSeries is a tiny library to use the BetaSeries API in Python.

You can find the site here : http://www.betaseries.com

With this library you can :
- search in BetaSeries database in order to find shows.
- get informations about a specific show.
- download subtitle.

How to start
=============

1. First you need to instance a new BetaSeries object :

>>> B = BetaSeries('yourbetaserieskey')

2. Second you can call a class, example search a show :

>>> result = B.search('dexter')

3. You get your first search object which contain the title and the show url

>>> result.title 
'Dexter'
>>> result.url
'dexter'

Next TO-DO
===========
- Gérer les différents cas d'archives