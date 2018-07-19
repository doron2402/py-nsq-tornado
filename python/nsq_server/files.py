#!/usr/bin/env python

from datetime import datetime
import logging
from tornado.gen import coroutine
import nsq_server.config as Config
from os import path, listdir

def get_year_from_dt(dt):
    return '{}'.format(dt.year)

def get_month_from_dt(dt):
    if dt.month < 10:
        return '0{}'.format(dt.month)
    return '{}'.format(dt.month)


@coroutine
def get_list_of_files_by_dates(start, end):
    # parse start & end dates
    result = []
    start_date = datetime.strptime(start, Config.DATE_FORMAT)
    end_date = datetime.strptime(end, Config.DATE_FORMAT)
    year = get_year_from_dt(start_date)
    month = get_month_from_dt(start_date)
    directory = '/Users/doronsegal/github/py-nsq-tornado/data/1/{}/{}'.format(year, month)
    logging.info('Looking for directory {}'.format(directory))
    # Check if directory exist
    if path.exists(directory) == False:
        logging.warning('Directory ({}) not found'.format(directory))
        return result

    json_files = [directory + '/' + f for f in listdir(directory) if path.isfile(
          path.join(directory, f)) and f.split('.')[-1] == 'json']

    # filter files - files should be between start and end date
    for json_file in json_files:
        (file_start, file_end) = fetch_dates_from_filename(json_file)
        logging.info('Comparing {} - {}'.format(
            start_date,
            file_end
        ))
        if (start_date - file_end).total_seconds() < 0 and (end_date - file_start).total_seconds() >= 0:
            logging.info('[BASE] file start: {}, end: {}'.format(file_start, file_end))
            result.append(json_file)

    return result

def fetch_dates_from_filename(filename):

    dates = filename.split('/')[-1].split('.')[0].split('_')

    file_start = datetime.strptime(
        dates[0],
        Config.FILES_DATE_FORMAT
    )

    file_end = datetime.strptime(
        dates[1],
        Config.FILES_DATE_FORMAT
    )

    return (file_start, file_end)





