import sys

import pygments
from pygments import lexers
from pygments import styles

from blurformatter import BlurFormatter

if len(sys.argv) < 2:
	print 'Usage:', sys.argv[0], '<filename>'
	sys.exit(1)

text = ''
with open(sys.argv[1], 'r') as f:
	text = f.read()

lexer = lexers.get_lexer_for_filename(sys.argv[1])
style = styles.get_style_by_name('manni')
formatter = BlurFormatter(style=style)

print formatter.get_style_defs()
#print highlight(text, lexer, formatter)

