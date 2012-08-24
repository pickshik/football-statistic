#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import Connection
from graber import grab_team, grab_calendar, match_history, grab_team_static



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
                'http://www.sports.ru/stat/football/iceland'})

DB_URI = '127.0.0.1'


def get_db():
    """
    Возвращает курсор
    """
    return Connection(DB_URI)


def get_db_cursor():
    """
    Возвращает ссылку на коллекцию
    """
    cursor = get_db()
    return cursor.fstatistic


def get_studydb_cursor():
    """
    Возвращает ссылку на коллекцию для обучения
    """
    cursor = get_db()
    return cursor.study


def add2bd():
    """
    Добавляет в базу название команды
    """
    db = get_db_cursor()
    teams = db.teams
    for champ in championats:
        for team, team_uri in grab_team(champ).items():
            tm = teams.find_one({'name': team})
            if not tm:
                print 'Add {0}:{1}'.format(team.encode('utf-8'), team_uri.encode('utf-8'))
                teams.insert({'name': team, 'uri': team_uri})
            else:
                print '{0}:{1} exist'.format(team.encode('utf-8'), team_uri.encode('utf-8'))


def add2studydb():
    """
    Добавляет в базу данные для обучения
    """
    db = get_studydb_cursor()
    matches = db.matches

    db2 = get_db_cursor()
    teams = db2.teams

    for champ in championats:
        for team1, score, team2 in grab_calendar(champ):
            data = {}
            print team1, score, team2
            data.update({team1 + '_' + team2: {'score': score}})

            data[team1 + '_' + team2].update({'meet': []})
            for y in match_history(team1, team2):
                if y != [] and y[0] != u'Дата':
                    print y[2] + '_' + y[5] + ':' + y[7] + '_' + y[4]
                    data[team1 + '_' + team2]['meet'].append(y[2] + '_' + y[5] + ':' + y[7] + '_' + y[4])

            tm1 = teams.find_one({'name': team1})
            if not tm1:
                print('Команды с названием {0} нет :('.format(team1.encode('utf-8')))
            else:
                print(team1)
                print()
                data[team1 + '_' + team2].update({team1: {}})
                for name, dat in grab_team_static(tm1['uri'] + '?type=champ').items():
                    try:
                        print(name + ': ' + dat)
                        data[team1 + '_' + team2][team1].update({name: dat})
                    except TypeError:
                        continue

            tm2 = teams.find_one({'name': team2})
            if not tm2:
                print('Команды с названием {0} нет :('.format(team2.encode('utf-8')))
            else:
                print()
                print(team2)
                print()
                data[team1 + '_' + team2].update({team2: {}})
                for name, dat in grab_team_static(tm2['uri'] + '?type=champ').items():
                    try:
                        print(name + ': ' + dat)
                        data[team1 + '_' + team2][team2].update({name: dat})
                    except TypeError:
                        continue

            matches.insert(data)


if __name__ == '__main__':
    add2bd()
    #add2studydb()
