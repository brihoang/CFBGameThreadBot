def make_table(mat):
    ret = "|"
    for e in mat[0]:
        ret += str(e) + '|'
    ret += '\n|:'

    for x in xrange(len(mat[0]) - 1):
        ret += '-:|:'
    ret += '-:|\n|'
    for line in mat[1:]:
        for e in line:
            ret += str(e) + '|'
        ret += '\n'
    return ret

def make_line_score(team1Name, team1Scores, team2Name, team2Scores):
    header = ['',1,2,3,4]
    for x in xrange(len(team1Scores) - 4):
        app = 'OT'
        if x > 0:
            app += str(x+ 1)
        header.append(app)
    header.append('Total')
    team1 = [team1Name] + team1Scores 
    team1.append(sum(team1Scores))
    team2 = [team2Name] + team2Scores 
    team2.append(sum(team2Scores))

    line = [header, team1, team2]
    return make_table(line)
