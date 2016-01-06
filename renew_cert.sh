#!/bin/bash

cd /root/letsencrypt/
./letsencrypt-auto certonly --webroot -w /var/www/ibsite/ -d seanp.xyz --renew-by-default
service nginx reload
