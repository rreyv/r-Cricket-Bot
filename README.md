rCricketBot
===========

Does things for /r/cricket

TL;DR
-----

* The bot will create a match thread automatically for all test playing + Ireland games

* To create a match thread for any other game (domestic, Under 19s, Under 23s, Women's etc.), message the bot with the subject 'create thread' and just the ESPNCricinfo live live scorecard URL as the body. [Example] [1]. Please wait until the match is very close to the start (30 minutes or so) or has already begun to request a thread.



Features
--------

* Creates a table in the sidebar that lists out the next 5 international fixtures along with the time remaining.

* Creates a match thread around 1 hour (56 minutes to 1 hour) before the start of an international fixture.

* Users can submit updates by messaging the bot. Updates then show up at the bottom of the selfpost. This requires that the user be approved by a moderator. Talk to the moderators of /r/cricket to get approved.

* **Users can create match threads for domestic/Under-19s/Under-23s/Women's/A fixtures by IM'ing the bot with a subject of 'create thread' and just the ESPNCricinfo live live scorecard URL as the body.** [Example] [1]. Please bear in mind that the bot can sometimes fail in creating match threads for non-international games. This is because the bot does not have access to an API and it has to scrape through the page's HTML to find relevant information. So for cases where a match's coverage is limited, the bot cannot find what it needs and fails. It's always best to wait until a half hour before the start of a game to create a match thread for it.


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
 
