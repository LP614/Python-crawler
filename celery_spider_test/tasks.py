#-*- coding: utf-8 -*-
'''
---------------

Description of this file

:author: Luopeng
:date created: 2019-11-28
:python version: 3.6

---------------
'''
from __future__ import absolute_import
from celery_test import app


@app.task
def daily_spider_001():
    return 1 + 2


@app.task
def daily_spider_002():
    return 2 + 2


@app.task
def daily_spider_003():
    return 3 + 2