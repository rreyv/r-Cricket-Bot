import praw
from getMatchInfo import getMatchInfoWrapper
from getFixturesInfo import getFixturesDictionary
from datetime import datetime
import time
from emailGlobals import sendEmail
import sqlite3 as sql
import HTMLParser


def getMainThreadInformation(matchInfo):
    teamOneName = matchInfo['teamInfo']['team1name']
    teamTwoName = matchInfo['teamInfo']['team2name']
    teamOnePlayerList = matchInfo['teamInfo']['team1players']
    teamTwoPlayerList = matchInfo['teamInfo']['team2players']
    text = "***" + "\n\n"
    text = text + "**" + teamOneName.strip() + "**\n\n"
    for player in teamOnePlayerList:
        text = text + player + ", "
    text = text[:-2]
    text = text + "\n\n"
    text = text + "***" + "\n\n"
    text = text + "**" + teamTwoName.strip() + "**\n\n"
    for player in teamTwoPlayerList:
        text = text + player + ", "
    text = text[:-2]
    text = text + "\n\n" + "***" + "\n\n"
    return text


def getGeneralRedditStuff(source):
    text = getStreamInformation()
    text = text + getFooter(source)
    return text


def getFooter(source):
    if source=='rCricketBot':
        return "\n\nThis thread was created automatically. Learn more about the bot [here](https://github.com/rreyv/r-Cricket-Bot#rcricketbot).\n***"
    else:
        return "\n\nThis thread was requested by /u/"+source+". Learn more about the bot [here](https://github.com/rreyv/r-Cricket-Bot#rcricketbot).\n***"
    pass

def getStreamInformation():
    Lshunter = "[Lshunter](http://www.lshunter.tv/other-live-streaming-video.html)"
    Wiziwig = "[Wiziwig](http://www.wiziwig.tv/competition.php?part=sports&discipline=cricket)"
    MoreStreams = "[More streams](http://www.reddit.com/r/Cricket/comments/foezt/live_streams/)"
    Crictime = "[Crictime](http://www.crictime.com)"
    text = "\n\n *Live streams:* " + Lshunter + " | " + \
        Wiziwig + " | " + Crictime + " | " + MoreStreams
    text = text + "\n\n ***"
    return text


def createMatchThreadWrapper(r,threadTitle,liveThreadURL,source,subreddit):
    RealLink,matchInfo = getMatchInfoWrapper(liveThreadURL)
    if not RealLink:
        return [False,matchInfo]
    # At this point, we have a cricinfo live thread link

    if not threadTitle:
        threadTitle = matchInfo['title']

    #If it's a test playing nation, tell them that the thread will be created automatically.

    if ( source!='rCricketBot' and (WeCareAbout(matchInfo['teamInfo']['team1name']) or WeCareAbout(matchInfo['teamInfo']['team2name']))):
        return [False,"Match thread creation request denied. \n\nAt least one of the teams has test status. A match thread will be created automatically approximately one hour before the game. If a thread hasn't been created please message /u/rreyv"]

    #If it's not a test playing nation, see if a thread already exists
    [alreadyExists, replyLink]=HasThreadBeenCreated(liveThreadURL)
    if alreadyExists:
        return [False,"Match thread has been created already for this match less than 12 hours ago. Here's the [link.]("+replyLink+")"]

    #At this line, the request to create the thread is either automated, or it's a match containing shitty teams
    threadText = "###" + threadTitle + "\n\n"
    threadText = threadText + "[Link to Cricinfo Live Commentary](" + liveThreadURL + ")" + " | Sort this thread by new posts | Reddit-Stream link for this thread" + "\n\n"
    threadText = threadText + getMainThreadInformation(matchInfo)
    # other match related information
    threadText = threadText + "\n\n" + "*Series links:* " + \
        "\n\n" + matchInfo['otherInfo'] + "\n\n" + "***" +"\n\n"
    threadText = threadText + getGeneralRedditStuff(source)
    html_parser = HTMLParser.HTMLParser()
    threadText = html_parser.unescape(threadText)
    try:
        submission = r.submit(subreddit, threadTitle, text=threadText)
    except:
        return [False, "Submission failed for some unknown reason. Maybe reddit was down? Please try again and if it fails, message /u/rreyv with the live thread link that you submitted."]
    #Update the SQL table with submission information
    InsertMatchThreadInfoIntoSQL(threadTitle,liveThreadURL,source,str(submission.url))

    #By this line, the thread has been created
    TryLoop=None
    while not TryLoop:
        try:
            TryLoop=EditSubmission(r,submission)
        except:
            time.sleep(30)

    #By this line, the submission has been edited and we can tell the requestor about it.
    sendEmail("Started match thread","Created a new match thread "+str(submission.url))
    return [True,"Match thread successfully created. [Here's the link](" + str(submission.url) +")."]
    


def WeCareAbout(teamName):
    teamName=teamName.strip()
    squadPos=teamName.find('squad')
    if squadPos!=-1:
        teamName=teamName[:(squadPos-1)]
    teamName=teamName.strip()
    teamsWeCareAbout = ['Australia', 'England', 'New Zealand', 'Pakistan', 'India', 'South Africa', 'Zimbabwe', 'Bangladesh', 'West Indies', 'Sri Lanka']
    if ((teamName in teamsWeCareAbout) and (teamName.find("Women")==-1) and (teamName.find("Under-23")==-1) and (teamName.find("Under-19")==-1)):
        return True
    return False


def InsertMatchThreadInfoIntoSQL(threadTitle,liveThreadURL,source,submissionUrl):
    con = None
    con = sql.connect('rCricket.db',detect_types=sql.PARSE_DECLTYPES)
    cur = con.cursor()
    currentGMT=datetime.utcnow()
    cur.execute("insert into MatchThreads('threadTitle','liveThreadLink','source','matchThreadLink','creationTime') values (?,?,?,?,?)",(threadTitle,liveThreadURL,source,submissionUrl,currentGMT))
    con.commit()
    con.close()


def HasThreadBeenCreated(liveThreadURL):
    con = None
    con = sql.connect('rCricket.db',detect_types=sql.PARSE_COLNAMES)
    cur = con.cursor()
    currentGMT=datetime.utcnow()
    cur.execute("select max(creationTime) as '[timestamp]' from MatchThreads where liveThreadLink= ?",(liveThreadURL,))
    data=cur.fetchone()
    if not data[0]:
        con.close()
        return [False,None]
    timeDifference=currentGMT-data[0]
    if timeDifference.total_seconds()<=43200:
        cur.execute("select MatchThreadLink from MatchThreads where creationTime=?", (data[0],))
        data=cur.fetchone()
        con.close()
        return [True,data[0]]
    return [False,None]


def EditSubmission(r,submission):
    submissionUrl=str(submission.url)
    redditStreamLink=submissionUrl.replace("http://www.reddit.com","http://www.reddit-stream.com")
    selfText=submission.selftext
    selfText=selfText.replace("Sort this thread by new posts","[Sort this thread by new posts]("+str(submissionUrl)+"?sort=new)")
    selfText=selfText.replace("Reddit-Stream link for this thread","[Reddit-Stream link for this thread]("+redditStreamLink+")")
    selfText=selfText+"\nUser Updates: [ ^click ^here ^to ^post ^an ^update](http://www.reddit.com/message/compose?to=rCricketBot&subject="+str(submissionUrl)+")"
    html_parser = HTMLParser.HTMLParser()
    selfText = html_parser.unescape(selfText)
    submission.edit(selfText)
    return "Great Success!"