#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
        print 'fail'
    else:
        print 'ok'


if __name__ == "__main__":
    match_history(u'Зенит', u'Спартак')
    match_history(u'Реал', u'Анжи')
