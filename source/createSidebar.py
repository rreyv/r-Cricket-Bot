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


def MakeRedditTable(fixturesData,r):
	table="Upcoming Matches:\n\nMatch|Time Left\n:---|:---\n"	#begin table.
	for i in fixturesData:
		matchTime = fixturesData[i]['Time']	#get match time
		currentGMT = datetime.utcnow()	#get UTC time
		timeDifference = matchTime - currentGMT	#get time difference
		DisplayText=fixturesData[i]['ColumnTitle']
		if len(DisplayText)>30:
			DisplayText=DisplayText.split(",")[0]
		if (timeDifference.total_seconds()<=3600 and timeDifference.total_seconds()>=3520):
			createMatchThreadWrapper(r,"Match thread: "+fixturesData[i]['MatchText'],fixturesData[i]['Link'])
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
			table=table+DisplayText+"|"+"[Live Now!]("+fixturesData[i]['Link']+")"+"\n" #if we do, add it to the match table
		else:
			table=table+DisplayText+"|"+"Live Now!"+"\n" #no match link, no link in the sidebar table
	table=table+"\n[More Fixtures](http://www.espncricinfo.com/ci/content/match/fixtures/index.html?days=30)"	#end of table. This is what the EndOfTableMarker searches for
	return table



def updateSidebar(fixturesData,r,subredditName):
	newTable=MakeRedditTable(fixturesData,r)
	# except blocks stolen from reddit post
	EndOfTableMarker="[More Fixtures](http://www.espncricinfo.com/ci/content/match/fixtures/index.html?days=30)" #Signature to look for that marks the end of table
	BeginningOfTableMarker="Upcoming Matches:"	#Signature to look for that marks beginning of table
	try:
		settings=r.get_settings(subredditName)
		description=settings['description']
		descriptionBegin=description.find(BeginningOfTableMarker)
		descriptionEnd=description.find(EndOfTableMarker) + len(EndOfTableMarker)
		description=description[:descriptionBegin] + newTable + description[descriptionEnd:]
		settings=r.get_subreddit(subredditName).update_settings(description=description)
		time.sleep(60)
	except APIException as e:
		time.sleep(30)
	except ExceptionList as el:
		time.sleep(30)
	except (HTTPError, RateLimitExceeded) as e:
		time.sleep(30)
	except timeout:
		time.sleep(30)
	except Exception as e:
		sendEmail("Subject","Text")


# if __name__ == "__main__":
# 	r = praw.Reddit('/r/cricket sidebar updater bot by /u/rreyv') #reddit stuff
# 	subredditName='rreyv'
# 	r.login() #sign in!
# 	fixturesData={}
# 	EndOfTableMarker="[More Fixtures](http://www.espncricinfo.com/ci/content/match/fixtures/index.html?days=30)" #Signature to look for that marks the end of table
# 	BeginningOfTableMarker="Upcoming Matches:"	#Signature to look for that marks beginning of table
# 	fixturesData=getFixturesDictionary(5)	#Get 5 fixtures in chronological order
# 	table=MakeRedditTable(fixturesData,r)
# 	timeCounter=0
# 	while True:	#outer loop to recreate fixturesData; set to 4 hours
# 		while True:	#inner loop to update sidebar; set to 60 seconds
# 			newTable=MakeRedditTable(fixturesData,r)
# 			# except blocks stolen from reddit post
# 			try:
# 				settings=r.get_settings(subredditName)
# 				description=settings['description']
# 				descriptionBegin=description.find(BeginningOfTableMarker)
# 				descriptionEnd=description.find(EndOfTableMarker) + len(EndOfTableMarker)
# 				description=description[:descriptionBegin] + newTable + description[descriptionEnd:]
# 				settings=r.get_subreddit(subredditName).update_settings(description=description)
# 				timeCounter+=1;
# 				if (timeCounter%240)==0:
# 					break
# 				time.sleep(60)
# 			except APIException as e:
# 				time.sleep(30)
# 			except ExceptionList as el:
# 				time.sleep(30)
# 			except (HTTPError, RateLimitExceeded) as e:
# 				time.sleep(30)
# 			except timeout:
# 				time.sleep(30)
# 			except Exception as e:
# 				sendEmail()
# 				raise
# 		fixturesData={}
# 		fixturesData=getFixturesDictionary(5)

