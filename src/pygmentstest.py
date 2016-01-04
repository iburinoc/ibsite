import sys

import pygments
from pygments import lexers
from pygments import styles

from blurformatter import BlurFormatter
from pygments.formatters import ImageFormatter, JpgImageFormatter

from PIL import ImageFilter

if len(sys.argv) < 2:
	print 'Usage:', sys.argv[0], '<filename>'
	sys.exit(1)

text = ''
with open(sys.argv[1], 'r') as f:
	text = f.read()

lexer = lexers.get_lexer_for_filename(sys.argv[1])
style = styles.get_style_by_name('manni')
opts = {
	"style": style,
	"line_numbers": False,
	"font_name": "Inconsolata",
	"blur_radius": 3,
	"font_size": 8,
}
formatter = BlurFormatter(**opts)

#print formatter.get_style_defs()
img = formatter.format(lexer.get_tokens(text), "out.jpg")

