import praw
import time
import HTMLParser
from emailGlobals import sendEmail


def OrangeRed(r):
	Moderators=['rreyv','neoronin','brownboy13','rahulthewall','poop_monster','Envia','parlor_tricks','kabuliwallah','sunnydelish']
	subreddit="india"
	already_done=[]
	try:
		for message in r.get_unread(limit=None):
			msgSubject=str(message.subject)
			msgAuthor=str(message.author)
			message.mark_as_read()
			if ((message.was_comment==False) and (message.id not in already_done)):
				if msgSubject.lower()=="add users":
					if msgAuthor in Moderators:
						replyText=AddUser(r,message)
					else:
						replyText="Only moderators can use this command."
				elif msgSubject.lower()=="remove users":
					if msgAuthor in Moderators:
						replyText=RemoveUser(r,message)
					else:
						replyText="Only moderators can use this command."
				elif msgSubject.lower()=="list users":
					if msgAuthor in Moderators:
						replyText=ListUsers(r)
					else:
						replyText="Only moderators can use this command."
				elif msgSubject.lower().startswith("[mega thread]"):
					if msgAuthor in Moderators:
						replyText=CreateThread(r,message,subreddit)
				elif ((msgSubject.find('reddit.com')!=-1) or (msgSubject.find('redd.it')!=-1)):
					replyText=UpdateThread(r,message)
				else:
					replyText="I don't know what you're trying to say."
				message.reply(replyText)
				already_done.append(message.id)
	except:
		sendEmail("Couldn't read inbox","Couldn't read inbox")


def CreateThread(r,message,subreddit):
	msgSubject=str(message.subject)
	msgAuthor=str(message.author)
	msgBody=str(message.body)
	threadTitle=msgSubject
	threadText=msgBody
	html_parser = HTMLParser.HTMLParser()
	msgBody = html_parser.unescape(msgBody)
	try:
		submission = r.submit(subreddit, threadTitle, text=threadText)
		msgBody=msgBody+"\n\n---\nUser Updates: [ ^click ^here ^to ^post ^an ^update](http://www.reddit.com/message/compose?to=MegaThreadBot&subject="+str(submission.url)+")"
		msgBody = html_parser.unescape(msgBody)
		submission.edit(msgBody)
		returnText = "Thread created successfully. [Click here to go there.](" + str(submission.url) + ")"
	except:
		returnText = "Submission failed for some unknown reason. Maybe reddit was down? Please try again and if it fails, message /u/rreyv with the live thread link that you submitted."
	return returnText


def AddUser(r,message):
	returnText=""
	ApprovedUpdaters=[]
	text_file = open("MTBApprovedUpdaters.txt")
	'''Create list of users'''
	for line in text_file:
		ApprovedUpdaters.append(line.strip().lower())
	text_file.close()
	for user in str(message.body).split(','):
		user=user.split('/')[-1].strip().lower()
		'''Check if the user exists in the list already'''
		if ApprovedUpdaters.count(user)>0:
			returnText+="User " + user + " is already an approved updater for mega threads.\n\n"
		else:
			try:
				Redditor=r.get_redditor(user)
				UserExists=True
			except:
				UserExists=False

			if UserExists:
				ApprovedUpdaters.append(user)
				#sendMessage(user,"You ")
				returnText+="User /u/" + user + " has been added as an approved updater for mega threads.\n\n"
			else:
				returnText+="Cannot find user /u/" + user +". Have you spelt it correctly? If you think this message is incorrect and the bot is misbehaving, please let /u/rreyv know.\n\n" 
	text_file=open('MTBApprovedUpdaters.txt', 'w')
	for user in ApprovedUpdaters:
		if user!="":
			print>>text_file, user
	text_file.close()
	return returnText


def RemoveUser(r,message):
	returnText=""
	ApprovedUpdaters=[]
	text_file = open("MTBApprovedUpdaters.txt")
	'''Create list of users'''
	for line in text_file:
		if line!="":
			ApprovedUpdaters.append(line.strip().lower())
	text_file.close()
	for user in str(message.body).split(','):
		user=user.split('/')[-1].strip().lower()
		'''Check if the user exists in the list'''
		if ApprovedUpdaters.count(user)>0:
			ApprovedUpdaters.remove(user)
			returnText+="User /u/" + user + " has been removed as an approved updater for mega threads.\n\n"
		else:
			returnText+="User /u/" + user + " was not an approved updater for mega threads to begin with.\n\n"

	text_file=open('MTBApprovedUpdaters.txt', 'w')
	for user in ApprovedUpdaters:
		if user!="":
			print>>text_file, user
	text_file.close()
	return returnText


def ListUsers(r):
	returnText="List of approved users: \n\n"
	ApprovedUpdaters=[]
	text_file = open("MTBApprovedUpdaters.txt")
	'''Create list of users'''
	for line in text_file:
		if line!="":
			returnText+="/u/"+line.strip()+"\n\n"
	text_file.close()
	return returnText


def UpdateThread(r,message):
	returnText=""
	ApprovedUpdaters=[]
	text_file = open("MTBApprovedUpdaters.txt")
	for line in text_file:
		ApprovedUpdaters.append(line.strip().lower())
	text_file.close()	
	msgAuthor=str(message.author)
	msgAuthor=msgAuthor.lower()
	msgSubject=str(message.subject)
	msgBody=str(message.body)
	if (msgAuthor in ApprovedUpdaters):
		try:
			submission=r.get_submission(msgSubject)
		except:
			returnText="Doesn't look like this is a reddit thread. Update failed."
			return returnText
		if str(submission.author)!="MegaThreadBot":
			returnText="Doesn't look like this thread was created by me. I can't update this."
			return returnText
		selfText=submission.selftext
		selfText=selfText+"\n\n"
		selfText=selfText+"\n\n*/u/"+msgAuthor+":*\n\n"
		selfText=selfText+msgBody
		selfText=selfText+"\n***"
		html_parser = HTMLParser.HTMLParser()
		selfText = html_parser.unescape(selfText)
		submission.edit(selfText)
		returnText="Thread has been updated. [Here's the link to the post.](" + str(submission.url) + ")"
		return returnText
	else:
		returnText="Sorry, only moderator approved users can update these threads. Please contact the moderators of /r/india to get approved."
	return returnText
