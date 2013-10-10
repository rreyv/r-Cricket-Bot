import praw
from datetime import datetime
from requests.exceptions import HTTPError
from praw.errors import ExceptionList, APIException, InvalidCaptcha, InvalidUser, RateLimitExceeded
from socket import timeout
import sqlite3 as sql
from emailGlobals import sendEmail
from inboxHandler import readInbox


def updateLiveScores(r,subredditName):
	#get list of currently running matches
	#loop over currently running matches:
		#matchScoreUpdater(r,subredditName,matchId)
	pass

def matchScoreUpdater(r,subredditName,matchId):
	#from matchId, get the live thread hyperlink
	liveThreadLink='http://www.espncricinfo.com/bangladesh-v-new-zealand-2013-14/engine/match/668949.html'
	desktopScorecardLink=getDesktopScorecardLink(liveThreadLink)
	liveScoreText=getLiveScoreText(desktopScorecardLink)
	updateMatchThread(r,subredditName,matchId,liveScoreText)

def getDesktopScorecardLink(liveThreadLink):
	return liveThreadLink+'?template=desktop'

def updateMatchThread(r,subredditName,matchId,liveScoreText):
	pass

def getLiveScoreText(desktopScorecardLink):
	pass