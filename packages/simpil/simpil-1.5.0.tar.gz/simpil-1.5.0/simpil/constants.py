# encoding: utf-8


from PIL import ImageFont
from .fonts import fonts

RGB = u'RGB'
JPEG = u'JPEG'
PNG = u'PNG'
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255,)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)

LEFT = "left"
TOP = "top"
CENTRE = u'centre'
CENTER = u'center'
BOTTOM = u'bottom'
RIGHT = u'right'

CONSOLAS = fonts['consola']

DEFAULT_FONT = CONSOLAS[18]
