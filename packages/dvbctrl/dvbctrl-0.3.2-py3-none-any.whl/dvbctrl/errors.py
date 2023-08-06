import sys

from dvbctrl.colours import colours


def errorNotify(exci, e):
    lineno = exci.tb_lineno
    fname = exci.tb_frame.f_code.co_name
    ename = type(e).__name__
    msg = f"{colours.fg.red}{ename} Exception at line {lineno} in function {fname}: {e}{colours.reset}"
    # log.error(msg)
    print(msg)


def errorRaise(exci, e):
    errorNotify(exci, e)
    raise


def errorExit(exci, e):
    errorNotify(exci, e)
    sys.exit(1)


class DVBConnectionError(Exception):
    pass


class DVBStreamerError(Exception):
    def __init__(self, code, msg, lines=None):
        self.code = code
        self.msg = msg
        self.lines = lines

    def __str__(self):
        return f"{self.code}: {self.msg}"


class TooManyConnectionsError(DVBStreamerError):
    pass


class UnknownCommandError(DVBStreamerError):
    pass


class WrongArgumentsError(DVBStreamerError):
    pass


class NotAuthenticatedError(DVBStreamerError):
    pass


class GenericCommandError(DVBStreamerError):
    pass


def makeError(code, msg, lines=None):
    try:
        if code == 1:
            return TooManyConnectionsError(code, msg, lines)
        elif code == 2:
            return UnknownCommandError(code, msg, lines)
        elif code == 3:
            return WrongArgumentsError(code, msg, lines)
        elif code == 4:
            return NotAuthenticatedError(code, msg, lines)
        return GenericCommandError(code, msg, lines)
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)
