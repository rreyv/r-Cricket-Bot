import praw
from datetime import datetime
import time
import logging
from requests.exceptions import HTTPError
from praw.errors import ExceptionList, APIException, InvalidCaptcha, InvalidUser, RateLimitExceeded
import sqlite3 as sql
from emailGlobals import sendEmail
from getMatchInfo import returnSoup
import re

def updateLineups(r):
	#TwelveHourOldMatches
	#figure out matches you need to update the lineup for
		updateLineUpPerThread(matchThreadId)
		pass

def updateLineupPerThread(matchThreadId):
	submission = r.get_submission(matchThreadId)
	selfText = submission.selftext
	teamOneName,teamOnePlayers=extractTeamInfo(selfText,1)
	teamTwoName,teamTwoPlayers=extractTeamInfo(selfText,2)
	format="tests"
	teamOneTable=teamOneName+"|M|R|HS|Avg|100|Wkt|BBI|Bowl Av.|5|Ct|St|"+"(v. )"+teamTwoName+"|M|R|HS|Avg|100|Wkt|BBI|Bowl Av.|5|Ct|St|\n"
	teamOneTable=teamOneTable+"|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|\n"
	teamTwoTable=teamTwoName+"|M|R|HS|Avg|100|Wkt|BBI|Bowl Av.|5|Ct|St|"+"(v. )"+teamOneName+"|M|R|HS|Avg|100|Wkt|BBI|Bowl Av.|5|Ct|St|\n"
	teamTwoTable=teamTwoTable+"|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|\n"
	for player in teamOnePlayers:
		teamOneTable=teamOneTable+returnStatsPerPlayer(player,teamTwoName.lower(),format)+"\n"
		time.sleep(2)
	for player in teamTwoPlayers:
	 	teamTwoTable=teamTwoTable+returnStatsPerPlayer(player,teamOneName.lower(),format)+"\n"
	 	time.sleep(2)
	lineSplit=selfText.split("***")
	teamInfo=lineSplit[2]
	teamOneTable="\n\n"+teamOneTable+"\n"
	teamTwoTable="\n\n"+teamTwoTable+"\n"
	selfText=selfText.replace(selfText.split("***")[2],teamOneTable)
	selfText=selfText.replace(selfText.split("***")[3],teamTwoTable)
	print selfText

def returnStatsPerPlayer(player,oppositionTeamName,format):
	playerId=re.findall('\d+\.html', player)[0]
	returnString="|" + player + "|"
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
	
	base_url='http://stats.espncricinfo.com/stats/engine/player/'
	url = base_url+ str(playerId) + "?"+ 'class='+str(formats[format]) +';opposition='+str(country_codes[oppositionTeamName.lower()])+";template=results;type=allround"
	soup = returnSoup(url)

	for table in soup.find_all(class_="engineTable"):
		if table.caption:
			if table.caption.string=='Career averages':
				for tableRow in table.find_all(class_="data1"):
					for tableData in tableRow.find_all("td"):
						#if ((not (tableData.has_attr("class") or tableData.has_attr("style"))) or tableData.get('class')==["padAst"] or tableData.get('class')==["padDp2"]):
						if (not (tableData.get("class")==["left"] or tableData.has_attr("style"))):
							if tableData.string:
								returnString=returnString+tableData.string+"|"
							else:
								returnString=returnString+" |"
					returnString=returnString+" |"
	if returnString[-2:]==" |":
		returnString=returnString[:-2]
	return returnString

def extractTeamInfo(selftext,teamNumber):
	lineSplit=selftext.split("***")
	teamNumber=teamNumber+1
	teamInfo=lineSplit[teamNumber]
	teamName=teamInfo.split("**")[1]
	teamPlayers=teamInfo.split("**")[2].strip().split(", ")
	return teamName,teamPlayers
	#teamOneName=getTeamName(selftext)

if __name__=="__main__":
	#returnStatsPerPlayer(35320,'Bangladesh','odis')
	r = praw.Reddit('/r/cricket testing things by /u/rreyv. Version 1.0') #reddit stuff
	r.login()
	matchThreadLink='http://www.reddit.com/r/rreyv/comments/1o9xe8/match_thread_bangladesh_v_new_zealand_at/'
	#extractTeamInfo(selfText,1)
	updateLineupPerThread(matchThreadLink)