import os
import socket
import sys
import time

from dvbctrl.errors import (
    errorNotify,
    errorRaise,
    errorExit,
    DVBConnectionError,
    makeError,
)


class ControlConnection:
    """Class implementing a connection to a DVBStreamer daemon."""

    def __init__(self, adapter, host=None, user="dvbctrl", passw="dvbctrl"):
        """Create a connection object to talk to a DVBStreamer daemon."""
        try:
            if host is None:
                host = os.uname().nodename
            host = "127.0.0.1"
            self.host = host
            self.adapter = adapter
            self.opened = False
            self.authenticated = False
            self.welcomemsg = None
            self.myip = None
            self.username = user
            self.password = passw
            self.lastsuccess = 0
        except Exception as e:
            errorNotify(sys.exc_info()[2], e)

    def expired(self):
        try:
            now = time.time()
            return now > (self.lastsuccess + 5)
        except Exception as e:
            errorNotify(sys.exc_info()[2], e)

    def open(self):
        """Open the connection to the DVBStreamer daemon."""
        try:
            if self.opened:
                return self.opened
            self.sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # print(f"{self.host=}")
            self.sckt.connect((self.host, self.adapter + 54197))
            self.authenticated = False
            self.myip = self.sckt.getsockname()[0]
            self.scktfile = self.sckt.makefile(mode="rw")
            self.opened = True
            errorcode, errormessage, lines = self.readResponse()
            if errorcode != 0:
                self.sckt.close()
                self.opened = False
                print(
                    f"error opening connection:\n{errorcode=}\n{errormessage=}\n{lines=}"
                )
            else:
                self.welcomemsg = errormessage
            return self.opened
        except Exception as e:
            errorNotify(sys.exc_info()[2], e)

    def close(self):
        """Close the connection to the DVBStreamer daemon."""
        try:
            if self.opened:
                self.sendCommand("logout")
        except Exception as e:
            errorNotify(sys.exc_info()[2], e)
        finally:
            if self.opened:
                self.scktfile.close()
                self.sckt.close()
                self.opened = False

    def sendCommand(self, command):
        """
        Send a command to the DVBStreamer daemon connection.
        @param command: Command to send to the server.
        """
        try:
            if not self.opened:
                raise DVBConnectionError("not connected")
            self.scktfile.write(f"{command}\n")
            self.scktfile.flush()
            self.lastsuccess = time.time()
        except Exception as e:
            errorNotify(sys.exc_info()[2], e)

    def readResponse(self):
        """
        Read a response from the DVBStreamer deamon after a command has been sent.
        Returns a tuple of error code, error message and response lines.
        """
        try:
            morelines = True
            lines = []
            errorcode = -1
            errormessage = ""
            while morelines:
                line = self.scktfile.readline()
                if line.startswith("DVBStreamer/"):
                    morelines = False
                    sections = line.split("/")
                    self.version = sections[1]
                    errorsections = sections[2].split(" ", 1)
                    errorcode = int(errorsections[0])
                    if len(errorsections) > 1:
                        errormessage = errorsections[1].strip()
                    else:
                        errormessage = ""
                elif line == "":
                    morelines = False
                else:
                    lines.append(line.strip("\n\r"))
            self.lastsuccess = time.time()
            return (errorcode, errormessage, lines)
        except Exception as e:
            errorNotify(sys.exc_info()[2], e)

    def executeCommand(self, command):
        """
        Send command and wait for response
        Returns a tuple of error message and response lines if the return error code was 0,
        otherwise a DVBStreamerError is raised.
        """
        try:
            self.sendCommand(command)
            errorcode, errormessage, lines = self.readResponse()
            if errorcode != 0:
                raise makeError(errorcode, errormessage, lines)
            return (errormessage, lines)
        except Exception as e:
            errorNotify(sys.exc_info()[2], e)

    def authenticate(self, username=None, password=None):
        """
        Authenticate the connection allowing it to execute more commands.
        """
        try:
            if username is None:
                username = self.username
            if password is None:
                password = self.password
            errormessage, lines = self.executeCommand(f'auth "{username}" "{password}"')
            self.authenticated = True
        except Exception as e:
            errorNotify(sys.exc_info()[2], e)

    def doCommand(self, cmd):
        """
        Open (if not opened)
        Auth (if not authenticated)
        run 'cmd' command
        """
        try:
            if not self.opened:
                opened = self.open()
                if not opened:
                    raise Exception(
                        f"failed to open connection to adapter {self.adapter}"
                    )
            if not self.authenticated:
                self.authenticate()
            errmsg, lines = self.executeCommand(cmd)
            if errmsg != "OK":
                msg = f"possible error with command {cmd}: {errmsg=}"
                lines.append(msg)
            return lines
        except Exception as e:
            errorNotify(sys.exc_info()[2], e)
