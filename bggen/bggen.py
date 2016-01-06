import sys
import os
import random

import pygments
from pygments import lexers, styles
from pygments.formatters import ImageFormatter

def main():
	if len(sys.argv) < 5:
		print 'python %s <in dir> <out dir> <num images> <lines>' % sys.argv[0]
		sys.exit(1)

	style = styles.get_style_by_name('manni')
	format_opts = {
		"style": style,
		"line_numbers": False,
		"font_name": "Inconsolata",
		"font_size": 8
	}

	in_dir = sys.argv[1]
	out_dir = sys.argv[2]
	num_images = int(sys.argv[3])
	num_lines = int(sys.argv[4])

	fnames = [os.path.join(os.getcwd(), in_dir, f)
		 for f in os.listdir(in_dir)]

	for i in range(num_images):
		inf = random.choice(fnames)
		outf = os.path.join(os.getcwd(), out_dir, str(i) + '.png')
		formatter = ImageFormatter(**format_opts)
		highlight_file(inf, outf, formatter, num_lines)
		print 'formatted %s into %s, %d/%d' % (inf, outf,
			i+1, num_images)

def highlight_file(inf, outf, formatter, n):
	lexer = lexers.get_lexer_for_filename(inf)

	lines = []
	with open(inf, 'r') as f:
		lines = f.readlines()
	n = min(n, len(lines))

	index = random.randrange(len(lines) - n + 1)
	flines = lines[index:index+n]
	text = ' ' * 160 + '\n' + ''.join(flines)

	formatter.format(lexer.get_tokens(text), outf)

if __name__ == '__main__':
	main()
