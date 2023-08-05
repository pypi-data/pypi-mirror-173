# encoding: utf-8

from PIL import ImageFont
from pathlib import Path

print(Path(__file__) / Path('fonts'))


class FontCache:

    def __init__(self,
                 font):
        self.sizes = {}
        self.font_path = self.find_font(font)  # TODO: try to find the font in common places

    @staticmethod
    def find_font(font):
        possible_paths = []
        for suffix in ('', '.ttf', '.otf'):
            possible_paths.append(Path(font).with_suffix(suffix))
            possible_paths.append(Path(__file__).parent / Path('fonts') / Path(font).with_suffix(suffix))
            possible_paths.append(Path().cwd() / Path(font).with_suffix(suffix))

        for path in possible_paths:
            if path.exists():
                return str(path.absolute())

        # Font has not been found in simpil, the current working directory
        return font

    def __getitem__(self,
                    size):
        try:
            return self.sizes[size]
        except KeyError:
            self.sizes[size] = ImageFont.truetype(font=self.font_path,
                                                  size=size)
        return self.sizes[size]


class FontsCache:
    def __init__(self):
        self.fonts = {}

    def __getitem__(self, font):
        try:
            the_font = self.fonts[font]
        except KeyError:
            self.fonts[font] = FontCache(font=font)
            the_font = self.fonts[font]
        return the_font


fonts = FontsCache()
