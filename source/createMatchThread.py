import praw
from getMatchInfo import createMatchThread
from getFixturesInfo import getFixturesDictionary
from datetime import datetime
import time
from emailGlobals import sendEmail


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


def getGeneralRedditStuff():
    text = getStreamInformation()
    text = text + getFooter()
    return text

def getFooter():
    return "\n\nThis thread has been created by a bot that is still being tested. Bug reports can be sent to /u/rreyv or posted to /r/rreyv."
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

def createMatchThreadWrapper(r,threadTitle,liveThreadURL):
    # ashes game
    #liveThreadURL="http://www.espncricinfo.com/the-ashes-2013/engine/current/match/566936.html"
    #liveThreadURL="http://www.espncricinfo.com/ci/engine/current/match/650125.html"
    #liveThreadURL="http://www.espncricinfo.com/zimbabwe-v-pakistan-2013/engine/current/match/659555.html"
    # women's game
    #liveThreadURL = "http://www.espncricinfo.com/ci/engine/current/match/593725.html"
    #liveThreadURL="http://www.espncricinfo.com/ci/engine/current/match/630770.html" #india A vs South Africa A#
    #liveThreadURL="http://www.espncricinfo.com/zimbabwe-v-pakistan-2013/engine/current/match/659553.html"
    #liveThreadURL="http://www.espncricinfo.com/ci/engine/match/663207.html"    # Zimbabwe Pakistan
    matchInfo = createMatchThread(liveThreadURL)
    if not threadTitle:
        threadTitle = matchInfo['title']
    threadText = "###" + threadTitle + "\n\n"
    threadText = threadText + "[Link to Cricinfo Live Commentary](" + liveThreadURL + ")" + "\n\n"
    threadText = threadText + getMainThreadInformation(matchInfo)
    # other match related information
    threadText = threadText + "\n\n" + "*Series links:* " + \
        "\n\n" + matchInfo['otherInfo'] + "\n\n" + "***" +"\n\n"
    threadText = threadText + getGeneralRedditStuff()
    submission = r.submit('rreyv', threadTitle, text=threadText)
    print submission.url
    sendMail("Started match thread","Started match thread")


# if __name__ == "__main__":
#     r = praw.Reddit('/r/cricket Match Thread creator bot by /u/rreyv')
#     r.login()
#     approvedUpdaters=['rreyv','rCricketBot']
#     #while True:
#     # for message in r.get_unread(limit=None):
#     #     msgSubject=str(message.subject)
#     #     msgAuthor=str(message.author)
#     #     msgBody=str(message.body)
#     #     print "Author: " + msgAuthor
#     #     print "Subject: " + msgSubject
#     #     print "Body: " + msgBody
#     #     #message.mark_as_read()
#     #     if ((message.was_comment==False) and (msgAuthor in approvedUpdaters) and (msgSubject.find('reddit.com')!=-1)):
#     #         submission=r.get_submission(msgSubject)
#     #         selfText=submission.selftext
#     #         selfText=selfText+"\n\n"
#     #         selfText=selfText+"\n**/u/"+msgAuthor+" says:**\n"
#     #         selfText=selfText+msgBody
#     #         #submission.selftext(selfText)
#     #         print selfText
#     #         #setattr(submission,'selftext',selfText)
#     #         submission.edit(selfText)
#     createMatchThreadWrapper(r,"booga Booga","")



'''Debugging purposes'''
if __name__ == "__main__":
    liveThreadURL="http://www.espncricinfo.com/zimbabwe-v-pakistan-2013/engine/match/659555.html"
    #liveThreadURL="http://www.espncricinfo.com/ci/engine/current/match/650125.html"
    threadTitle = "Match thread: 1st Test: Zimbabwe v Pakistan at Harare, Day 2"
    r = praw.Reddit('/r/cricket Match Thread creator bot by /u/rreyv')
    r.login()
    createMatchThreadWrapper(r,threadTitle,liveThreadURL)
    