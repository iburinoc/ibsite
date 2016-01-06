import sys

import pygments
from pygments import lexers
from pygments import styles

from pygments.formatters import ImageFormatter, JpgImageFormatter

from PIL import ImageFilter

if len(sys.argv) < 2:
	print 'Usage:', sys.argv[0], '<filename>'
	sys.exit(1)

text = ''
with open(sys.argv[1], 'r') as f:
	text = f.read()

text = text + ' ' * 160 + '\n'

lexer = lexers.get_lexer_for_filename(sys.argv[1])
style = styles.get_style_by_name('manni')
opts = {
	"style": style,
	"line_numbers": False,
	"font_name": "Inconsolata",
	"font_size": 8,
}
formatter = ImageFormatter(**opts)

img = formatter.format(lexer.get_tokens(text), "out.png")

