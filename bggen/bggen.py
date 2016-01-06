import sys
import os
import random

import pygments
from pygments import lexers, styles
from pygments.formatters import ImageFormatter
from PIL import ImageFilter

def main():
	if len(sys.argv) < 4:
		print 'python %s <in dir> <out dir> <lines>' % sys.argv[0]
		sys.exit(1)

	style = styles.get_style_by_name('manni')
	format_opts = {
		"style": style,
		"line_numbers": False,
		"font_name": "Inconsolata",
		"font_size": 8
	}
	formatter = ImageFormatter(**format_opts)

	in_dir = sys.argv[1]
	out_dir = sys.argv[2]
	lines = sys.argv[3]

	fnames = [
		(os.path.join(os.getcwd(), in_dir, f),
		 os.path.join(os.getcwd(), out_dir, f + '.png'))
		 for f in os.listdir(in_dir)]

	for ((inf, outf), i) in zip(fnames, range(len(fnames))):
		highlight_file(inf, outf, formatter, lines)
		print 'formatted %s into %s, %d/%d' % (inf, outf,
			i+1, len(fnames))

def test_min(a, b):
	return a if a < b else b

def highlight_file(inf, outf, formatter, n):
	lexer = lexers.get_lexer_for_filename(inf)

	lines = []
	with open(inf, 'r') as f:
		lines = f.readlines()
	l = len(lines)
	print(type(len(lines)))
	print n, len(lines), l, test_min(n, l), min(n, l)
	n = test_min(n, len(lines))

	index = random.randrange(len(lines) - n + 1)
	flines = lines[index:index+n]
	print n, index
	text = ' ' * 160 + '\n' + ''.join(flines)

	formatter.format(lexer.get_tokens(text), outf)

if __name__ == '__main__':
	main()
