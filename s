#! /bin/sh

cmd=$1
shift
case $cmd in
    test) poetry run pytest tests;;
    exec) poetry run python $@;;
    example) ./s exec example.py;;
    *) $1 $cmd;;
esac