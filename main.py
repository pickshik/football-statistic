#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from db import get_db_cursor, championats
from graber import grab_team_static, match_history, grab_calendar


def main_out(team1, team2):
    def key_for_sort(x):
        if x[0] != None and x[1] != None:
            return len(x[0] + x[1])

    print('#----------------------------------------- {0} - {1} ---------------------------#'.format(team1.encode('utf-8'), team2.encode('utf-8')))
    for y in match_history(team1, team2):
            for x in y:
                print(x, end=' | ')
            print()

    db = get_db_cursor()
    teams = db.teams
    print('-*-'*20)

    tm1 = teams.find_one({'name': team1})
    if not tm1:
        print('Команды с названием {0} нет :('.format(team1.encode('utf-8')))
    else:
        print(team1)
        print("-"*40)
        for name, data in iter(sorted(grab_team_static(tm1['uri'] + '?type=champ').items(), key=key_for_sort)):
            try:
                print(name + ': ' + data)
            except TypeError:
                continue
    print('-*-'*20)

    tm2 = teams.find_one({'name': team2})
    if not tm2:
        print('Команды с названием {0} нет :('.format(team2.encode('utf-8')))
    else:
        print(team2)
        print("-"*40)
        for name, data in iter(sorted(grab_team_static(tm2['uri'] + '?type=champ').items(), key=key_for_sort)):
            try:
                print(name + ': ' + data)
            except TypeError:
                continue
    print('-*-'*20)


if __name__ == '__main__':
    import argparse

    def right_args(args):
        if len(args) > 1:
            return ' '.join(args)
        else:
            return args[0]

    parser = argparse.ArgumentParser(add_help=True, version='0.0.1')
    parser.add_argument("-team1", nargs='*', action="store", required=True, dest='team1', help="the name of the first team")
    parser.add_argument("-team2", nargs='*', action="store", required=True, dest='team2', help="the name of the second team")
    args = parser.parse_args()
    team1 = right_args(args.team1)
    team2 = right_args(args.team2)
    main_out(unicode(team1, "utf-8"), unicode(team2, "utf-8"))
