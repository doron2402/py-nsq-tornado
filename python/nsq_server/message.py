#!/usr/bin/env python

import logging
import functools
from tornado.gen import coroutine, sleep
import tornado
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
import ijson
import json
import decimal

import nsq_server.config as Config
from nsq_server.time_interval import TimeInterval
from nsq_server.files import get_list_of_files_by_dates

TOUCH_INTERVAL = 5 # 5 seconds

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

        rt = TimeInterval(TOUCH_INTERVAL, message)
        logging.info('has message responded? {}'.format(message.has_responded()))

        try:
            parsed_message = json.loads(message.body)
            # Calculate files
            logging.info('read data from {} to {}'.format(
                parsed_message.get('start_date'),
                parsed_message.get('end_date')
            ))
            # Process message
            logging.info('read json...')
            list_of_files = yield get_list_of_files_by_dates(
                parsed_message.get('start_date'),
                parsed_message.get('end_date')
            )
            logging.info(list_of_files)
            result = yield read_json('./data/1/2018/01/20180108T120000_20180108T180000.json')
            # logging.info(result)

            logging.info('gen sleeping..')
            yield sleep(10)
            logging.info('gen sleeping..done.')

            logging.info(message.body)
            logging.info('sleep is done.')

        except Exception as err:
            logging.info(err)
            logging.error(err)
            rt.stop()
            # Requeue message something went wrong...
            requeue_message(message)
        finally:
            logging.info('finally start.')
            rt.stop()
            # Finish message
            message.finish()
            # finish_message(message)


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