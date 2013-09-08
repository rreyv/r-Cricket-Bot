rCricketBot
===========

Does things for /r/cricket

Features
--------

* Creates a table in the sidebar that lists out the next 5 international fixtures along with the time remaining.

* Creates a match thread around 1 hour (56 minutes to 1 hour) before the start of an international fixture.

* Users can submit updates by messaging the bot. Updates then show up at the bottom of the selfpost. This requires that the user be approved by a moderator. Talk to the moderators of /r/cricket to get approved.

* Users can create match threads for domestic/Under-19s/Under-23s/Women's/A fixtures by IM'ing the bot with a subject of 'create thread' and just the ESPNCricinfo live live scorecard URL as the body. [Example] [1]. Please bear in mind that the bot can sometimes fail in creating match threads for non-international games. This is because the bot does not have access to an API and it has to scrape through the page's HTML to find relevant information. So for cases where a match's coverage is limited, the bot cannot find what it needs and fails. It's always best to wait until a half hour before the start of a game to create a match thread for it.
 
 [1]: http://i.imgur.com/pH5guDI.png "Example"