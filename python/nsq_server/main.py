#!/usr/bin/env python
import logging
import os
import json
import tornado.options
import ssl
import nsq
import config as Config
from message import Message


logging.raiseExceptions = False
logging.basicConfig(level=Config.LOGGER_LEVEL)
logger = logging.getLogger(__name__)
# Set nsq logger level to warning
# logging.getLogger('nsq').setLevel(logging.WARNING)


# The server start by listening for incoming messages
# on nsq. once a message receive it will handle by `message_handler`
if __name__ == '__main__':
    tornado.options.parse_command_line()
    logger.info("Server start")
    logger.info('Listen on Topic: {}'.format(Config.NSQ_TOPIC))
    message_instance = Message()
    reader = nsq.Reader(
        topic=Config.NSQ_TOPIC,
        channel=Config.NSQ_CHANNEL,
        nsqd_tcp_addresses=[Config.NSQD_TCP_ADDRESS],
        message_handler=message_instance.process_message,
        heartbeat_interval=10,
        output_buffer_size=4096,
        output_buffer_timeout=100,
        user_agent='exporter',
        lookupd_poll_interval=15,
        max_in_flight=1
    )
    nsq.run()