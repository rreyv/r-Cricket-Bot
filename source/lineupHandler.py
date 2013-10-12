import praw
from datetime import datetime
import time
import logging
from requests.exceptions import HTTPError
from praw.errors import ExceptionList, APIException, InvalidCaptcha, InvalidUser, RateLimitExceeded
import sqlite3 as sql
from emailGlobals import sendEmail

def updateLineups(r):
	#TwelveHourOldMatches
	#figure out matches you need to update the lineup for
		updateLineUpPerThread(matchThreadId)
		pass

def updateLineupPerThread(matchThreadId):
	#get selftext from matchthread
	teamOneName,teamOnePlayers=extractTeamInfo(selftext,1)
	teamTwoName,teamTwoPlayers=extractTeamInfo(selftext,2)
	teamOneTable=teamOneName+"|M|R|HS|Avg|100|Wkt|BBI|Bowl Av.|5|Ct|St|"+teamOneName+"(v. )"+teamTwoName+"|M|R|HS|Avg|100|Wkt|BBI|Bowl Av.|5|Ct|St|\n"
	teamOneTable=teamOneTable+"|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|\n"
	teamTwoTable=teamTwoName+"|M|R|HS|Avg|100|Wkt|BBI|Bowl Av.|5|Ct|St|"+teamTwoName+"(v. )"+teamOneName+"|M|R|HS|Avg|100|Wkt|BBI|Bowl Av.|5|Ct|St|\n"
	teamTwoTable=teamTwoTable+"|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|\n"
	for player in teamOnePlayers:
		teamOneTable=teamOneTable+returnStatsPerPlayer(player,teamTwoName,format)+"\n"
	for player in teamTwoPlayers:
		teamTwoTable=teamTwoTable+returnStatsPerPlayer(player,teamTwoName,format)+"\n"


def returnStatsPerPlayer(playerId,oppositionTeamName,format):
	country_codes = {
	'afghanistan' : 40,
	'australia' : 2,
	'bangladesh' : 25,
	'bermuda' : 12,
	'england' : 1,
	'hong kong' : 19,
	'india' : 6,
	'ireland' : 29,
	'netherlands' : 15,
	'new zealand' : 5,
	'pakistan' : 7,
	'scotland' : 30,
	'south africa' : 3,
	'sri lanka' : 8,
	'west indies' : 4,
	'zimbabwe' : 9
	}
	formats = {
	'tests' : 1,
	'odis' : 2,
	't20is' : 3,
	'test' : 1,
	'odi' : 2,
	't20i' : 3,
	}
	
	base_url='http://http://stats.espncricinfo.com/stats/engine/player/'
	url = playerId + ".html?" + base_url + 'class='+formats(format)+';opposition='+country_codes(oppositionTeamName.lower())+";template=results;type=allround"
	soup = returnSoup(url)
def extractTeamInfo(selftext,teamNumber):
	teamOneName=getTeamName(selftext)