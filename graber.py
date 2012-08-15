#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import urllib
from grab import Grab


def match_history(first_team, second_team, n_last_match=5):
    """
    Функция которая возвращает таблицу из n_last_match последних
    матчей между командами first_team и second_team
    """
    URI = "http://www.sportzone.ru/sport/search.html?com1={0}&com2={1}&sport=1&rows={2}&search=%CF%EE%E8%F1%EA".format(urllib.quote_plus(first_team.encode('cp1251')), urllib.quote_plus(second_team.encode('cp1251')), n_last_match)
    g = Grab(log_file="/tmp/graber.log")
    g.go(URI)
    if g.search(u'Ранее не встречались'):
        print('fail')
    else:
        try:
            all_table = g.xpath('/html/body/table[4]/tr/td[2]/table')
        except IndexError:
            print('fail')
        answer = []
        for y in all_table:
            a_temp = []
            for x in y:
                if x.text == None:
                    temp = x.xpath('a')
                    if len(temp) > 0 and temp[0].text != None:
                        a_temp.append(temp[0].text)
                else:
                    a_temp.append(x.text)
            answer.append(a_temp)
    return answer


def grab_team(uri):
    """
    Функция из сайта sports.ru выдирает название команд и возварщает список из них
    """
    teams = {}
    g = Grab()
    g.go(uri)
    try:
        get_teams = g.css_list('div.pageLayout div.contentLayout div.box div.layout-columns.second-page div.mainPart div.match-center div.tabs-container div ul li.panel.active-panel div.stat.mB6 table.stat-table.table tbody tr td.name-td.alLeft.bordR a')
    except IndexError:
        return teams
    for t in get_teams:
        teams.update({t.text: t.items()[0][1]})
    return teams


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        for y in match_history(unicode(sys.argv[1], 'utf-8'), unicode(sys.argv[2], 'utf-8')):
            for x in y:
                print(x, end=' | ')
            print()
    else:
        for y in match_history(u'Англия', u'Италия'):
            for x in y:
                print(x, end=' | ')
            print()
    print(grab_team('http://www.sports.ru/stat/football/russia/'))
