import formatter
from bs4 import BeautifulSoup
from urllib2 import urlopen
BASE_URL = "http://espn.go.com/college-football/boxscore?gameId="
TEAM_STATS_URL = "http://espn.go.com/college-football/matchup?gameId=" 
homeTeam = ''
awayTeam = ''

def setUpTeams():
    global homeTeam
    global homeTeamNick
    global awayTeam
    global awayTeamNick

    teams = soup.find_all('a', 'team-name')


    awayTeam = teams[0].find('span', 'long-name').getText()
    homeTeam = teams[1].find('span', 'long-name').getText()
    awayTeamNick = teams[0].find('span', 'short-name').getText()
    homeTeamNick = teams[1].find('span', 'short-name').getText()

def getHomeTeam():
    return homeTeam + " " + homeTeamNick

def getAwayTeam():
    return awayTeam + " " + awayTeamNick


def setUpGameId(gameId):
    global BASE_URL 
    global TEAM_STATS_URL
    global html
    global soup
    global teamHtml
    global teamSoup
    BASE_URL += str(gameId)
    TEAM_STATS_URL += str(gameId)
    html = urlopen(BASE_URL)
    teamHtml = urlopen(TEAM_STATS_URL)
    soup = BeautifulSoup(html, 'lxml')
    teamSoup = BeautifulSoup(teamHtml, 'lxml')

def getLineScore():
    linescore = soup.find_all('td', 'team-name')

    teamNames = []
    teamScores = []
    
    for x in linescore:
        teamNames.append(x.getText())
        score = []
        siblings = x.find_next_siblings()
        for s in siblings:
            score.append(s.getText())
        teamScores.append(score)
    return formatter.make_line_score(teamNames[0], teamScores[0], teamNames[1], teamScores[1])

def getTeamStats():
    finalMat = [[awayTeam,'',homeTeam]]
    stats = teamSoup.find(id='teamstats-wrap')
    rows = stats.find_all('tr')
    
    for r in rows[1:]:
            row = r.find_all('td')
            row[0],row[1] = row[1],row[0]
            currentRow = []
            for x in row:
                    currentRow.append(x.getText().strip())
            finalMat.append(currentRow)
    return formatter.make_table(finalMat)



def getStats(statType):
    stats = soup.find(id= 'gamepackage-' + statType)
    awayStats = stats.find('div', 'gamepackage-away-wrap')
    homeStats = stats.find('div', 'gamepackage-home-wrap')

    header = awayStats.find('thead').find_all('th')
    header[0] = awayTeam
    if statType == 'passing':
        header.pop()

    headerArray = []

    for cat in header:
                    if isinstance(cat, basestring):
                            headerArray.append(cat)
                    else:
                            headerArray.append(cat.getText())
    header[0] = homeTeam 
    for cat in header:
                    if isinstance(cat, basestring):
                            headerArray.append(cat)
                    else:
                            headerArray.append(cat.getText())
    
    awayBody = awayStats.find('tbody').find_all('tr')
    homeBody = homeStats.find('tbody').find_all('tr')

    awayTotal = awayBody[-1]
    homeTotal = homeBody[-1]

    awayBody.pop()
    homeBody.pop()

    numRows = max(len(awayBody), len(homeBody));
    numStats = len(headerArray) / 2
    
    finalMat = [headerArray]

    for x in xrange(numRows):
        row = []
        if x >= len(awayBody):
            row = ['' for y in xrange(numStats)]
        else:
            for stat in awayBody[x].findAll('td'):
                row.append(stat.getText())
            if statType == 'passing':
                row.pop()

        if x >= len(homeBody):
            row += ['' for y in xrange(numStats)]
        else:
            for stat in homeBody[x].findAll('td'):
                row.append(stat.getText())
            if statType == 'passing':
                row.pop()
        finalMat.append(row)
    finalRow = []
    for x in awayTotal:
        finalRow.append(x.getText())
    if statType == 'passing':
        finalRow.pop()
    for x in xrange(numStats - len(awayTotal)):
        finalRow.append('')

     
    for x in homeTotal:
        finalRow.append(x.getText())
    if statType == 'passing':
        finalRow.pop()
    for x in xrange(numStats - len(homeTotal)):
        finalRow.append('')

    finalMat.append(finalRow)

    return formatter.make_table(finalMat)
