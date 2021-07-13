#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This scripts is used to get CV list from potentials"""

#import configparser
import logging
import time

from common.boss import Boss

log_format = "%(asctime)s %(process)s %(levelname)s [-] %(message)s"
log_level = logging.INFO
logging.basicConfig(format=log_format, level=log_level)

JOB_CONF = "boss_jobs.conf"

boss = Boss()
boss.wait_scan_login()

boss.get_cv()
