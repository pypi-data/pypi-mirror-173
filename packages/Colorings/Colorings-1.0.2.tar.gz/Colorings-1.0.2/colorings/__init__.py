import re


class argumentError(Exception):
    pass

class colorings:
    """
    CONTAINS STATICS METHODS TO COLORS TEXT AND KNOWN COLORS CONSTANTS
    """
    hex_letter = list("ABCDEF")
    correspondance = {"A": 10, "B": 11, "C": 12, "D": 13, "E": 14, "F": 15}

    # Basic colors
    RED = "\033[38;2;255;0;0m"
    GREEN = "\033[38;2;0;255;0m"
    BLUE = "\033[38;2;0;0;255m"
    SILVER = "\033[38;2;192;192;192m"
    GRAY = "\033[38;2;128;128;128m"
    WHITE = "\033[38;2;255;255;255m"

    RESET = "\u001b[0m"
    BOLD = "\u001b[1m"
    UNDERLINE = "\u001b[4m"
    REVERSE = "\u001b[7m"

    # violets
    MAGENTA = "\033[38;2;255;0;255m"
    LAVENDER = "\033[38;2;230;230;250m"
    THISTLE = "\033[38;2;216;191;216m"
    PLUM = "\033[38;2;221;160;221m"
    VIOLET = "\033[38;2;238;130;238m"
    ORCHID = "\033[38;2;218;112;214m"
    MEDIUMORCHID = "\033[38;2;186;85;211m"
    MEDIUMPURPLE = "\033[38;2;147;112;219m"
    BLUEVIOLET = "\033[38;2;138;43;226m"

    # blue
    AQUA = "\033[38;2;0;255;255m"
    NAVY = "\033[38;2;0;0;128m"
    TEAL = "\033[38;2;0;128;128m"

    # green
    OLIVE = "\033[38;2;128;128;0m"
    LIME = "\033[38;2;0;255;0m"

    # yellow
    YELLOW = "\033[38;2;255;255;0m"

    # Pink
    PINK = "\033[38;2;255;192;203m"

    # other colors :
    CHOCOLATE = "\033[38;2;210;105;30m"

    @staticmethod
    def __hexrgb__(hexadecimal: str) -> list:
        """
        :param hexadecimal: Must be something like "12EFC3"
        :return: the rgb code of the hexadecimal color such as (255,255,255) which is white
        """
        if len(hexadecimal) < 6 or len(hexadecimal) > 6:
            raise argumentError("INVALID HEX CODE")

        d = list(hexadecimal)
        c = [d[0] + d[1], d[2] + d[3], d[4] + d[5]]
        rgb = []
        for val in c:
            val = [v for v in val]
            for i, letter in enumerate(val):
                if letter in colorings.hex_letter:
                    val[i] = colorings.correspondance[letter]

            rgb.append(int(val[0]) * (16 ** 1) + int(val[1]) * (16 ** 0))

        return rgb

    @staticmethod
    def __rgbhex__(rgb: tuple or list):
        if len(rgb) < 3:
            raise argumentError("INVALID RGB CODE")
        elif len(rgb) > 3:
            raise argumentError("INVALID RGB CODE")
        d = []
        for digit in rgb:
            test = hex(digit).split('x')[-1]
            d.append(test.upper())
        return d

    @staticmethod
    def color(text: str, codesep="&", rgb=False) -> str:
        """
        :param text: must be str object and should contain color code such as : "&12EFC3&Hello &d& How you're doing ?"
        :param codesep: the ASCII character that is used to indicate where color code ares.
        :param rgb: If you wish to use rgb code instead of hexadecimal just turn it On (ex : "&10,10,10&Hello")
        :return: return the text with color !! (ex : "\033[38;2;{10};{10};{10]}mHellow")
        """
        if type(text) != str or type(codesep) != str or type(rgb) != bool:
            raise argumentError("INVALID TEXT")

        custom_remplacement = {"d": "\u001b[0m", "b": "\u001b[1m", "u": "\u001b[4m",
                               "r": "\u001b[7m"}
        if not rgb:
            c = re.findall("&[A-Za-z0-9]+&", text)
        else:
            c = re.findall("&[A-Za-z0-9-,]+&", text)
        restart = False
        for val in c:
            for key in custom_remplacement.keys():
                if val == codesep + key + codesep:
                    text = text.replace(codesep + key + codesep, custom_remplacement[key])
                    restart = True
            if restart:
                restart = False
                continue
            val = val.replace(codesep, "")
            if not rgb:

                color = colorings.__hexrgb__(val)
                try:
                    text = text.replace(codesep + val + codesep,
                                        f"\033[38;2;{color[0]};{color[1]};{color[2]}m")
                except IndexError:
                    raise argumentError("INVALID RGB/HEX CODE")
            else:
                color = val.split(",")
                try:
                    text = text.replace(codesep + val + codesep,
                                        f"\033[38;2;{color[0]};{color[1]};{color[2]}m")
                except IndexError:
                    raise argumentError("INVALID RGB/HEX CODE")
        return text

    @staticmethod
    def hex(hexadecimal: str):
        if type(hexadecimal) != str:
            raise argumentError("INVALID HEXCODE")
        color = colorings.__hexrgb__(hexadecimal)
        return f"\033[38;2;{color[0]};{color[1]};{color[2]}m"

    @staticmethod
    def rgb(rgb: tuple or list):
        if len(rgb) < 3 or len(rgb) > 3:
            raise argumentError("INVALID RGB CODE")
        return f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m"

    @staticmethod
    def __allcolor__():
        for i in range(256):
            print(f"\u001b[38;5;{i}m{i}", end=" ")

        for i in range(256):
            print(f"\u001b[48;5;{i}m{i}", end="" + "\u001b[0m ")

        print("\u001b[1mBOLD" + "\u001b[7mREVERSE" + "\u001b[0m " "\u001b[4mUNDERLINE")

    @staticmethod
    def cursmove(n, up=False, down=False, left=False, right=False):
        """Move cursor n times, may not work on every IDE"""
        if up and down or right and left or right and up or left and up or left and down or right and down:
            raise argumentError("\u001b[38;5;3mOnly one direction allowed\u001b[0m")
        if up:
            return f"\u001b[{n}A"
        if down:
            return f"\u001b[{n}B"
        if right:
            return f"\u001b[{n}C"
        if left:
            return f"\u001b[{n}D"