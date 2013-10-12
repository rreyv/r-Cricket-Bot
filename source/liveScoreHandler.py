import praw
from datetime import datetime
from requests.exceptions import HTTPError
from praw.errors import ExceptionList, APIException, InvalidCaptcha, InvalidUser, RateLimitExceeded
import sqlite3 as sql
from bs4 import BeautifulSoup
from emailGlobals import sendEmail
from inboxHandler import readInbox
from getMatchInfo import returnSoup


def updateLiveScores(r,subredditName):
	#get list of currently running matches
	#loop over currently running matches:
		#matchScoreUpdater(r,subredditName,matchId) #For each running match, run the update score function
	pass

def matchScoreUpdater(r,subredditName,matchId):
	#from matchId, get the live thread hyperlink
	liveThreadLink='http://www.espncricinfo.com/bangladesh-v-new-zealand-2013-14/engine/match/668949.html'
	iFrameLink=getiFrameLink(liveThreadLink)
	liveScoreText=getLiveScoreText(iFrameLink)
	updateMatchThread(r,subredditName,matchId,liveScoreText)

def getiFrameLink(liveThreadLink):
	return liveThreadLink+'?template=iframe_desktop'

def updateMatchThread(r,subredditName,matchId,liveScoreText):
	pass

def getLiveScoreText(iFrameLink):
	returnText="|Team|Score|\n|:---|:---|"
	soup = returnSoup(iFrameLink)
	for Table in soup.find_all(class_="desktopPanelContent"):
		returnText=returnText+HTMLTableToPythonTable(Table)+"\n\n"
	print returnText


def HTMLTableToPythonTable(Table):
	returnText=""
	#Table = soup.find(class_=tableClass)
	for TableRow in Table.find_all("tr"):
		if len(TableRow.find_all("td"))>1:
			returnText=returnText+"\n"
			returnText=returnText+"|"
			for TableData in TableRow.find_all("td"):
				returnText=returnText+TableData.string+"|"
	for TableRow in Table.find_all("tr"):
		if len(TableRow.find_all("td"))==1:
			TableData=TableRow.find("td")
			if TableData.string:
				returnText=returnText+"\n\n"+TableData.string
	return returnText


if __name__=="__main__":
	matchScoreUpdater(1,2,3)