#!/usr/bin/env python
import logging
import functools
from threading import Timer
from time import sleep
from tornado.gen import coroutine, sleep
import tornado
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
import ijson


class RepeatedTimer(object):
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


class Message():
    executor = ThreadPoolExecutor(max_workers=1)

    @coroutine
    def process_message(self, message):
        # Enables asynchronous processing for this message.
        logging.info('incoming message')

        message.enable_async()
        logging.info('body: {}'.format(message.body))
        logging.info('has message responded? {}'.format(message.has_responded()))

        if message.has_responded() == False:
            rt = RepeatedTimer(5, message)
            logging.info('has message responded? {}'.format(message.has_responded()))
            try:
                # Process message
                logging.info('read json...')
                result = yield read_json()
                logging.info(result)

                logging.info('gen sleeping..')
                yield sleep(10)
                logging.info('gen sleeping..done.')

                logging.info(message.body)
                logging.info('sleep is done.')

            except Exception as err:
                logging.error(err)
                requeue_message(message)
            finally:
                logging.info('finally start.')
                rt.stop() # better in a try/finally block to make sure the program ends!


@coroutine
def requeue_message(message):
    logging.info('requeue message')
    message.requeue()


@coroutine
def finish_message(message):
    logging.info('Finish message')
    message.finish()

@coroutine
def read_json():
    data_result_file_path = '~/github/py-nsq-tornado/python/server/test.json'
    arr = []
    logging.info('opening {}'.format(data_result_file_path))
    with open(data_result_file_path, 'r') as json_file:
        items = ijson.items(json_file, 'item')
        logging.info(items)
        for item in items:
            logging.info(item)
            arr.append(item)
    return arr
