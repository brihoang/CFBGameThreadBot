import formatter
from bs4 import BeautifulSoup
from urllib2 import urlopen
BASE_URL = "http://espn.go.com/college-football/boxscore?gameId="

def setUpGameId(gameId):
    global BASE_URL 
    global html
    global soup
    BASE_URL += str(gameId)
    html = urlopen(BASE_URL)
    soup = BeautifulSoup(html, 'lxml')

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

def getStats(statType):
	stats = soup.find(id= 'gamepackage-' + statType)
	awayStats = stats.find('div', 'gamepackage-away-wrap')
	homeStats = stats.find('div', 'gamepackage-home-wrap')

        header = awayStats.find('thead').find_all('th');
        if statType == 'passing':
            header.pop()

        headerArray = []

        for cat in header:
            headerArray.append(cat.getText())
        for cat in header:
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

            print x
            print len(homeBody)
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
        for x in xrange(numStats - len(awayTotal)):
            finalRow.append('')

         
        for x in homeTotal:
            finalRow.append(x.getText())
        for x in xrange(numStats - len(homeTotal)):
            finalRow.append('')

        finalMat.append(finalRow)

        return formatter.make_table(finalMat)
