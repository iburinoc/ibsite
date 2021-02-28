#!/bin/bash

set -euxo pipefail

trap exit TERM

[ -d ibsite/ ] || git clone https://github.com/iburinoc/ibsite

bundle exec jekyll build -s ibsite/jekyll -d /www

python3 bgserver.py ibsite/bg/images/ &

nginx -t

nginx

while true
do
    sleep 1h &
    git --git-dir ibsite/.git pull && \
        bundle exec jekyll build -s ibsite/jekyll -d /www && \
        wait $!
done
