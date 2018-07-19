import nsq
import os
import time
import tornado.ioloop
from datetime import datetime
import json
import logging
import random
import nsq_server.config as Config

# Write message every second to a topic
TOPIC = os.environ.get('topic', 'topic')
NSQD = os.environ.get('nsqd', '127.0.0.1:4150')
START_DATE = datetime(2018,1,1,0,0,0).strftime(Config.DATE_FORMAT)
END_DATE = datetime(2018,3,1,0,0,0).strftime(Config.DATE_FORMAT)
LOGGER_LEVEL = logging.getLevelName(os.environ.get('LOGGER_LEVEL', 'WARN'))
logging.getLogger('nsq').setLevel(LOGGER_LEVEL)


def strTimeProp(start, end, date_format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, date_format))
    etime = time.mktime(time.strptime(end, date_format))

    ptime = stime + prop * (etime - stime)
    return datetime.fromtimestamp(ptime).strftime(date_format)


def randomDate(start, end, prop):
    return strTimeProp(start, end, Config.DATE_FORMAT, prop)

def pub_message():

    start_date = randomDate(START_DATE, END_DATE, random.random())
    end_date = randomDate(start_date, END_DATE, random.random())
    now = (datetime.now() - datetime(1970,1,1)).total_seconds()
    msg = {
        'start_date': start_date,
        'end_date': end_date,
        'timestamp': now,
        'timestamp_iso': datetime.now().strftime(Config.DATE_FORMAT)
    }
    logging.info('publishing a message')
    writer.pub(TOPIC, json.dumps(msg), finish_pub)

def finish_pub(conn, data):
    logging.info(data)
    logging.info(conn)

writer = nsq.Writer([NSQD])
tornado.ioloop.PeriodicCallback(pub_message, 1000).start()
nsq.run()

