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

# if __name__=="__main__":
# 	msg = MIMEText("Waddup. This is the body")
# 	msg['Subject'] = 'The contents of this title'
# 	msg['From'] = 'rcricketbot@gmail.com'
# 	msg['To'] = 'ravishr224@gmail.com'

# 	s = smtplib.SMTP('smtp.gmail.com', 587)
# 	s.ehlo()
# 	s.starttls()
# 	s.ehlo()
# 	username=raw_input('Enter username: ')
# 	pw=raw_input('Enter the password: ')
# 	s.login(username+'@gmail.com',pw)
# 	s.sendmail(msg['From'], msg['To'], msg.as_string())
# 	s.quit()

# def updateSidebar(fixturesData,r,subredditName):
# 	newTable=MakeRedditTable(fixturesData,r)
# 	# except blocks stolen from reddit post
# 	EndOfTableMarker="[More Fixtures](http://www.espncricinfo.com/ci/content/match/fixtures/index.html?days=30)" #Signature to look for that marks the end of table
# 	BeginningOfTableMarker="Upcoming Matches:"	#Signature to look for that marks beginning of table
# 	try:
# 		settings=r.get_settings(subredditName)
# 		description=settings['description']
# 		descriptionBegin=description.find(BeginningOfTableMarker)
# 		descriptionEnd=description.find(EndOfTableMarker) + len(EndOfTableMarker)
# 		description=description[:descriptionBegin] + newTable + description[descriptionEnd:]
# 		settings=r.get_subreddit(subredditName).update_settings(description=description)
# 		timeCounter+=1;
# 		if (timeCounter%240)==0:
# 			break
# 		time.sleep(60)
# 	except APIException as e:
# 		time.sleep(30)
# 	except ExceptionList as el:
# 		time.sleep(30)
# 	except (HTTPError, RateLimitExceeded) as e:
# 		time.sleep(30)
# 	except timeout:
# 		time.sleep(30)
# 	except Exception as e:
# 		sendEmail(fromUser,fromPass,toUser,"Subject","Text")
# 		raise

def readInbox(r):
	pass

if __name__=="__main__":
	#One time setup
	r = praw.Reddit('/r/cricket sidebar updater bot by /u/rreyv') #reddit stuff
	subredditName='rreyv'
	r.login() #sign in!
	fixturesData={}
	fixturesData=getFixturesDictionary(5)

	i=0
	#one time setup ends
	while True:
		#things that happen every four hours
		while True:
			#things that happen every 60 seconds
			updateSidebar(fixturesData,r,subredditName)
			readInbox(r)
			time.sleep(60)
			i+=1;
			if i%240==0:
				break
			#End of 60 second loop
		fixturesData={}
		fixturesData=getFixturesDictionary(5)
		sendEmail("Grabbing fixtures from Cricinfo","Grabbed fixtures from Cricinfo")
		i=0
		#end of four hour loop#

	# con = None
	# try:
	# 	con=sql.connect('rCricket.db')
	# 	cur=con.cursor()
	# 	matchThreadText="Match Thread: something yada yada"
	# 	matchThreadLink="http://www.google.com"
	# 	cur.execute('insert into MatchThreads(\'MatchThreadTitle\',\'MatchThreadHyperLink\') values (\''+matchThreadText+'\',\''+matchThreadLink+'\')')
	# 	#data=cur.fetchone()
	# 	cur.execute('select * from MatchThreads')
	# 	data=cur.fetchone()
	# 	print data
	# except sql.Error, e:
	# 	print "Error %s:" % e.args[0]
