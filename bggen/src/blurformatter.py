"""
	Formats for PNG output with blur
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter

from pygments.formatters import ImageFormatter, JpgImageFormatter

class GaussianBlurRedux(ImageFilter.GaussianBlur):
	def __init__(self, radius=2):
		self.radius = radius

class BlurFormatter(JpgImageFormatter):
    def __init__(self, **options):
        radius = options.get('blur_radius', 2)
        self.im_filter = GaussianBlurRedux(radius=radius)
        ImageFormatter.__init__(self, **options)

    def format(self, tokensource, outfile):
        """
        Format ``tokensource``, an iterable of ``(tokentype, tokenstring)``
        tuples and write it into ``outfile``.

        This implementation calculates where it should draw each token on the
        pixmap, then calculates the required pixmap size and draws the items.
        """
        self._create_drawables(tokensource)
        self._draw_line_numbers()
        im = Image.new(
            'RGB',
            self._get_image_size(self.maxcharno, self.maxlineno),
            self.background_color
        )
        self._paint_line_number_bg(im)
        draw = ImageDraw.Draw(im)
        # Highlight
        if self.hl_lines:
            x = self.image_pad + self.line_number_width - self.line_number_pad + 1
            recth = self._get_line_height()
            rectw = im.size[0] - x
            for linenumber in self.hl_lines:
                y = self._get_line_y(linenumber - 1)
                draw.rectangle([(x, y), (x + rectw, y + recth)],
                               fill=self.hl_color)
        for pos, value, font, kw in self.drawables:
            draw.text(pos, value, font=font, **kw)
	img = im.filter(self.im_filter)
        img.save(outfile, self.image_format.upper())	

