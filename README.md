# py-nsq-tornado-
Python app using Tornado and NSQ


# Run nsq instances
- `docker-compose up -d`

# how to run
- Docker compose (NSQ)
  - First make sure to run nsqd (daemon, admin, lookup) `docker-compose -d`
  - You can test to check if nsqd is running by going to `http://localhost:4171`
- Python ENV
  - Activate python env `source env/bin/activate`
  - Or you can use `pyenv` - `pyenv versions` to print a list of versions
  - `pyenv activate nsq-tornado`
- export python path `export PYTHONPATH=$HOME/github/py-nsq-tornado/python:$PYTHONPATH`
- run the producer `PYTHONPATH=$HOME/github/py-nsq-tornado/python:$PYTHONPATH python sandbox/nsq_producer.py`
- run the consumer/s `PYTHONPATH=$HOME/github/py-nsq-tornado/python:$PYTHONPATH python python/nsq_server/main.py`


# generate fake data
- `python sandbox/generate_fake_data.py` - this will generate fake data under `./data`