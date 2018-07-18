#!/usr/bin/env python

import logging
import functools
from tornado.gen import coroutine, sleep
import tornado
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
import ijson
import decimal

class Message():
    executor = ThreadPoolExecutor(max_workers=4)

    @coroutine
    def process_message(self, message):
        # Enables asynchronous processing for this message.
        logging.info('incoming message')

        message.enable_async()
        logging.info('body: {}'.format(message.body))
        logging.info('has message responded? {}'.format(message.has_responded()))

        if message.has_responded() is True:
            return

        rt = TimeInterval(5, message)
        logging.info('has message responded? {}'.format(message.has_responded()))
        try:
            # Process message
            logging.info('read json...')
            result = yield read_json('./data/1/2018/01/2018-01-01T00:00:00.000000Z_2018-01-01T06:00:00.000000Z.json')
            # logging.info(result)

            logging.info('gen sleeping..')
            yield sleep(10)
            logging.info('gen sleeping..done.')

            logging.info(message.body)
            logging.info('sleep is done.')

        except Exception as err:
            logging.error(err)
            rt.stop()
            requeue_message(message)
        finally:
            logging.info('finally start.')
            rt.stop()


@coroutine
def requeue_message(message):
    logging.info('requeue message')
    message.requeue()


@coroutine
def finish_message(message):
    logging.info('Finish message')
    message.finish()


@coroutine
def read_json(data_result_file_path):
    arr = []
    logging.info('opening {}'.format(data_result_file_path))
    counter = 0
    with open(data_result_file_path, 'r') as json_file:
        items = ijson.items(json_file, 'item')
        for item in items:
            counter += 1
            if 'value_a' in item:
                item['value_a'] = parse_decimal(item['value_a'])
            if 'value_b' in item:
                item['value_b'] = parse_decimal(item['value_b'])
            arr.append(item)
    logging.info('JSON size: {}'.format(counter))
    return arr


def parse_decimal(val):
    if isinstance(val, decimal.Decimal):
        return float(val)
    return val