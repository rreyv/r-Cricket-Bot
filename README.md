rCricketBot
===========

Does things for /r/cricket

!Important!

***Ireland support has been removed as of Sept. 10. ESPNCricinfo is not classifying Ireland's four day games under 'International' so saying that the bot supports Ireland would be incorrect. If you wish to start a match thread for Ireland games, please message the bot to do so (steps are below) or create one manually.*** 

TL;DR
-----

* The bot will create a match thread automatically for all test playing nations

* To create a match thread for any other game (domestic, Under 19s, Under 23s, Women's etc.), message the bot with the subject 'create thread' and just the ESPNCricinfo live live scorecard URL as the body. [Example] [1]. Please wait until the match is very close to the start (between 30 minutes and 1 hour) or has already begun (a ball has been bowled) to request a thread. **The bot might fail in some cases where the toss has occured but a ball hasn't been bowled.**



Features
--------

* Creates a table in the sidebar that lists out the next 5 international fixtures along with the time remaining.

* Creates a match thread around 1 hour (56 minutes to 1 hour) before the start of an international fixture.

* Users can submit updates by messaging the bot. Updates then show up at the bottom of the selfpost. This requires that the user be approved by a moderator. Talk to the moderators of /r/cricket to get approved.

* **Users can create match threads for domestic/Under-19s/Under-23s/Women's/A fixtures by IM'ing the bot with a subject of 'create thread' and just the ESPNCricinfo live live scorecard URL as the body.** [Example] [1]. Please bear in mind that the bot can sometimes fail in creating match threads for non-international games. This is because the bot does not have access to an API and it has to scrape through the page's HTML to find relevant information. So for cases where a match's coverage is limited, the bot cannot find what it needs and fails. It's best to wait until the match is between 30 minutes and 60 minutes from the start OR has already begun to create a match thread for it. **In most cases, if a ball has been bowled the match thread will be created without issues.**


Running the bot on your own PC
------------------------------

* Download the source code

* Install the following python modules: [PRAW] [2], [Beautiful Soup 4] [3]

* Create a sqlite3 database named 'rCricket.db' in the project folder

* Create the MatchThreads table:

        CREATE TABLE "MatchThreads" (
    
        "fixtureId" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    
        "threadTitle" TEXT NOT NULL,
    
        "liveThreadLink" TEXT NOT NULL,
    
        "source" TEXT,
    
        "matchThreadLink" TEXT NOT NULL,
    
        "creationTime" TEXT NOT NULL
    
        )

* Edit startBot.py and ensure you have the right subreddit name

* Run the bot: python startBot.py


Credits
--------

* [u/honeydew5] [4] for help with Python
 

 [1]: http://i.imgur.com/pH5guDI.png "Example"
 [2]: https://praw.readthedocs.org/en/latest/ "PRAW"
 [3]: http://www.crummy.com/software/BeautifulSoup/ "Beautiful Soup 4"
 [4]: http://www.reddit.com/user/honeydew5/ "u/honeydew5"
 
