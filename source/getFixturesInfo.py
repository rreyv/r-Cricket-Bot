# Documentation
"""
The purpose of this script is to develop a Reddit Bot which would automatically
create a new match thread before the match starts
"""

################################################################################
# IMPORTS
################################################################################
import urllib2
from bs4 import BeautifulSoup 
from datetime import datetime
from getMatchInfo import returnSoup

################################################################################
# FUNCTIONS
################################################################################

def readInternationalFixtures( myurl, ciResults):
    """
    The purpose of this function is to extract data from espncricinfo about the 
    current and future matches and store that result in a dictionary. 
    """
    soup = returnSoup( myurl )

    matchDateId = None
    matchRowId = None

    rowType = {'id':'date',
               'class':'match'}

    # Obtain only the results which are rows in the table
    allRows = soup.find_all('tr')

    i=0
    for row in allRows:
        if 'id' in row.attrs:
            rowType = "date"
        elif 'class' in row.attrs:
            rowType = "match"
        else:
            rowType = ""

        if rowType == "date":
            if 'id' in row.attrs:
                (matchDateId, matchDate) = getText(row, 'id')
                matchRowId = None

        elif rowType == "match":
            if 'head_id' in row.attrs and 'class' in row.attrs and str(row['class'][0]) =="ciResults":
                if row['head_id'] == matchDateId:
                    columns = row.find_all('td')
                    i+=1
                    ciResults[i]={}
                    ciResults[i]['Day']=matchDate[4:]
                    formatColumn (columns,ciResults,i)
                    
            for link in row.find_all('a'):
                ciResults[i]['Link']='http://www.espncricinfo.com'+link.get('href')

    return ciResults

def getText (rowValue, attrName):
    matchId = rowValue[attrName]
    stuff = ((rowValue.get_text()).strip()).encode('ascii', 'ignore')
    return (matchId, stuff)

def formatColumn ( colData, ciResults,i ):
    text = [col.get_text() for col in colData]
    textval = [val.encode('ascii', 'ignore') for val in text]
    data = [(val.replace("\n", "")).strip() for val in textval]

    team1 = (data[1].split(" v "))[0].strip()
    team2 = ((data[1].split(" v "))[1].split(" at "))[0].strip()

    team1Abv=getTeamAbv(team1)
    team2Abv=getTeamAbv(team2)

    indexOfAt=data[1].find(" at")
    indexOfComma=data[1].find(", ")
    dataAfterComma=data[1][(indexOfComma+2):]

    if len(dataAfterComma)>20:
        dataAfterComma = abbreviateMatchText(dataAfterComma)

    matchTextWithoutLocation=team1Abv + " v " + team2Abv + ", " + dataAfterComma
    if data[0].strip()=="-":
        data[0]="00:00 GMT"
    ciResults[i]['ColumnTitle']=matchTextWithoutLocation
    ciResults[i]['Time']=getTime(data[0],ciResults[i]['Day'])
    ciResults[i]['MatchText']=data[1]
    ciResults[i]['TeamOne']=team1
    ciResults[i]['TeamTwo']=team2


def abbreviateMatchText(matchTextWithoutLocation):
    returnStr=""
    for i in matchTextWithoutLocation.upper().split():
        returnStr += i[0]
    return returnStr



def getTeamAbv(teamName):
    if teamName=="Australia":
        return "AUS"
    elif teamName=="England":
        return "ENG"
    elif teamName=="New Zealand":
        return "NZ"
    elif teamName=="Pakistan":
        return "PAK"
    elif teamName=="India":
        return "IND"
    elif teamName=="South Africa":
        return "RSA"
    elif teamName=="Zimbabwe":
        return "ZIM"
    elif teamName=="Bangladesh":
        return "BAN"
    elif teamName=="Ireland":
        return "IRL"
    elif teamName=="West Indies":
        return "WI"
    elif teamName=="Sri Lanka":
        return "SL"
    elif teamName=="Scotland":
        return "SCO"
    else:
        return teamName


def getTime(timeString,Day):
    months=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthsNum=['1','2','3','4','5','6','7','8','9','10','11','12']
    GMT=timeString.split(" | ")[0]
    GMT=timeString.split(" ")[0]
    GMTHour=GMT.split(":")[0]
    try:
        GMTMinutes=GMT.split(":")[1]
    except:
        GMTMinutes="00"
    GMTMonth=Day.split(" ")[0].strip()
    GMTDay=Day.split(" ")[1]
    GMTMonth=getMonthNumber(GMTMonth)
    if (GMTMonth+1)<datetime.now().month:
        GMTYear=datetime.now().year+1
    else:
        GMTYear=datetime.now().year
    MatchGMT=datetime.strptime(str(GMTYear) + " " + str(GMTMonth) + " "+GMTDay + " "+ GMTHour + " " + GMTMinutes,"%Y %m %d %H %M")
    return MatchGMT


'''I swear there is a better way to do this'''
def getMonthNumber(string):
    if string=='Jan':
        return 1
    elif string=='Feb':
        return 2
    elif string=='Mar':
        return 3
    elif string=='Apr':
        return 4
    elif string=='May':
        return 5
    elif string=='Jun':
        return 6
    elif string=='Jul':
        return 7
    elif string=='Aug':
        return 8
    elif string=='Sep':
        return 9
    elif string=='Oct':
        return 10
    elif string=='Nov':
        return 11
    elif string=='Dec':
        return 12

'''Return n number of matches that are 1) Not women's games and 2) Not kids games'''
def returnMatchesWeCareAbout(fixturesData,n):
    fixturesWeCareAbout={}
    j=0
    teamsWeCareAbout = ['Australia', 'England', 'New Zealand', 'Pakistan', 'India', 'South Africa', 'Zimbabwe', 'Bangladesh', 'West Indies', 'Sri Lanka']
    for i in fixturesData:
        if ((fixturesData[i]['TeamOne'] in teamsWeCareAbout) or (fixturesData[i]['TeamTwo'] in teamsWeCareAbout)):
            if ((fixturesData[i]['TeamOne'].find("Under-19")==-1) and (fixturesData[i]['TeamOne'].find("Under-23")==-1) and (fixturesData[i]['TeamOne'].find("Women")==-1)):
                fixturesWeCareAbout[j]={}
                fixturesWeCareAbout[j]=fixturesData[i]
                j+=1
                if j==n:
                    return fixturesWeCareAbout
    return fixturesWeCareAbout

def getFixturesDictionary(n):
    fixturesData = {}
    url='http://www.espncricinfo.com/ci/content/match/fixtures/index.html?days=45'
    fixturesData = readInternationalFixtures(url, fixturesData)
    fixturesData = returnMatchesWeCareAbout(fixturesData,n)
    return fixturesData


