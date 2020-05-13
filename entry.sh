#!/bin/bash

set -euxo pipefail

trap exit TERM

cp ibsite_nginx.conf /conf/
git clone https://github.com/iburinoc/ibsite
mkdir -p /www/ibsite
bundle exec jekyll build -s ibsite/jekyll -d /www/ibsite

python3 bgserver.py ibsite/bg/images/ &

while true
do
    sleep 1h &
    git --git-dir ibsite/.git pull && \
        bundle exec jekyll build -s ibsite/jekyll -d /www/ibsite && \
        wait $!
done
