#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configparser
import logging
import time

from common.boss import Boss

log_format = "%(asctime)s %(process)s %(levelname)s [-] %(message)s"
log_level = logging.INFO
logging.basicConfig(format=log_format, level=log_level)

JOB_CONF = "boss_jobs.conf"

# Get jobs and filter from config file
jobs = {}

config = configparser.ConfigParser()
config.read(JOB_CONF)

for job_name in config.sections():
    jobs[job_name] = {
        "filters": config[job_name]["filters"].split(","),
        "max_say_hi": config.getint(job_name, "max_say_hi")
    }

logging.info("Jobs: %s" % jobs)

boss = Boss()
boss.wait_scan_login()

boss.goto_recommend_page()

for job, conditions in jobs.items():
    logging.info("Begin to filter job %s..." % job)

    filters = conditions["filters"]
    logging.info("Filter Conditions is %s" % filters)

    max_say_hi = conditions["max_say_hi"]

    boss.filter_job_name(job)

    boss.filter_persons(filters)
    boss.say_hi(max_say_hi)

    time.sleep(5)
