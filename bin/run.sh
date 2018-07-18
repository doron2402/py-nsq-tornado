
export PYTHONPATH=$HOME/py-nsq-tornado/python:$PYTHONPATH
export PYTHONPATH=$HOME/py-nsq-tornado/python/server:$PYTHONPATH

echo $PYTHONPATH

python python/server/main.py