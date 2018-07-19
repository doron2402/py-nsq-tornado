from faker import Faker
from json import dump
from datetime import datetime, timedelta
from random import random
from nsq_server.config import DATE_FORMAT, FILES_DATE_FORMAT

fake = Faker()

date = datetime(2018,1,1,0,0,0)

data_arr = []
start_date = date
while date < datetime(2018,1,10,0,0,0):
    date += timedelta(seconds=1)

    data = {
      'timestamp': date.strftime(DATE_FORMAT),
      'value_a': random(),
      'value_b': random()
    }
    data_arr.append(data)
    if date.hour % 6 == 0 and date.minute == 0  and date.second == 0:
        file_name = 'data/1/{}/0{}/{}_{}.json'.format(
            date.year,
            date.month,
            start_date.strftime(FILES_DATE_FORMAT),
            date.strftime(FILES_DATE_FORMAT)
        )
        with open(file_name, 'w') as outfile:
            dump(data_arr, outfile)
            start_date = date
