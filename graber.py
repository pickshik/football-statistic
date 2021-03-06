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
        return []
    else:
        try:
            all_table = g.xpath('/html/body/table[4]/tr/td[2]/table')
        except IndexError:
            return []
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


def grab_team_static(uri):
    """
    Функция которая возвращает словарь со статистикой выступления команды
    """
    def from_info(d):
        temp = []
        for x in d:
            if x.text == None:
                temp.append(x.xpath('b')[0].text)
            else:
                temp.append(x.text)
        return {temp[0]: temp[1]}

    def from_table(d):
        temp = []
        for x in d:
            if x.text == None:
                temp.append('0')
            else:
                temp.append(x.text.strip())
        return {temp[0]: ' '.join(temp[1:])}

    def get_date(uri):
        g = Grab()
        g.go(uri)

        try:
            t = g.xpath('/html/body/div[4]/div[3]/div/div[3]/div[3]/p[2]')
        except IndexError:
            return None
        return t.text

    data = {}
    g = Grab()
    g.go(uri)

    try:
        t = g.css('div.pageLayout div.contentLayout div.box div.layout-columns.second-page div.mainPart div.info-block div.about table tbody')
    except IndexError:
        pass
    data.update(from_info(t.xpath('tr[1]/td')))
    data.update(from_info(t.xpath('tr[2]/td')))
    for x in t.xpath('tr[3]/td[2]/span/a'):
        data.update({x.values()[0]: get_date('http://www.sports.ru' + x.values()[-1])})

    try:
        t = g.xpath('/html/body/div/div[3]/div/div/div/div[5]/table/tbody')
    except IndexError:
        pass
    for y in t:
        data.update(from_table(y))

    return data


def grab_calendar(uri):
    """
    Функция возвращет множество в котором сожержаться кортежи из 3 элементов
    1 элемент - 1 команда, 2 элемент - счет, 3 элемент - 2 команда
    """
    data = set()

    g = Grab()
    g.go(uri)

    try:
        t = g.xpath('/html/body/div[4]/div[3]/div/div/div/div[4]/div[2]/table/tbody')
    except IndexError:
        return data
    for y in t:
        data.add((y.xpath('td[3]/div/a')[0].text, y.xpath('td[4]/a/b')[0].text, y.xpath('td[5]/div/a')[0].text))

    return data


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

    for name, data in grab_team_static('http://www.sports.ru/tags/1044511.html?type=champ').items():
        try:
            print(name + ': ' + data)
        except TypeError:
            print('fail')

    print(grab_calendar('http://www.sports.ru/stat/football/russia'))
