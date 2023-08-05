import os
import re
from typing import Any, Union

import cv2
import numpy as np
import requests
from a_cv2_imshow_thread import imshow_thread


colormap = {
    # X11 colour table from https://drafts.csswg.org/css-color-4/, with
    # gray/grey spelling issues fixed.  This is a superset of HTML 4.0
    # colour names used in CSS 1.
    "aliceblue": "#f0f8ff",
    "antiquewhite": "#faebd7",
    "aqua": "#00ffff",
    "aquamarine": "#7fffd4",
    "azure": "#f0ffff",
    "beige": "#f5f5dc",
    "bisque": "#ffe4c4",
    "black": "#000000",
    "blanchedalmond": "#ffebcd",
    "blue": "#0000ff",
    "blueviolet": "#8a2be2",
    "brown": "#a52a2a",
    "burlywood": "#deb887",
    "cadetblue": "#5f9ea0",
    "chartreuse": "#7fff00",
    "chocolate": "#d2691e",
    "coral": "#ff7f50",
    "cornflowerblue": "#6495ed",
    "cornsilk": "#fff8dc",
    "crimson": "#dc143c",
    "cyan": "#00ffff",
    "darkblue": "#00008b",
    "darkcyan": "#008b8b",
    "darkgoldenrod": "#b8860b",
    "darkgray": "#a9a9a9",
    "darkgrey": "#a9a9a9",
    "darkgreen": "#006400",
    "darkkhaki": "#bdb76b",
    "darkmagenta": "#8b008b",
    "darkolivegreen": "#556b2f",
    "darkorange": "#ff8c00",
    "darkorchid": "#9932cc",
    "darkred": "#8b0000",
    "darksalmon": "#e9967a",
    "darkseagreen": "#8fbc8f",
    "darkslateblue": "#483d8b",
    "darkslategray": "#2f4f4f",
    "darkslategrey": "#2f4f4f",
    "darkturquoise": "#00ced1",
    "darkviolet": "#9400d3",
    "deeppink": "#ff1493",
    "deepskyblue": "#00bfff",
    "dimgray": "#696969",
    "dimgrey": "#696969",
    "dodgerblue": "#1e90ff",
    "firebrick": "#b22222",
    "floralwhite": "#fffaf0",
    "forestgreen": "#228b22",
    "fuchsia": "#ff00ff",
    "gainsboro": "#dcdcdc",
    "ghostwhite": "#f8f8ff",
    "gold": "#ffd700",
    "goldenrod": "#daa520",
    "gray": "#808080",
    "grey": "#808080",
    "green": "#008000",
    "greenyellow": "#adff2f",
    "honeydew": "#f0fff0",
    "hotpink": "#ff69b4",
    "indianred": "#cd5c5c",
    "indigo": "#4b0082",
    "ivory": "#fffff0",
    "khaki": "#f0e68c",
    "lavender": "#e6e6fa",
    "lavenderblush": "#fff0f5",
    "lawngreen": "#7cfc00",
    "lemonchiffon": "#fffacd",
    "lightblue": "#add8e6",
    "lightcoral": "#f08080",
    "lightcyan": "#e0ffff",
    "lightgoldenrodyellow": "#fafad2",
    "lightgreen": "#90ee90",
    "lightgray": "#d3d3d3",
    "lightgrey": "#d3d3d3",
    "lightpink": "#ffb6c1",
    "lightsalmon": "#ffa07a",
    "lightseagreen": "#20b2aa",
    "lightskyblue": "#87cefa",
    "lightslategray": "#778899",
    "lightslategrey": "#778899",
    "lightsteelblue": "#b0c4de",
    "lightyellow": "#ffffe0",
    "lime": "#00ff00",
    "limegreen": "#32cd32",
    "linen": "#faf0e6",
    "magenta": "#ff00ff",
    "maroon": "#800000",
    "mediumaquamarine": "#66cdaa",
    "mediumblue": "#0000cd",
    "mediumorchid": "#ba55d3",
    "mediumpurple": "#9370db",
    "mediumseagreen": "#3cb371",
    "mediumslateblue": "#7b68ee",
    "mediumspringgreen": "#00fa9a",
    "mediumturquoise": "#48d1cc",
    "mediumvioletred": "#c71585",
    "midnightblue": "#191970",
    "mintcream": "#f5fffa",
    "mistyrose": "#ffe4e1",
    "moccasin": "#ffe4b5",
    "navajowhite": "#ffdead",
    "navy": "#000080",
    "oldlace": "#fdf5e6",
    "olive": "#808000",
    "olivedrab": "#6b8e23",
    "orange": "#ffa500",
    "orangered": "#ff4500",
    "orchid": "#da70d6",
    "palegoldenrod": "#eee8aa",
    "palegreen": "#98fb98",
    "paleturquoise": "#afeeee",
    "palevioletred": "#db7093",
    "papayawhip": "#ffefd5",
    "peachpuff": "#ffdab9",
    "peru": "#cd853f",
    "pink": "#ffc0cb",
    "plum": "#dda0dd",
    "powderblue": "#b0e0e6",
    "purple": "#800080",
    "rebeccapurple": "#663399",
    "red": "#ff0000",
    "rosybrown": "#bc8f8f",
    "royalblue": "#4169e1",
    "saddlebrown": "#8b4513",
    "salmon": "#fa8072",
    "sandybrown": "#f4a460",
    "seagreen": "#2e8b57",
    "seashell": "#fff5ee",
    "sienna": "#a0522d",
    "silver": "#c0c0c0",
    "skyblue": "#87ceeb",
    "slateblue": "#6a5acd",
    "slategray": "#708090",
    "slategrey": "#708090",
    "snow": "#fffafa",
    "springgreen": "#00ff7f",
    "steelblue": "#4682b4",
    "tan": "#d2b48c",
    "teal": "#008080",
    "thistle": "#d8bfd8",
    "tomato": "#ff6347",
    "turquoise": "#40e0d0",
    "violet": "#ee82ee",
    "wheat": "#f5deb3",
    "white": "#ffffff",
    "whitesmoke": "#f5f5f5",
    "yellow": "#ffff00",
    "yellowgreen": "#9acd32",
}


def get_all_colors_in_range(start, end):
    start = color_converter(start)
    end = color_converter(end)
    allrgbvals = []
    for s, e in zip(start, end):
        allrgbvals.append(tuple(range(s, e + 1)))
    for r in allrgbvals[0]:
        for g in allrgbvals[1]:
            for b in allrgbvals[2]:
                yield r, g, b


def color_converter(color):
    # adapted from https://github.com/bunkahle/PILasOPENCV
    if isinstance(color, list):
        color = tuple(color)
    if isinstance(color, tuple):
        return color
    if color in colormap:
        color = colormap[color]

        # check for known string formats
    if re.match(r"^#?[a-f0-9]{3}$", color, flags=re.IGNORECASE):
        if "#" in color:
            return (
                int(color[1] * 2, 16),
                int(color[2] * 2, 16),
                int(color[3] * 2, 16),
            )
        return (
            int(color[0] * 2, 16),
            int(color[1] * 2, 16),
            int(color[2] * 2, 16),
        )

    if re.match(r"^#?[a-f0-9]{4}$", color, flags=re.IGNORECASE):
        if "#" in color:

            return (
                int(color[1] * 2, 16),
                int(color[2] * 2, 16),
                int(color[3] * 2, 16),
                int(color[4] * 2, 16),
            )
        return (
            int(color[0] * 2, 16),
            int(color[1] * 2, 16),
            int(color[2] * 2, 16),
            int(color[3] * 2, 16),
        )

    if re.match(r"^#?[a-f0-9]{6}$", color, flags=re.IGNORECASE):
        if "#" in color:

            return (
                int(color[1:3], 16),
                int(color[3:5], 16),
                int(color[5:7], 16),
            )
        return (
            int(color[0:2], 16),
            int(color[2:4], 16),
            int(color[4:6], 16),
        )

    if re.match(r"^#?[a-f0-9]{8}$", color, flags=re.IGNORECASE):
        if "#" in color:

            return (
                int(color[1:3], 16),
                int(color[3:5], 16),
                int(color[5:7], 16),
                int(color[7:9], 16),
            )
        return (
            int(color[0:2], 16),
            int(color[2:4], 16),
            int(color[4:6], 16),
            int(color[6:8], 16),
        )

    m = re.match(
        r"rgb\(\s*(?:\d+)\s*,\s*(?:\d+)\s*,\s*(?:\d+)\s*\)$", color, flags=re.IGNORECASE
    )
    if m:
        return (int(m.group(1)), int(m.group(2)), int(m.group(3)))

    m = re.match(
        r"rgb\(\s*(?:\d+)%\s*,\s*(?:\d+)%\s*,\s*(?:\d+)%\s*\)$",
        color,
        flags=re.IGNORECASE,
    )
    if m:
        return (
            int((int(m.group(1)) * 255) / 100.0 + 0.5),
            int((int(m.group(2)) * 255) / 100.0 + 0.5),
            int((int(m.group(3)) * 255) / 100.0 + 0.5),
        )

    m = re.match(
        r"hsl\(\s*(?:\d+\.?\d*)\s*,\s*(?:\d+\.?\d*)%\s*,\s*(?:\d+\.?\d*)%\s*\)$",
        color,
        flags=re.IGNORECASE,
    )
    if m:
        from colorsys import hls_to_rgb

        rgb = hls_to_rgb(
            float(m.group(1)) / 360.0,
            float(m.group(3)) / 100.0,
            float(m.group(2)) / 100.0,
        )
        return (
            int(rgb[0] * 255 + 0.5),
            int(rgb[1] * 255 + 0.5),
            int(rgb[2] * 255 + 0.5),
        )

    m = re.match(
        r"hs[bv]\(\s*(?:\d+\.?\d*)\s*,\s*(?:\d+\.?\d*)%\s*,\s*(?:\d+\.?\d*)%\s*\)$",
        color,
        flags=re.IGNORECASE,
    )
    if m:
        from colorsys import hsv_to_rgb

        rgb = hsv_to_rgb(
            float(m.group(1)) / 360.0,
            float(m.group(2)) / 100.0,
            float(m.group(3)) / 100.0,
        )
        return (
            int(rgb[0] * 255 + 0.5),
            int(rgb[1] * 255 + 0.5),
            int(rgb[2] * 255 + 0.5),
        )

    m = re.match(
        r"rgba\(\s*(?:\d+)\s*,\s*(?:\d+)\s*,\s*(?:\d+)\s*,\s*(?:\d+)\s*\)$",
        color,
        flags=re.IGNORECASE,
    )
    if m:
        return (int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)))
    raise ValueError("unknown color specifier: %r" % color)


def open_image_in_cv(image, channels_in_output=None):
    if isinstance(image, str):
        if os.path.exists(image):
            if os.path.isfile(image):
                image = cv2.imread(image)
        elif re.search(r"^.{1,10}://", str(image)) is not None:
            x = requests.get(image).content
            image = cv2.imdecode(np.frombuffer(x, np.uint8), cv2.IMREAD_COLOR)
        else:
            image = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)
    elif "PIL" in str(type(image)):
        image = np.array(image)
    else:
        if image.dtype != np.uint8:
            image = image.astype(np.uint8)

    if channels_in_output is not None:
        if image.shape[-1] == 4 and channels_in_output == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
        elif image.shape[-1] == 3 and channels_in_output == 4:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
        else:
            pass
    return image


class ColorCheck:
    def __init__(self, image: Any):
        """
        Parameters:
            image: Any
                url, file path, str base64 encoded, PIL, np.ndarray

        """
        self.img = open_image_in_cv(image, channels_in_output=3)
        self.image = self.img.copy()
        self.image_to_show = []
        self.color_dict = {}
        self.color_map = []

        self.start = (0, 0)
        self.end = (self.img.shape[1], self.img.shape[0])

    def crop_imageselection(self, start: tuple, end: tuple):
        """
        Limit search to a certain region of the picture

        pic = ColorCheck(r"https://www.python.org/static/opengraph-icon-200x200.png")

        pic.crop_imageselection((100, 100), (150, 150))

        each_color_detailed1, sum_1 = pic.get_coords_of_color_range(
            start=(255, 215, 60), end="#FFE262", highlightcolor=(255, 0, 255)
        )

        pic.reset_cropped_imageselection()

        x1, y1, xy1 = pic.get_coords_of_color(
            (255, 212, 59), zipxy=False, highlightcolor=(255, 0, 0)
        )

        pic.show_result()

        #result: https://github.com/hansalemaos/screenshots/raw/main/colorfind4.png

            Parameters:
                start: tuple
                    x,y coordinates
                end: tuple
                    x,y coordinates
            Returns:
                self

        """

        self.start = start
        self.end = end
        self.img = self.image[self.start[1] : self.end[1], self.start[0] : self.end[0]]
        self.color_dict = {}
        self.color_map = []
        return self

    def reset_cropped_imageselection(self):
        """
        Reset the cropped region

        """
        self.img = self.image.copy()
        self.start = (0, 0)
        self.end = (self.img.shape[1], self.img.shape[0])
        self.color_dict = {}
        self.color_map = []
        return self

    def get_coords_of_color(
        self,
        color: Union[str, tuple, list],
        zipxy: bool = True,
        highlightcolor: Union[None, tuple] = None,
    ) -> tuple:
        """
        Get all coordinates of a certain color in your picture
        pic = ColorCheck(r"https://www.python.org/static/opengraph-icon-200x200.png")
        x0, y0, xy0 = pic.get_coords_of_color((255, 212, 59))

        x0
        Out[4]:
        array([164, 162, 163, 164, 161, 162, 163, 159, 160, 161, 162, 163, 158,
               159, 160, 161, 162, 157, 158, 159, 160, 161, 162, 155, 156, 157,
               158, 159, 160, 161, 154, 155, 156, 157, 158, 159, 160, 161, 152,
               153, 154, 155, 156, 157, 158, 159, 160, 151, 152, 153, 154, 155,
               156, 157, 158, 159, 160, 149, 150, 151, 152, 153, 154, 155, 156,
               ....

        y0
        Out[7]:
        array([117, 118, 118, 118, 119, 119, 119, 120, 120, 120, 120, 120, 121,
               121, 121, 121, 121, 122, 122, 122, 122, 122, 122, 123, 123, 123,
               123, 123, 123, 123, 124, 124, 124, 124, 124, 124, 124, 124, 125,
               125, 125, 125, 125, 125, 125, 125, 125, 126, 126, 126
               ....

        xy0
        Out[9]: (if zipxy is True) / (None if zipxy is False)
        ((164, 117),
         (162, 118),
         (163, 118),
         (164, 118),
         (161, 119),
         (162, 119),
         (163, 119),
         (159, 120),
         (160, 120),
         (161, 120),
         (162, 120),
         (163, 120),
         ....

            Parameters:
                color:Union[str,tuple,list]
                    examples of valid inputs: (255, 212, 59), ffa7d7, #ffa9d9, black
                zipxy: bool
                    [50,100,200], [20,120,220] -> [(50,20), (100,120), (200,220)]
                    (default=True)
                highlightcolor:Union[None,tuple]=None
                    Only relevant if you want to see the output results with pic.show_result()
                    examples of valid inputs: (255, 212, 59), ffa7d7, #ffa9d9, black
                    (default=None)
            Returns:
                tuple
                (all x coordinates, all y coordinates, zipped x,y coordinates/None)
        """
        color = color_converter(color)
        if color in self.color_dict:
            mask = self.color_dict[color]
        else:
            mask = (
                (self.img[:, :, 0] == color[2])
                & (self.img[:, :, 1] == color[1])
                & (self.img[:, :, 2] == color[0])
            )
            self.color_dict[color] = mask
        xcoords, ycoords = np.where(mask)
        xcoords += self.start[1]
        ycoords += self.start[0]
        if highlightcolor is not None:
            highlightcolor = color_converter(highlightcolor)
            if not np.any(self.image_to_show):
                self.image_to_show = self.image.copy()
            self.image_to_show[xcoords, ycoords] = list(reversed(highlightcolor))
        allcoords = None
        if zipxy:
            allcoords = tuple(zip(*(xcoords, ycoords)[::-1]))
        return ycoords, xcoords, allcoords

    def get_coords_of_color_range(
        self,
        start: Union[str, tuple, list],
        end: Union[str, tuple, list],
        highlightcolor: Union[None, tuple] = None,
    ) -> tuple:
        """
        Get all coordinates of a certain color range in your picture
        pic = ColorCheck(r"https://www.python.org/static/opengraph-icon-200x200.png")

        each_color_detailed1,sum_1=pic.get_coords_of_color_range(start=(255,215,60),end=  '#FFE262',highlightcolor=(255,0,255))
        #result https://github.com/hansalemaos/screenshots/raw/main/colorfind2.png

        each_color_detailed1
        ....
          ((255, 210, 60), ()),
          ((255, 211, 55), ()),
          ((255, 211, 56), ()),
          ((255, 211, 57), ()),
          ((255, 211, 58), ()),
          ((255, 211, 59), ()),
          ((255, 211, 60), ()),
          ((255, 212, 55), ()),
          ((255, 212, 56), ()),
          ((255, 212, 57), ()),
          ((255, 212, 58), ()),
          ((255, 212, 59),
           ((164, 117),
            (162, 118),
            (163, 118),
            (164, 118),
            (161, 119),
            (162, 119),
            (163, 119),
            (159, 120),
            (160, 120),
            (161, 120),
            (162, 120),
            (163, 120),
        ....

        sum1
        ...
         (132, 125),
         (130, 126),
         (131, 126),
         (129, 127),
         (130, 127),
         (128, 128),
         (126, 129),
         (127, 129),
         (125, 130),
         (123, 131),
         (124, 131),
         (115, 137),
         (113, 138),
         (114, 138),
         (112, 139),
         (110, 140),
         (111, 140),
         ...

            Parameters:
                start:Union[str,tuple,list]
                    start of the color range
                    examples of valid inputs: (255, 212, 59), ffa7d7, #ffa9d9, black
                end:Union[str,tuple,list]
                    end of the color range
                    examples of valid inputs: (255, 212, 59), ffa7d7, #ffa9d9, black
                highlightcolor:Union[None,tuple]=None
                    Only relevant if you want to see the output results with pic.show_result()
                    examples of valid inputs: (255, 212, 59), ffa7d7, #ffa9d9, black
                    (default=None)
            Returns:
                tuple
                (all x coordinates, all y coordinates, zipped x,y coordinates/None)
                """

        allcors = get_all_colors_in_range(start, end)
        allco = []
        allco_ = []
        for cor in allcors:
            x, y, xy = self.get_coords_of_color(
                color=cor, highlightcolor=highlightcolor
            )
            allco.append((cor, xy))
            allco_.extend(list(xy))
        return allco, allco_

    def _create_color_map(self):
        if not np.any(self.color_map):
            self.color_map = np.zeros(256 * 256 * 256, dtype=np.int32)
            col = np.ravel(
                ((self.img[..., 0].astype("u4") * 256 + self.img[..., 1]) * 256)
                + self.img[..., 2]
            )
            col, idx = np.unique(np.sort(col), True)
            idx = np.hstack([idx, [self.img.shape[0] * self.img.shape[1]]])
            self.color_map[col] = idx[1:] - idx[:-1]
            self.color_map.shape = (256, 256, 256)

    def count_color(self, color: Union[str, tuple, list]) -> int:
        """
        Count how often a certain color is present
        pic = ColorCheck(r"https://www.python.org/static/opengraph-icon-200x200.png")

        pic.count_color((255, 212, 59))
        Out[12]: 477
            Parameters:
                color:Union[str,tuple,list]
                    examples of valid inputs: (255, 212, 59), ffa7d7, #ffa9d9, black

            Returns:
                int
        """
        color = color_converter(color)
        self._create_color_map()
        return self.color_map[color[2]][color[1]][color[0]]

    def count_color_range(
        self, start: Union[str, tuple, list], end: Union[str, tuple, list],
    ) -> tuple:
        """
        Count how often the colors of a certain color range are present
        pic = ColorCheck(r"https://www.python.org/static/opengraph-icon-200x200.png")
        each_color_detailed, sum_ = pic.count_color_range(start=(255, 215, 60), end="FFE262")

        sum_
        Out[5]: 2976

        each_color_detailed
        Out[6]:
        [((255, 215, 60), 0),
         ((255, 215, 61), 0),
         ((255, 215, 62), 0),
         ((255, 215, 63), 0),
         ((255, 215, 64), 0),
         ((255, 215, 65), 0),
         ((255, 215, 66), 48),
         ((255, 215, 67), 69),
         ((255, 215, 68), 87),
         ((255, 215, 69), 19),
         ...

            Parameters:
                start:Union[str,tuple,list]
                    start of the color range
                    examples of valid inputs: (255, 212, 59), ffa7d7, #ffa9d9, black
                end:Union[str,tuple,list]
                    end of the color range
                    examples of valid inputs: (255, 212, 59), ffa7d7, #ffa9d9, black

            Returns:
                tuple

        """
        allcors = get_all_colors_in_range(start, end)
        allco = []
        allco_ = []

        for cor in allcors:
            counting = self.count_color(color=cor)
            allco.append((cor, counting))
            allco_.append(counting)
        return allco, sum(allco_)

    def get_all_colors_in_image(self) -> tuple:
        """
        pic = ColorCheck(r"https://www.python.org/static/opengraph-icon-200x200.png")
        pic.get_all_colors_in_image()
        ((0, 0, 0),
         (77, 64, 18),
         (80, 66, 18),
         (83, 69, 20),
         (86, 72, 20),
         (87, 72, 20),
         (88, 73, 20),
         (77, 66, 21),
         (73, 63, 23),
         (81, 70, 26),
         (118, 98, 27),
         ...

        """
        self._create_color_map()
        allcolors = tuple(zip(*np.nonzero(self.color_map)[::-1]))
        return allcolors

    def count_all_colors(self) -> tuple:
        """
        pic.count_all_colors()
        Out[4]:
        [((0, 0, 0), 27515),
         ((77, 64, 18), 1),
         ((80, 66, 18), 1),
         ((83, 69, 20), 1),
         ((86, 72, 20), 1),
         ((87, 72, 20), 1),
         ((88, 73, 20), 1),
         ((77, 66, 21), 1),
         ...
        """
        allcors = self.get_all_colors_in_image()
        colorcount = [
            (color, self.color_map[color[2]][color[1]][color[0]]) for color in allcors
        ]
        return colorcount

    def reset_resultimg(self):
        self.image_to_show = self.image.copy()
        return self

    def show_result(
        self,
        window_name: str = "",
        quit_key: str = "q",
    ):
        """
        Show results
            Parameters:
                window_name: str
                    OpenCV window title
                    (default = "")
                quit_key: str
                    Key to close OpenCV window
                    (default = "q")
            Returns:
                self
        """
        if not np.any(self.image_to_show):
            self.image_to_show = self.image.copy()
        imshow_thread(
            image=self.image_to_show,
            window_name=window_name,
            sleep_time=None,
            quit_key=quit_key,
        )
        return self


# pic = ColorCheck(r"https://www.python.org/static/opengraph-icon-200x200.png")
# pic.get_all_colors_in_image()
# """
# ((0, 0, 0),
#  (77, 64, 18),
#  (80, 66, 18),
#  (83, 69, 20),
#  (86, 72, 20),
#  (87, 72, 20),
#  (88, 73, 20),
#  (77, 66, 21),
#  (73, 63, 23),
#  (81, 70, 26),
#  (118, 98, 27),
#  (69, 62, 29),
#  (72, 65, 29),
#  (81, 71, 30),
#  (129, 107, 30),
#  (130, 108, 30),
#  (76, 68, 31),
#  (77, 70, 32),
#  (72, 66, 33),
#  (80, 71, 33),
#  (143, 119, 33),
#  (85, 76, 34),
#  (108, 93, 34)
#  ...
# """
# pic.count_all_colors()
# """Out[4]:
# [((0, 0, 0), 27515),
#  ((77, 64, 18), 1),
#  ((80, 66, 18), 1),
#  ((83, 69, 20), 1),
#  ((86, 72, 20), 1),
#  ((87, 72, 20), 1),
#  ((88, 73, 20), 1),
#  ((77, 66, 21), 1),
#  ((73, 63, 23), 1),
#  ((81, 70, 26), 1),
#  ((118, 98, 27), 2),
#  ((69, 62, 29), 1),
#  ((72, 65, 29), 1),
#  ((81, 71, 30), 1),
#  ((129, 107, 30), 1),
#  ((130, 108, 30), 1),
#  ((76, 68, 31), 1),
#  ((77, 70, 32), 1),
#  ((72, 66, 33), 1),
#  ((80, 71, 33), 1),"""
#
# x0, y0, xy0 = pic.get_coords_of_color((255, 212, 59))
#
# # x1,y1,xy1=pic.get_coords_of_color((255, 212, 59),zipxy=False,highlightcolor=(255,0,0))
# """
# pic.get_coords_of_color((255, 212, 59),zipxy=False,highlightcolor=(255,0,0))
# """
#
# # each_color_detailed1,sum_1=pic.get_coords_of_color_range(start=(255,215,60),end=  '#FFE262',highlightcolor=(255,0,255))
#
# """
#   ((255, 210, 60), ()),
#   ((255, 211, 55), ()),
#   ((255, 211, 56), ()),
#   ((255, 211, 57), ()),
#   ((255, 211, 58), ()),
#   ((255, 211, 59), ()),
#   ((255, 211, 60), ()),
#   ((255, 212, 55), ()),
#   ((255, 212, 56), ()),
#   ((255, 212, 57), ()),
#   ((255, 212, 58), ()),
#   ((255, 212, 59),
#    ((164, 117),
#     (162, 118),
#     (163, 118),
#     (164, 118),
#     (161, 119),
#     (162, 119),
#     (163, 119),
#     (159, 120),
#     (160, 120),
#     (161, 120),
#     (162, 120),
#     (163, 120),
# """
# # pic.show_result()
# each_color_detailed, sum_ = pic.count_color_range(start=(255, 215, 60), end="FFE262")
# """
# sum_
# Out[5]: 2976
#
# each_color_detailed
# Out[6]:
# [((255, 215, 60), 0),
#  ((255, 215, 61), 0),
#  ((255, 215, 62), 0),
#  ((255, 215, 63), 0),
#  ((255, 215, 64), 0),
#  ((255, 215, 65), 0),
#  ((255, 215, 66), 48),
#  ((255, 215, 67), 69),
#  ((255, 215, 68), 87),
#  ((255, 215, 69), 19),
#
# """
#
# pic.crop_imageselection((100, 100), (150, 150))
#
# each_color_detailed1, sum_1 = pic.get_coords_of_color_range(
#     start=(255, 215, 60), end="#FFE262", highlightcolor=(255, 0, 255)
# )
#
# pic.reset_cropped_imageselection()
#
# x1, y1, xy1 = pic.get_coords_of_color(
#     (255, 212, 59), zipxy=False, highlightcolor=(255, 0, 0)
# )
#
# pic.show_result()
# # x,y,xy=pic.get_coords_of_color('ffa7d7',highlightcolor=(0,0,0))
# # indi,summ=pic.count_color_range(start='#ffa7d7',end='#ffa9d9')
# # indi1,summ1=pic.get_coords_of_color_range(start='#ffa7d7',end='#ffa9d9',highlightcolor=(0,0,0))
# # # pic.crop_image((330,150),(540,200))
# # indi1,summ1=pic.get_coords_of_color_range(start=(70,10,190),end=(80,20,200),highlightcolor=(255,0,0))
# # indi1,summ1=pic.get_coords_of_color_range(start='black',end=(10,10,10),highlightcolor=(0,255,255))
# # indi1,summ1=pic.get_coords_of_color_range(start='#fefefe',end='ffffff',highlightcolor=(255,255,0))
# #
# # pic.show_result()
# #
# # #(40, 7, 28)
# #
# # x,y,xy=pic.get_coords_of_color((40, 7, 28),highlightcolor=(200,0,0))
