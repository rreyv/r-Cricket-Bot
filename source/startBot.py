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


if __name__=="__main__":
	#One time setup
	r = praw.Reddit('/r/cricket sidebar updater and match thread creator bot by /u/rreyv') #reddit stuff
	subredditName='rreyv'
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
			#things that happen every 45 seconds
			updateSidebar(fixturesData,r,subredditName)
			readInbox(r)
			time.sleep(45)
			i+=1;
			if i%240==0:
				break
			#End of 45 second loop
		fixturesData={}
		fixturesData=getFixturesDictionary(5)
		sendEmail("Grabbing fixtures from Cricinfo","Grabbed fixtures from Cricinfo")
		i=0
		#end of four hour loop#