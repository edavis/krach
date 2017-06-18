#!/usr/bin/env python

from kenpom import parse_games
from collections import defaultdict

wins = defaultdict(int)
losses = defaultdict(int)
opps = defaultdict(list)
count = 0
last_game = ''
teams = set()

for game in parse_games('cbbga17.txt'):
    home = game['home']
    hscore = game['hscore']
    visitor = game['visitor']
    vscore = game['vscore']

    teams.add(home)
    teams.add(visitor)

    if hscore > vscore:
        wins[home] += 1
        losses[visitor] += 1
    else:
        wins[visitor] += 1
        losses[home] += 1

    opps[home].append(visitor)
    opps[visitor].append(home)

    count += 1
    last_game = game['date']

teams = sorted(teams)
ratings = {team: 100.0 for team in teams}
iterations = 0

while True:
    new_ratings = ratings.copy()
    delta = 0.0

    for team in teams:
        new_ratings[team] = wins[team] * sum(1 / (ratings[team] + ratings[opp]) for opp in opps[team]) ** -1
        team_delta = abs(new_ratings[team] - ratings[team])
        delta += team_delta

    ratings = new_ratings.copy()

    if delta < 0.0001:
        break

    iterations += 1

print "NCAA D-1 Men's College Basketball -- KRACH Ratings"
print 'Most recent game = {} ({} games total)'.format(last_game, count)
print 'Data courtesy of kenpom.com'
print
print '{: >3s}  {:25s}{:>10s}  {:^7s}'.format('Rnk', 'Team', 'Rating', 'W-L')
s = sorted(ratings.items(), key=lambda e: e[1], reverse=True)
for idx, (team, rating) in enumerate(s, 1):
    print '{: >3d}  {:25s}{:10.3f}  ({:d}-{:d})'.format(idx, team, rating, wins[team], losses[team])
