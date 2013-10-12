import praw
import datetime
import time
from requests.exceptions import HTTPError
from praw.errors import ExceptionList, APIException, InvalidCaptcha, InvalidUser, RateLimitExceeded
import sqlite3 as sql
from bs4 import BeautifulSoup
from emailGlobals import sendEmail
from inboxHandler import readInbox
from getMatchInfo import returnSoup
import HTMLParser


def updateLiveScores(r):
	ArrayOfCurrentlyRunningFixtures = getArrayOfCurrentlyRunningFixtures()
	if not ArrayOfCurrentlyRunningFixtures:
		return
	for runningFixture in ArrayOfCurrentlyRunningFixtures:
		matchThreadLink = runningFixture[0]
		liveThreadLink = runningFixture[1]
		matchScoreUpdater(r,liveThreadLink,matchThreadLink)


def getArrayOfCurrentlyRunningFixtures():
	con = None
	con = sql.connect('rCricket.db',detect_types=sql.PARSE_COLNAMES)
	cur = con.cursor()
	currentGMT=datetime.datetime.utcnow()
	TwelveHoursAgo=currentGMT - datetime.timedelta(0,0,0,0,0,12)
	cur.execute("select matchThreadLink,liveThreadLink from MatchThreads where creationTime between ? and ?",(TwelveHoursAgo,currentGMT))
	data=cur.fetchall()
	return data

def matchScoreUpdater(r,liveThreadLink,matchThreadLink):
	#liveThreadLink='http://www.espncricinfo.com/bangladesh-v-new-zealand-2013-14/engine/match/668949.html'
	iFrameLink=getiFrameLink(liveThreadLink)
	liveScoreText=getLiveScoreText(iFrameLink)
	updateMatchThread(r,matchThreadLink,liveScoreText)

def getiFrameLink(liveThreadLink):
	return liveThreadLink+'?template=iframe_desktop'

def updateMatchThread(r,matchThreadLink,liveScoreText):
	submission = r.get_submission(matchThreadLink)
	selfText = submission.selftext
	html_parser = HTMLParser.HTMLParser()
	start = selfText.find("***")
	end = selfText.find("***",(start+3)) + 3
	selfText = selfText[:start] + liveScoreText + selfText[end:]
	selfText = html_parser.unescape(selfText)
	submission.edit(selfText)

def getLiveScoreText(iFrameLink):
	returnText=["","",""]
	returnText[1]="***\n\n|Team|Score|\n|:---|:---|"
	soup = returnSoup(iFrameLink)
	for Table in soup.find_all(class_="desktopPanelContent"):
		returnText[1]=returnText[1]+HTMLTableToPythonTable(Table)[1]+"\n\n"
		returnText[2]=returnText[2]+HTMLTableToPythonTable(Table)[2]
	index=returnText[1].find("|Batsmen|R|B|4s|6s|")+len("|Batsmen|R|B|4s|6s|")
	finalReturnText=returnText[1][:index]+"\n|:---|:---|:---|:---|:---|"+returnText[1][index:]
	finalReturnText=finalReturnText + returnText[2]
	finalReturnText=finalReturnText+"***"
	print finalReturnText
	return finalReturnText

def HTMLTableToPythonTable(Table):
	returnText=["","",""]
	for TableRow in Table.find_all("tr"):
		if len(TableRow.find_all("td"))>1:
			returnText[1]=returnText[1]+"\n"
			returnText[1]=returnText[1]+"|"
			for TableData in TableRow.find_all("td"):
				returnText[1]=returnText[1]+TableData.string+"|"
	for TableRow in Table.find_all("tr"):
		if len(TableRow.find_all("td"))==1:
			TableData=TableRow.find("td")
			if TableData.string:
				returnText[2]=returnText[2]+TableData.string+"\n\n"
	return returnText

if __name__=="__main__":
	#matchScoreUpdater(1,2,3,4)
	#getArrayOfCurrentlyRunningFixtures()
	r = praw.Reddit('/r/rreyv live score updater test by /u/rreyv. Version 1.0') #reddit stuff
	subredditName='cricket'
	r.login() #sign in!
	while True:
		updateLiveScores(r)
		time.sleep(50)