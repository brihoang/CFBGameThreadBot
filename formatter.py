import grabData
def make_table(mat):
    ret = "|"
    for e in mat[0]:
        ret += str(e) + '|'
    ret += '\n|:'

    for x in xrange(len(mat[0]) - 1):
        ret += '-:|:'
    ret += '-:|\n'
    for line in mat[1:]:
        ret += '|'
        for e in line:
            ret += str(e) + '|'
        ret += '\n'
    return ret

def make_line_score(team1Name, team1Scores, team2Name, team2Scores):
    header = ['',1,2,3,4]
    for x in xrange(len(team1Scores) - 5):
        app = 'OT'
        if x > 0:
            app += str(x+ 1)
        header.append(app)
    header.append('Total')
    team1 = [team1Name] + team1Scores 
    team2 = [team2Name] + team2Scores 

    line = [header, team1, team2]
    return make_table(line)

def make_box_score(awayTeam, homeTeam):
	ret = '#' + awayTeam + ' vs. ' + homeTeam + '\n\n'
	ret += grabData.getLineScore()
	ret += '\n#Passing Stats\n\n'
	ret += grabData.getStats('passing')
	ret += '\n#Rushing Stats\n\n'
	ret += grabData.getStats('rushing')
	ret += '\n#Receiving Stats\n\n'
	ret += grabData.getStats('receiving')
	ret += '\n#Interception Stats\n\n'
	ret += grabData.getStats('interceptions')
	ret += '\n#Kick Return Stats\n\n'
	ret += grabData.getStats('kickReturns')
	ret += '\n#Punt Return Stats\n\n'
	ret += grabData.getStats('puntReturns')
	ret += '\n#Kicking Stats\n\n'
	ret += grabData.getStats('kicking')
	ret += '\n#Punting Stats\n\n'
	ret += grabData.getStats('punting')
	ret += '\n#Team Stats\n\n'
	ret += grabData.getTeamStats()
	return ret
