#!/usr/bin/python

import sys
import os
import random

from flask import Flask, send_file

if len(sys.argv) < 2:
	print('Usage: %s <root_dir>' % sys.argv[0])
	sys.exit(1)

app = Flask(__name__)

root_dir = sys.argv[1]
files = [os.path.join(os.getcwd(), root_dir, f) for f in os.listdir(root_dir)
		if ('.jpg' in f or '.png' in f)]
if len(files) == 0:
	print('Must be at least one image in dir')
	sys.exit(1)

print('%d files to select from' % len(files))
print(files)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def bgimage(path):
	f = random.choice(files)
	mimetype = 'image/png' if '.png' in f else 'image/jpeg'
	return send_file(f, mimetype=mimetype)

if __name__ == '__main__':
	app.run(port=64156)

