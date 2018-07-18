#!/usr/bin/env python

import logging
from threading import Timer

class TimeInterval(object):
    def __init__(self, interval, message, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.message    = message
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        logging.info('message touch id: {}'.format(self.message.id))
        self.message.touch()

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        logging.info('stop touching the message')
        self._timer.cancel()
        self.is_running = False
        finish_message(self.message)
