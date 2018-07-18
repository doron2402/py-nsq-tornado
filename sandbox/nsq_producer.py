import nsq
import os
import time
import tornado.ioloop
import json
import logging

# Write message every second to a topic
TOPIC = os.environ.get('topic', 'topic')
NSQD = os.environ.get('nsqd', '127.0.0.1:4150')
LOGGER_LEVEL = logging.getLevelName(os.environ.get('LOGGER_LEVEL', 'WARN'))
logging.getLogger('nsq').setLevel(LOGGER_LEVEL)


def pub_message():
    msg = {
      'time': time.strftime('%H:%M:%S')
    }
    logging.info('publishing a message')
    writer.pub(TOPIC, json.dumps(msg), finish_pub)

def finish_pub(conn, data):
    logging.info(data)
    logging.info(conn)

writer = nsq.Writer([NSQD])
tornado.ioloop.PeriodicCallback(pub_message, 1000).start()
nsq.run()

