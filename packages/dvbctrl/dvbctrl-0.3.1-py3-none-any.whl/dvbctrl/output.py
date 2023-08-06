import sys

from dvbctrl.colours import colours
from dvbctrl.errors import errorNotify


def progressBar(progress, total, showValues=False, remove=False):
    try:
        percent = 100 * (progress / float(total))
        fill = chr(9609)  # left 3/4 filled block
        blank = chr(9617)  # light shaded character
        bar = (
            colours.fg.green
            + fill * int(percent)
            + colours.fg.darkgray
            + blank * (100 - int(percent))
        )
        if showValues:
            msg = f"\r|{bar}| {progress} / {total}"
        else:
            msg = f"\r|{bar}| {percent:.2f}"
        print(msg, end="\r")
        if remove:
            splat = " " * len(msg)
            print(f"{colours.reset}{splat}")
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)
