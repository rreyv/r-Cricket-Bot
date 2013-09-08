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

def readInbox(r,subreddit):
	Moderators=['sunnydelish','TheAshes','jack47','EyesAllOnFire','ingreenheaven','rreyv']
	#approvedUpdaters=['rreyv','sunnydelish']
	try:
		for message in r.get_unread(limit=None):
			msgSubject=str(message.subject)
			msgAuthor=str(message.author)
			message.mark_as_read()
			if message.was_comment==False:
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
				elif msgSubject.lower()=="create thread":
					replyText=CreateThread(r,message,subreddit)
				elif ((msgSubject.find('reddit.com')!=-1) or (msgSubject.find('redd.it')!=-1)):
					replyText=UpdateThread(r,message)
				else:
					replyText="I'm not sure what you're trying to say. Check out the bot help page [here](https://github.com/rreyv/r-Cricket-Bot#rcricketbot)."
				message.reply(replyText)
	except:
		print "Error"
		#print str(e)
		#sendEmail("We've got a problem","Couldn't read inbox")


def CreateThread(r,message,subreddit):
	msgSubject=str(message.subject)
	msgAuthor=str(message.author)
	msgBody=str(message.body)
	Result,returnText=createMatchThreadWrapper(r,None,msgBody,msgAuthor,subreddit)
	return returnText


def AddUser(r,message):
	returnText=""
	ApprovedUpdaters=[]
	text_file = open("ApprovedUpdaters.txt")
	'''Create list of users'''
	for line in text_file:
		# if line!="":
		ApprovedUpdaters.append(line.strip())
	text_file.close()
	for user in str(message.body).split(','):
	#for user in message.split(','):
		user=user.split('/')[-1].strip()
		'''Check if the user exists in the list already'''
		if ApprovedUpdaters.count(user)>0:
			returnText+="User " + user + " is already an approved updater for match threads.\n\n"
		else:
			try:
				Redditor=r.get_redditor(user)
				UserExists=True
			except:
				UserExists=False

			if UserExists:
				ApprovedUpdaters.append(user)
				#sendMessage(user,"You ")
				returnText+="User /u/" + user + " has been added as an approved updater for match threads.\n\n"
			else:
				returnText+="Cannot find user /u/" + user +". Have you spelt it correctly? If you think this message is incorrect and the bot is misbehaving, please let /u/rreyv know." 
	text_file=open('ApprovedUpdaters.txt', 'w')
	for user in ApprovedUpdaters:
		if user!="":
			print>>text_file, user
	text_file.close()
	return returnText



def RemoveUser(r,message):
	returnText=""
	ApprovedUpdaters=[]
	text_file = open("ApprovedUpdaters.txt")
	'''Create list of users'''
	for line in text_file:
		if line!="":
			ApprovedUpdaters.append(line.strip())
	text_file.close()
	for user in str(message.body).split(','):
	#for user in message.split(','):
		user=user.split('/')[-1].strip()
		'''Check if the user exists in the list'''
		if ApprovedUpdaters.count(user)>0:
			ApprovedUpdaters.remove(user)
			#potentionally message them
			returnText+="User /u/" + user + " has been removed as an approved updater for match threads.\n\n"
		else:
			returnText+="User /u/" + user + " was not an approved updater for match threads to begin with.\n\n"

	text_file=open('ApprovedUpdaters.txt', 'w')
	for user in ApprovedUpdaters:
		if user!="":
			print>>text_file, user
	text_file.close()
	return returnText


def ListUsers(r):
	returnText="List of approved users: \n\n"
	ApprovedUpdaters=[]
	text_file = open("ApprovedUpdaters.txt")
	'''Create list of users'''
	for line in text_file:
		if line!="":
			returnText+="/u/"+line.strip()+"\n\n"
	text_file.close()
	return returnText

def UpdateThread(r,message):
	returnText=""
	ApprovedUpdaters=[]
	text_file = open("ApprovedUpdaters.txt")
	for line in text_file:
		ApprovedUpdaters.append(line.strip())
	text_file.close()	
	msgAuthor=str(message.author)
	msgSubject=str(message.subject)
	msgBody=str(message.body)
	if (msgAuthor in ApprovedUpdaters):

		try:
			submission=r.get_submission(msgSubject)
		except:
			returnText="Doesn't look like this is a reddit thread. I can only update match threads created by me."
			return returnText
		if str(submission.author)!="rCricketBot":
			returnText="Doesn't look like this match thread was created by me. I can't update this."
			return returnText
		selfText=submission.selftext
		selfText=selfText+"\n\n"
		selfText=selfText+"\n\n*/u/"+msgAuthor+":*\n\n"
		selfText=selfText+msgBody
		selfText=selfText+"\n***"
		submission.edit(selfText)
		returnText="Match thread has been updated."
		return returnText
	else:
		returnText="Sorry, only moderator approved users can update match threads. Please contact the moderators of /r/cricket to get approved."
	return returnText