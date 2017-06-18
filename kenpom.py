import re

D1TEAMS = set([line.strip() for line in open('teams.txt')])
assert len(D1TEAMS) == 351, 'incorrect number of D1 teams found'

def is_d1_matchup(a, b):
    return all([a in D1TEAMS, b in D1TEAMS])

def parse_games(fname):
    base = '^(?P<date>[\d/]+)[ ](?P<visitor>.{,22}?)[ ][ ]?(?P<visitor_score>\d{2,3}) (?P<home>.{,22}?)[ ][ ]?(?P<home_score>\d{2,3})'
    result = re.compile(base)
    result_extra = re.compile(base + '[ ](?P<extra>.{,3})')
    fp = open(fname)

    for game_id, line in enumerate(fp, 1):
        if len(line) == 65:
            obj = result.search(line).groupdict()
        else:
            obj = result_extra.search(line).groupdict()

        extra = obj.get('extra', '')

        home = obj['home'].strip()
        visitor = obj['visitor'].strip()

        if not is_d1_matchup(home, visitor):
            continue

        yield {
            'game_id': game_id,
            'date': obj['date'],
            'visitor': visitor,
            'vscore': int(obj['visitor_score']),
            'home': home,
            'hscore': int(obj['home_score']),
            'extra': extra,
            'overtime': re.search('[1-9]', extra),
            'neutral': re.search('[Nn]', extra),
        }
