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

