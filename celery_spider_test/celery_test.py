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
from celery import Celery


app = Celery(include=['tasks'])
app.config_from_object('celeryconfig')
if __name__ == '__main__':
    app.start()
