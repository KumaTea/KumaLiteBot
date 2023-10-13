#!/usr/bin/env bash

apt update -qq && apt install zip -y -qq

cd /tmp
mkdir python
pip install "python-telegram-bot<20" -t python -q
zip -r python.zip python
