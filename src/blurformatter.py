"""
	Formats for HTML output with blur
"""

from pygments.formatters import HtmlFormatter
from pygments.token import Token

NOSELECT = '-webkit-user-select: none;' + \
	'-webkit-touch-callout: none;' + \
	'-khtml-user-select: none;' + \
	'-moz-user-select: none;' + \
	' -ms-user-select: none;' + \
	'user-select: none;'
NOOVERFLOW = 'overflow: hidden; text-overflow: clip;'
MAKEBACKGROUND = 'position: relative; left: 10px; top: 10px;'

class BlurFormatter(HtmlFormatter):
	def _create_stylesheet(self):
		t2c = self.ttype2class = {Token: ''}
		c2s = self.class2style = {}
		for ttype, ndef in self.style:
			name = self._get_css_class(ttype)
			style = ''
			style += 'color: rgba(0,0,0,0); '
			if ndef['color']:
				style += 'text-shadow: 0px 0px 0.2em #%s; ' % ndef['color']
			else:
				style += 'text-shadow: 0px 0px 0.2em #000; '
			if ndef['bold']:
				style += 'font-weight: bold; '
			if ndef['italic']:
				style += 'font-style: italic; '
			if ndef['underline']:
				style += 'text-decoration: underline; '
			if ndef['bgcolor']:
				style += 'background-color: #%s; ' % ndef['bgcolor']
			if ndef['border']:
				style += 'border: 1px solid #%s; ' % ndef['border']
			if style:
				t2c[ttype] = name
				# save len(ttype) to enable ordering the styles by
				# hierarchy (necessary for CSS cascading rules!)
				c2s[name] = (style[:-2], ttype, len(ttype))

	def get_style_defs(self, arg=None):
		return '.highlight {' + \
			MAKEBACKGROUND + \
			NOSELECT + \
			NOOVERFLOW + \
			'}\n' + \
			HtmlFormatter.get_style_defs(self, arg)
