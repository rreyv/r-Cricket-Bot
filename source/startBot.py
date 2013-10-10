import praw
from createMatchThread import createMatchThreadWrapper
from getFixturesInfo import getFixturesDictionary
from createSidebar import updateSidebar
from datetime import datetime
import time
import logging
from requests.exceptions import HTTPError
from praw.errors import ExceptionList, APIException, InvalidCaptcha, InvalidUser, RateLimitExceeded
from socket import timeout
import sqlite3 as sql
from emailGlobals import sendEmail
from inboxHandler import readInbox
from liveScoreHandler import updateLiveScores


if __name__=="__main__":
	#One time setup
	r = praw.Reddit('/r/cricket sidebar updating and match thread creating bot by /u/rreyv. Version 1.0') #reddit stuff
	subredditName='cricket'
	r.login() #sign in!
	fixturesData={}
	fixturesData=getFixturesDictionary(5)
	sendEmail("Bot has begun","Yep it has")
	# SQL table init
	i=0
	#one time setup ends
	while True:
		#things that happen every four hours
		while True:
			#things that happen every 50 seconds
			updateLiveScores(r,subredditName)
			updateSidebar(fixturesData,r,subredditName)
			readInbox(r,subredditName)
			time.sleep(50)
			i+=1;
			if i%240==0:
				break
			#End of 50 second loop
		fixturesData={}
		fixturesData=getFixturesDictionary(5)
		sendEmail("Grabbing fixtures from Cricinfo","Grabbed fixtures from Cricinfo")
		i=0
		#end of four hour loop#