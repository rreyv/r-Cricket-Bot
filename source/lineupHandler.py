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
		updateLineUpPerThread(matchThreadId,liveThreadId)
		pass

def updateLineupPerThread(matchThreadId,liveThreadId):
	teamOneInfo=extractTeamInfo(selftext,1)
	teamTwoInfo=extractTeamInfo(selftext,2)
	pass

def returnStatsPerPlayer(playerId,oppositionTeamName):
	pass

def extractTeamInfo(selftext,teamNumber):
	