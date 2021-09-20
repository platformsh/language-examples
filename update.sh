#!/usr/bin/env bash

HOME=$(pwd)

echo "- Updating Go"
cd $HOME/golang && go mod tidy && go get -u

echo "- Updating Java"
cd $HOME/java && mvn clean install -U

echo "- Updating Node.js"
cd $HOME/nodejs && npm update

echo "- Updating PHP"
cd $HOME/php && composer update --ignore-platform-reqs

echo "- Updating Python"
cd $HOME/python && pipenv --three update
