#! /bin/sh

cmd=$1
shift
case $cmd in
    test) poetry run pytest tests;;
    *) $1 $cmd;;
esac