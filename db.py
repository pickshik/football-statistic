#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import Connection
from graber import grab_team


championats = set({'http://www.sports.ru/stat/football/russia',
                'http://www.sports.ru/stat/football/england',
                'http://www.sports.ru/stat/football/germany',
                'http://www.sports.ru/stat/football/spain',
                'http://www.sports.ru/stat/football/italy',
                'http://www.sports.ru/stat/football/france',
                'http://www.sports.ru/stat/football/holland',
                'http://www.sports.ru/stat/football/portugal',
                'http://www.sports.ru/stat/football/turkey',
                'http://www.sports.ru/stat/football/switzerland',
                'http://www.sports.ru/stat/football/belgium',
                'http://www.sports.ru/stat/football/ukraine',
                'http://www.sports.ru/stat/football/greece',
                'http://www.sports.ru/stat/football/scotland',
                'http://www.sports.ru/stat/football/sweden',
                'http://www.sports.ru/stat/football/belarus',
                'http://www.sports.ru/stat/football/finland',
                'http://www.sports.ru/stat/football/iceland',
})

DB_URI = '127.0.0.1'


def get_db_cursor():
    """
    Возвращает сылку на коллекцию
    """
    cursor = Connection(DB_URI)
    return cursor.fstatistic


def add2bd():
    db = get_db_cursor()
    teams = db.teams
    for champ in championats:
        for team, team_uri in grab_team(champ).items():
            tm = teams.find_one({team: team_uri})
            if not tm:
                print 'Add {0}:{1}'.format(team.encode('utf-8'), team_uri.encode('utf-8'))
                teams.insert({team: team_uri})
            else:
                print '{0}:{1} exist'.format(team.encode('utf-8'), team_uri.encode('utf-8'))


if __name__ == '__main__':
	add2bd()
