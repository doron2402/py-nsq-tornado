# py-nsq-tornado-
Python app using Tornado and NSQ


# Run nsq instances
- `docker-compose up -d`

# how to run
- First make sure to run nsqd (daemon, admin, lookup) `docker-compose -d`
- You can test to check if nsqd is running by going to `http://localhost:4171`
- Activate python env `source env/bin/activate`
- export python path `export PYTHONPATH=$HOME/py-nsq-tornado/python:$PYTHONPATH`
- run the producer `PYTHONPATH=$HOME/py-nsq-tornado/python:$PYTHONPATH python sandbox/nsq_prucer.py`
- run the consumer/s `PYTHONPATH=$HOME/py-nsq-tornado/python:$PYTHONPATH python python/server/main.py`


# generate fake data
- `python sandbox/generate_fake_data.py` - this will generate fake data under `./data`