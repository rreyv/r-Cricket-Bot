import urllib2
from bs4 import BeautifulSoup


def getMatchInfoWrapper(cricinfoLiveLink):
    # get the scorecard link from the cricinfo live link
    scorecardLink = getScorecardLink(cricinfoLiveLink)
    if scorecardLink == "Match Over":
        return False, "Couldn't create match thread. Possible reasons are:\n\n* The match is over.\n* The match is not close to starting (i.e., live thread page is missing lots of data).\n* You did not send me the right link. The link must be the live thread link that you get from the fixtures page in Cricinfo."
    else:
        matchInfo = {}
        # get the soup from the scorecard link
        soup = returnSoup(scorecardLink)
        # does the match span multiple days?
        multipleDays = getMatchLength(soup)
        # get the thread title
        threadTitle = getThreadTitle(soup, multipleDays)
        teamLineup = getTeamLineup(soup)  # get the team lineup
        otherInfo = getOtherMatchRelatedInformation(soup)
        matchInfo['title'] = threadTitle
        matchInfo['teamInfo'] = teamLineup
        matchInfo['otherInfo'] = otherInfo
        return True,matchInfo
        # print threadTitle


def getScorecardLink(cricinfoLiveLink):
    soup = returnSoup(cricinfoLiveLink)
    liveIFrame = soup.find(id="live_iframe")
    # Match is over, live scorecard doesn't exist, return Match Over
    if not liveIFrame:
        return "Match Over"
        #return cricinfoLiveLink  # for debugging purposes
    return (cricinfoLiveLink + '?view=scorecard')


def getThreadTitle(soup, multipleDays):
    pageTitle = soup.title.string
    pageTitle = pageTitle.split("|", 1)
    pageTitle = pageTitle[0].strip()
    # if multipleDays == True:
    #	day = getMatchDay(soup)
    #	return "Match thread: " + pageTitle[:-6] + ", " + day
    return "Match thread: " + pageTitle[:-6] + getMatchDay(soup, multipleDays)


def getMatchLength(soup):
    rightHeader = soup.find(class_="headRightDiv")
    rightHeader = rightHeader.find_all('li')
    lastLine = rightHeader[-1]
    lastLine = lastLine.string.strip()
    if lastLine.find('-day match') != -1:
        return True
    else:
        return False


def returnSoup(hyperLink):
    usock = urllib2.urlopen(hyperLink)
    source = usock.read()
    usock.close()
    return BeautifulSoup(source, from_encoding="utf-8")


def getMatchDay(soup, multipleDays):
    if multipleDays is True:
        matchState = soup.find(class_="breakText")
        if not matchState:
            return ""
        else:
            matchState = matchState.get_text()
        if matchState.find('Day 1') != -1:
            return ", Day 1"
        elif matchState.find('Day 2') != -1:
            return ", Day 2"
        elif matchState.find('Day 3') != -1:
            return ", Day 3"
        elif matchState.find('Day 4') != -1:
            return ", Day 4"
        elif matchState.find('Day 5') != -1:
            return ", Day 5"
        return ""
    else:
        return ""


def getTeamLineup(soup):
    teamsList = {}
    numberOfInningsBat0 = len(soup.find_all(id="inningsBat0"))
    if numberOfInningsBat0>1:
        teamsList = getAnnouncedTeams(soup)
        return teamsList

    inningsBat1 = soup.find(id="inningsBat1")

    if not inningsBat1:
        teamsList = getSquad(soup)  # match hasn't begun, return squad
        return teamsList
    else:
        # match has begun, get playing eleven for team 1
        teamsList1 = getPlayingEleven(soup, "inningsBat1")
        # match has begun, get playing eleven for team 2
        inningsBat2=soup.find(id="inningsBat2")

        if inningsBat2:
            teamsList2 = getPlayingEleven(soup, "inningsBat2")
        else:
            teamsList2 = getPlayingEleven(soup, "inningsBat0")
        teamsList['team1name'] = teamsList1['teamname']
        teamsList['team2name'] = teamsList2['teamname']
        teamsList['team1players'] = teamsList1['teamplayers']
        teamsList['team2players'] = teamsList2['teamplayers']
        return teamsList


def getAnnouncedTeams(soup):
    i = 1
    teamsList = {}
    for team in soup.find_all(class_="inningsBat0"):
        if not team:
            #Should never happen as we're checking if battingClass exists right before this function call
            print "Can't find team information."
            return ""
        teamName = team.find(class_="inningsHead").find(
            "td").find_next_sibling().get_text()
        teamName = extractTeamName(teamName)
        teamsList['team' + str(i) + 'name'] = teamName
        teamsList['team' + str(i) + 'players'] = []
        teamsList['team' + str(i) + 'players'].extend(getPlayingBatsmen(team))
        teamsList['team' + str(i) + 'players'].extend(getDidNotBatBatsmen(team))
        i=i+1
    return teamsList


def getSquad(soup):
    i = 1
    teamsList = {}
    for team in soup.find_all(class_="inningsTable"):
        teamName = team.find(class_="inningsHead").get_text()
        teamsList['team' + str(i) + 'name'] = teamName
        teamsList['team' + str(i) + 'players'] = []
        for teamMember in team.find_all("span"):
            teamMemberLink = teamMember.find('a').get('href')
            teamMemberName = teamMember.get_text().strip()
            teamsList['team' + str(i) + 'players'].append(
                "[" + teamMemberName + "](http://www.espncricinfo.com" + teamMemberLink + ")")
        i += 1
    return teamsList


def getPlayingEleven(soup, battingClass):
    '''PLEASE REMEMBER TO CHANGE THIS TO FIRST INNINGS
    '''
    teamsList = {}
    team = soup.find(id=battingClass)
    if not team:
        #Should never happen as we're checking if battingClass exists right before this function call
        print "Can't find team information."
        return ""
    teamName = team.find(class_="inningsHead").find(
        "td").find_next_sibling().get_text()
    teamName = extractTeamName(teamName)
    teamsList['teamname'] = teamName
    teamsList['teamplayers'] = []
    teamsList['teamplayers'].extend(getPlayingBatsmen(team))
    teamsList['teamplayers'].extend(getDidNotBatBatsmen(team))
    return teamsList

'''Function can be improved'''


def extractTeamName(teamName):
    '''PLEASE REMEMBER TO CHANGE THIS TO FIRST INNINGS
    '''
    index = teamName.find("1st innings")
    if (index == -1):
        index = teamName.find("innings")
    if (index == -1):
        index = teamName.find("team")
    teamName = teamName[0:index - 1]
    return teamName.strip()


def getPlayingBatsmen(team):
    playerList = []
    for player in team.find_all("td", class_="playerName"):
        playerName = player.get_text().strip()
        playerLink = player.find('a').get('href')
        playerList.append(
            "[" + playerName + "](http://www.espncricinfo.com" + playerLink + ")")
    return playerList


def getDidNotBatBatsmen(team):
    playerList = []
    didNotBat = team.find_next_sibling(class_="inningsTable")
    if not didNotBat:
        return
    for player in didNotBat.find_all(class_="playerName"):
        playerName = player.get_text().strip()
        playerLink = player.get('href')
        playerList.append(
            "[" + playerName + "](http://www.espncricinfo.com" + playerLink + ")")
    return playerList


def getOtherMatchRelatedInformation(soup):
    returnText = ""
    subNav = soup.find(id="ciSubnav")
    for li in subNav.find_all('a'):
        if ((li.get('class')!=['PopupLinks']) and (li.get('class')!=['popNavLink'])):
            liText = li.get_text()
            liLink = li.get('href')
            liLink = "http://www.espncricinfo.com" + liLink
            returnText = returnText + " [" + liText + "](" + liLink + ") |"
    return returnText[:-2]
