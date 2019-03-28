import datetime
import os
from config import config
import logging

def log_msg(msg):
    logger = logging.getLogger()
    logger.info(msg)

def log(msg):
    log_msg(msg)

def log_normal(msg):
    log_msg("%s: %s" % (datetime.datetime.now(), msg))

def log_error(msg):
    log_msg("%s: ERROR: - %s" % (datetime.datetime.now(), msg))

def log_warning(msg):
    log_msg("%s: WARNING - %s" % (datetime.datetime.now(), msg))

def log_debug(msg):
    log_msg("%s: DEBUG - %s" % (datetime.datetime.now(), msg))
