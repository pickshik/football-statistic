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


if __name__ == "__main__":
    for y in match_history(u'Зенит', u'Спартак'):
        for x in y:
            print(x, end=' | ')
        print()

    #match_history(u'Реал', u'Анжи')
