#!usr/bi/env python3
#tests

from datetime import timedelta
import unittest
from celery import PeriodicTask

from app.generator import WorldGrid, BlobManager, Player
from . import cel_app

class TestMyCeleryWorker(unittest.Testcase):

    def setUp(self):
        cel_app.conf.update(CELERY_ALWAYS_EAGER=True)

    def tearDown(self):
        cel_app.conf.update(CELERY_ALWAYS_EAGER=False)

    