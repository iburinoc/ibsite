#!/bin/bash

set -euxo pipefail

cp ibsite_nginx.conf /conf/
git clone https://github.com/iburinoc/ibsite
mkdir /www/ibsite
bundle exec jekyll build -s ibsite/jekyll -d /www/ibsite

python3 bgserver.py ibsite/bg/images/ &

while true
do
    sleep 3600
    git clone https://github.com/iburinoc/ibsite
    bundle exec jekyll build -s ibsite/jekyll -d /www/ibsite
done
