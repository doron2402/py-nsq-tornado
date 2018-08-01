
export PYTHONPATH=$HOME/py-nsq-tornado/python:$PYTHONPATH
export PYTHONPATH=$HOME/py-nsq-tornado/python/nsq_server:$PYTHONPATH

echo $PYTHONPATH

python python/nsq_server/main.py