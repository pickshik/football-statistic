#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from db import get_db_cursor
from graber import grab_team_static, match_history


def main(team1, team2):
    print('Играют {0} - {1}'.format(team1.encode('utf-8'), team2.encode('utf-8')))
    for y in match_history(team1, team2):
            for x in y:
                print(x, end=' | ')
            print()

    db = get_db_cursor()
    teams = db.teams

    tm1 = teams.find_one({'name': team1})
    if not tm1:
        print('Команды с названием {0} нет :('.format(team1.encode('utf-8')))
    else:
        print(team1)
        print()
        for name, data in grab_team_static(tm1['uri'] + '?type=champ').items():
            print(name + ': ' + data)

    tm2 = teams.find_one({'name': team2})
    if not tm2:
        print('Команды с названием {0} нет :('.format(team2.encode('utf-8')))
    else:
        print()
        print(team2)
        print()
        for name, data in grab_team_static(tm2['uri'] + '?type=champ').items():
            print(name + ': ' + data)


if __name__ == '__main__':
    main(u'Спартак', u'Рубин')
