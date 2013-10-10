import praw
from datetime import datetime
from requests.exceptions import HTTPError
from praw.errors import ExceptionList, APIException, InvalidCaptcha, InvalidUser, RateLimitExceeded
from socket import timeout
import sqlite3 as sql
from emailGlobals import sendEmail
from inboxHandler import readInbox


def updateLiveScores:
	pass