import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime, date
import pandas as pd
import numpy as np
import html5lib
import predictionParameters

# Note: this code was strongly borrowed from http://www.danielforsyth.me/exploring_nba_data_in_python/
year = predictionParameters.predictionYear

gamesFile = './games' + str(year) + '.csv'
BASE_URL = 'http://espn.go.com/nba/boxscore?gameId={0}'
outputFile = './players' + str(year) + '.csv'

pointsForPoints = 1
pointsForThree = 0.5
pointsForRebound = 1.25
pointsForAssist = 1.5
pointsForSteal = 2
pointsForBlock = 2
pointsForTurnover = -.5
pointsForDoubleDouble = 1.5
pointsForTripleDouble = 3

games =  pd.read_csv(gamesFile)

request = requests.get(BASE_URL.format(games['id'][0]))
# print request.url
table = BeautifulSoup(request.text).find('table', class_='mod-data')
# print table.prettify()
heads = table.find_all('thead')
headers = heads[0].find_all('tr')[1].find_all('th')[1:]
headers = [th.text for th in headers]
headers[1] = 'FGM'
headers[2] = '3PM'
headers[3] = 'FTM'
headers.insert(4, 'FTA')
headers.insert(3, '3PA')
headers.insert(2, 'FGA')
headers.append('DKPoints')
print headers

columns = ['id', 'team', 'player'] + headers + ['position']

players = pd.DataFrame(columns=columns)

def get_players(players, team_name):
	array = np.zeros((len(players), len(headers)+2), dtype=object)
	array[:] = np.nan
	for i, player in enumerate(players):
		cols = player.find_all('td')
		# print "#########################################################"
		# print cols[0].text
		# break
		array[i, 0] = cols[0].text.split(',')[0]
		playerPosition = cols[0].text.split(',')[1]
		# print array[i, 0]
		k = 1
		for j in range(1, len(headers) - 3):
			# print "%d %s" % (k, headers[k])
			if not cols[1].text.startswith('DNP'):
				array[i, k] = cols[j].text
				# print cols[j].text
				if j in (2, 3, 4):
					text = cols[j].text
					made = text.split('-')[0]
					attempted = text.split('-')[1]
					array[i, k] = made
					k = k+1
					array[i, k] = attempted
			k = k+1
		for m in xrange(1, len(array[i])):
			array[i][m] = float(array[i][m])
			# print "%d %s %s" % (m, headers[m-1], array[i, m])
		# print headers
		(points, rebounds, assists, blocks, steals) = array[i][17], array[i][10], array[i][11], array[i][13], array[i][12]
		doubleDoubles = tripleDoubles = 0
		numDoubles = 0
		if points >= 10: numDoubles+=1
		if rebounds >= 10: numDoubles+=1
		if assists >= 10: numDoubles+=1
		if blocks >= 10: numDoubles+=1
		if steals >= 10: numDoubles+=1
		if numDoubles >= 3:
			doubleDoubles += 1
			tripleDoubles += 1
		elif numDoubles == 2:
			doubleDoubles += 1

		DKPoints = (points*pointsForPoints + array[i][4]*pointsForThree + rebounds*pointsForRebound + 
			assists*pointsForAssist + steals*pointsForSteal + blocks*pointsForBlock + 
			array[i][14]*pointsForTurnover + doubleDoubles*pointsForDoubleDouble + tripleDoubles*pointsForTripleDouble)
		array[i][18] = DKPoints
		# print array[i]
	# print array
	# print "9999999999999999999999999999999999999999999999999999"
		array[i][19] = playerPosition
	frame = pd.DataFrame(columns=columns)
	for x in array:
		# print x
		line = np.concatenate(([index, team_name], x)).reshape(1,len(columns))
		new = pd.DataFrame(line, columns=frame.columns)
		frame = frame.append(new)
	return frame

gameIndices = []

for index, row in games[:].iterrows():
# for index, row in games.iterrows():
    print index
    print row[0]
    gameIndices.append(row[0])
    # print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    request = requests.get(BASE_URL.format(row['id']))
    # print request.url
    table = BeautifulSoup(request.text, 'html5lib').find('table', class_='mod-data')
    # print table.prettify()
    heads = table.find_all('thead')
    bodies = table.find_all('tbody')

    team_1 = heads[0].th.text
    # print team_1
    team_1_players = bodies[0].find_all('tr') + bodies[1].find_all('tr')
    team_1_players = get_players(team_1_players, team_1)
    team_1_players['game_id'] = row[0]
    
    players = players.append(team_1_players)
    
    team_2 = heads[3].th.text
    team_2_players = bodies[3].find_all('tr') + bodies[4].find_all('tr')
    team_2_players = get_players(team_2_players, team_2)
    team_2_players['game_id'] = row[0]
    players = players.append(team_2_players)

players = players.set_index('id')
players = pd.merge(players, games, on='game_id')
print players
players.to_csv(outputFile)


