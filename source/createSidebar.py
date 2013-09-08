import praw
from createMatchThread import createMatchThreadWrapper
from getFixturesInfo import getFixturesDictionary
from datetime import datetime
import time
import logging
from requests.exceptions import HTTPError
from praw.errors import ExceptionList, APIException, InvalidCaptcha, InvalidUser, RateLimitExceeded
from socket import timeout
from emailGlobals import sendEmail


def MakeRedditTable(fixturesData,r,subreddit):
	table="Upcoming Matches:\n\nMatch|Time Left\n:---|:---\n"	#begin table.
	for i in fixturesData:
		matchTime = fixturesData[i]['Time']	#get match time
		currentGMT = datetime.utcnow()	#get UTC time
		timeDifference = matchTime - currentGMT	#get time difference
		DisplayText=fixturesData[i]['ColumnTitle']
		if len(DisplayText)>30:
			DisplayText=DisplayText.split(",")[0]
		if (timeDifference.total_seconds()<=3600 and timeDifference.total_seconds()>=3400):
			ReturnValue,ReturnText=createMatchThreadWrapper(r,"Match thread: "+fixturesData[i]['MatchText'],fixturesData[i]['Link'],'rCricketBot',subreddit)
		if timeDifference.total_seconds()>0:	#if the match is yet to begin
			timeDifference=str(timeDifference)	#convert to string to get out relevant information
			if timeDifference.find("day")!=-1:	#if the string has the word 'day' in it, we'll have to create the 'D' segment
				days=(timeDifference.split(" ")[0] + "D ")	#get the days
				timeStr=timeDifference.split(" ")[2]	#get the time portion. When there is a day section, the time portion is the third segment
			else:
				days="" #if there's no days, there's no "D"
				timeStr=timeDifference #and the entire timeDifference string is just time
			Hours=(timeStr.split(":")[0] + "H ") #get hours
			Minutes=(timeStr.split(":")[1] + "M ") #get minutes
			timeStr=days + Hours + Minutes
			if 'Link' in fixturesData[i]:
				timeStr='['+timeStr+']('+fixturesData[i]['Link']+')'
			table=table+DisplayText+"|"+timeStr+"\n" #add it to the table string
		elif 'Link' in fixturesData[i]: #else if the match has begun, check if we have a live match link for it
			table=table+DisplayText+"|"+"[Live!]("+fixturesData[i]['Link']+")"+"\n" #if we do, add it to the match table
		else:
			table=table+DisplayText+"|"+"Live!"+"\n" #no match link, no link in the sidebar table
	table=table+"\n[More Fixtures](http://www.espncricinfo.com/ci/content/match/fixtures/index.html?days=30)"	#end of table. This is what the EndOfTableMarker searches for
	return table



def updateSidebar(fixturesData,r,subredditName):
	newTable=MakeRedditTable(fixturesData,r,subredditName)
	EndOfTableMarker="[More Fixtures](http://www.espncricinfo.com/ci/content/match/fixtures/index.html?days=30)" #Signature to look for that marks the end of table
	BeginningOfTableMarker="Upcoming Matches:"	#Signature to look for that marks beginning of table
	try:
		settings=r.get_settings(subredditName)
		description=settings['description']
		descriptionBegin=description.find(BeginningOfTableMarker)
		descriptionEnd=description.find(EndOfTableMarker) + len(EndOfTableMarker)
		description=description[:descriptionBegin] + newTable + description[descriptionEnd:]
		settings=r.get_subreddit(subredditName).update_settings(description=description)
	except:
		sendEmail("We've got a problem","Couldn't update sidebar, trying again in 60 seconds....")

