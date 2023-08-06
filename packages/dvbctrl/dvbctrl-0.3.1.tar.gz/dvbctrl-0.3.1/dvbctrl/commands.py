"""commands module for dvbstreamer control."""
import sys

from dvbctrl.connection import ControlConnection
from dvbctrl.errors import errorNotify


# commands:
#         quit - Exit the program. (NOT IMPLEMENTED)
#         help - Display the list of commands or help on a specific command. (NOT IMPLEMENTED)
#       select - Select a new service to stream.
#       setmrl - Set the MRL of the primary service filter.
#       getmrl - Get the primary service filter MRL.
#        addsf - Add a service filter.
#         rmsf - Remove a service filter.
#        lssfs - List all service filters.
#        setsf - Set the service to be filtered by a service filter.
#        getsf - Get the service to stream to a secondary service output.
#     setsfmrl - Set the service filter's MRL.
#     getsfmrl - Get the service filter's MRL.
# setsfavsonly - Enable/disable streaming of Audio/Video/Subtitles only.
# getsfavsonly - Get whether Audio/Video/Subtitles only streaming is enabled.
#   lsservices - List all services or for a specific multiplex.
#      lsmuxes - List multiplexes.
#       lspids - List the PIDs for a specified service.
#      current - Print out the service currently being streamed.
#  serviceinfo - Display information about a service.
#      muxinfo - Display information about a mux.
#        stats - Display the stats for the PAT,PMT and service PID filters.
#     festatus - Displays the status of the tuner.
#     feparams - Get current frontend parameters.
#      lsprops - List available properties.
#      getprop - Get the value of a property.
#      setprop - Set the value of a property.
#     propinfo - Display information about a property.
#      dumptsr - Dump information from the TSReader
#       lslnbs - List known LNBs
#         scan - Scan the specified multiplex(es) for services.
#   cancelscan - Cancel the any scan that is in progress.
#      epgdata - Register to receive EPG data in XML format.
#         date - Display the last date/time received.
#  enabledsmcc - Enable DSM-CC data download for the specified service filter.
# disabledsmcc - Disable DSM-CC data download for the specified service filter.
#    dsmccinfo - Display DSM-CC info for the specified service filter.
# epgcaprestart - Starts or restarts the capturing of EPG content.
#  epgcapstart - Starts the capturing of EPG content.
#   epgcapstop - Stops the capturing of EPG content.
#          now - Display the current program on the specified service.
#         next - Display the next program on the specified service.
#  addlistener - Add a destination to send event notification to.
#   rmlistener - Remove a destination to send event notification to.
#  lslisteners - List all registered event listener
# addlistenevent - Add an internal event to monitor.
# rmlistenevent - Remove an internal event to monitor
# lslistenevents - List all registered event listener
#        lslcn - List the logical channel numbers to services.
#      findlcn - Find the service for a logical channel number.
#    selectlcn - Select the service from a logical channel number.
#        addmf - Add a new destination for manually filtered PIDs.
#         rmmf - Remove a destination for manually filtered PIDs.
#        lsmfs - List current filters.
#     setmfmrl - Set the filter's MRL.
#     addmfpid - Adds a PID to a filter.
#      rmmfpid - Removes a PID from a filter.
#     lsmfpids - List PIDs for filter.
#    addoutput - Add a new output.
#     rmoutput - Remove an output.
#  enablesicap - Enable the capture of PSI/SI data.
# disablesicap - Disable the capture of PSI/SI data.
#    lsplugins - List loaded plugins.
#   plugininfo - Display the information about a plugin.
#          who - Display current control connections.
#         auth - Login to control dvbstreamer.
#       logout - Close the current control connection.


class DVBCommand(ControlConnection):
    """Class implementing control commands for a DVBStreamer daemon."""

    def __init__(self, adapter=0, host=None, user="dvbctrl", passw="dvbctrl"):
        try:
            super().__init__(adapter, host, user, passw)
            self.mux = None
            self.channel = None
        except Exception as e:
            errorNotify(sys.exc_info()[2], e)

    def setStatus():
        try:
            # TODO
            lines = self.festatus()
        except Exception as e:
            errorNotify(sys.exc_info()[2], e)

    def select(self, channel):
        """Tunes to the required channel on the <Primary> service filter"""
        try:
            lines = self.doCommand(f"select '{channel}'")
            self.channel = channel
            return lines
        except Exception as e:
            errorNotify(sys.exc_info()[2], e)

    def setsf(self, sfilter, channel):
        """Set the service to be filtered by a service filter."""
        try:
            lines = self.doCommand(f"setsf {sfilter} '{channel}'")
            return lines
        except Exception as e:
            errorNotify(sys.exc_info()[2], e)

    def getsf(self, sfilter):
        """Get the service to stream to a secondary service output."""
        try:
            lines = self.doCommand(f"getsf {sfilter}")
            return lines
        except Exception as e:
            errorNotify(sys.exc_info()[2], e)

    def setmrl(self, mrl):
        """set the output file for the primary service filter"""
        try:
            return self.doCommand(f"setmrl '{mrl}'")
        except Exception as e:
            errorNotify(sys.exc_info()[2], e)

    def getmrl(self):
        """return the output file for the primary service filter"""
        try:
            return self.doCommand("getmrl")
        except Exception as e:
            errorNotify(sys.exc_info()[2], e)

    def addsf(self, name):
        """add a service filter by name"""
        try:
            return self.doCommand(f"addsf '{name}' null://")
        except Exception as e:
            errorNotify(sys.exc_info()[2], e)

    def rmsf(self, name):
        """removes a service filter by name"""
        try:
            return self.doCommand(f"rmsf '{name}'")
        except Exception as e:
            errorNotify(sys.exc_info()[2], e)

    def lssfs(self):
        """list the current service filters"""
        try:
            return self.doCommand("lssfs")
        except Exception as e:
            errorNotify(sys.exc_info()[2], e)

    def setsfmrl(self, name, fn):
        """set the output file for the named service filter"""
        try:
            return self.doCommand(f"setsfmrl '{name}' '{fn}'")
        except Exception as e:
            errorNotify(sys.exc_info()[2], e)

    def getsfmrl(self, name):
        """get the output file for the named service filter"""
        try:
            return self.doCommand(f"getsfmrl '{name}'")
        except Exception as e:
            errorNotify(sys.exc_info()[2], e)

    def setsffavsonly(self, name, on=True):
        """Enable/disable streaming of Audio/Video/Subtitles only for the named service filter"""
        try:
            onoff = "on" if on else "off"
            return self.doCommand(f"setsffavsonly '{name}' {onoff}")
        except Exception as e:
            errorNotify(sys.exc_info()[2], e)

    def getsfavsonly(self):
        """Get whether Audio/Video/Subtitles only streaming is enabled"""
        try:
            return self.doCommand("getsffavsonly")
        except Exception as e:
            errorNotify(sys.exc_info()[2], e)

    def lsservices(self, mux=None):
        """List all services or for a specific multiplex"""
        try:
            cmd = "lsservices" if mux is None else f"lsservices {mux}"
            return self.doCommand(cmd)
        except Exception as e:
            errorNotify(sys.exc_info()[2], e)

    def lsmuxes(self):
        """List multiplexes"""
        try:
            return self.doCommand("lsmuxes")
        except Exception as e:
            errorNotify(sys.exc_info()[2], e)

    def lspids(self, channel):
        """returns the pids for a channel

        lines=[
        '4 PIDs for "5STAR"',
        '6673: { type: "ITU-T Rec. H.262 | ISO/IEC 13818-2 Video or ISO/IEC 11172-2 constrained parameter video stream" }',
        '6674: { type: "ISO/IEC 11172 Audio" }',
        '6675: { type: "ISO/IEC 11172 Audio" }',
        '6678: { type: "ITU-T Rec. H.222.0 | ISO/IEC 13818-1 PES packets containing private data" }'
        ]
        """
        try:
            return self.doCommand(f"lspids {channel}")
        except Exception as e:
            errorNotify(sys.exc_info()[2], e)

    def current(self):
        """Print out the service currently being streamed"""
        try:
            return self.doCommand("current")
        except Exception as e:
            errorNotify(sys.exc_info()[2], e)

    def serviceinfo(self, name):
        """Display information about a service"""
        try:
            return self.doCommand(f"serviceinfo '{name}'")
        except Exception as e:
            errorNotify(sys.exc_info()[2], e)

    def muxinfo(self, mux):
        """Display information about a mux"""
        try:
            return self.doCommand(f"muxinfo {mux}")
        except Exception as e:
            errorNotify(sys.exc_info()[2], e)

    def stats(self):
        """Display the stats for the PAT,PMT and service PID filters"""
        try:
            return self.doCommand("stats")
        except Exception as e:
            errorNotify(sys.exc_info()[2], e)

    def festatus(self):
        """Displays the status of the tuner"""
        try:
            return self.doCommand("festatus")
        except Exception as e:
            errorNotify(sys.exc_info()[2], e)

    def scan(self, mux=None):
        """Scan the specified multiplex(es) for services"""
        try:
            cmd = "scan all" if mux is None else f"scan {mux}"
            return self.doCommand(cmd)
        except Exception as e:
            errorNotify(sys.exc_info()[2], e)

    def cancelscan(self):
        """Cancel the any scan that is in progress"""
        try:
            return self.doCommand("cancelscan")
        except Exception as e:
            errorNotify(sys.exc_info()[2], e)

    def lslcn(self):
        """List the logical channel numbers to services."""
        try:
            chans = []
            lines = self.doCommand("lslcn")
            for line in lines:
                data = line.split(":")
                if len(data) == 2:
                    chans.append({data[0].strip(): data[1].strip()})
                else:
                    print(f"lslcn extraneous {line=}")
            return chans
        except Exception as e:
            errorNotify(sys.exc_info()[2], e)

    def findlcn(self, lcn):
        """Find the service for a logical channel number"""
        try:
            return self.doCommand(f"findlcn {lcn}")
        except Exception as e:
            errorNotify(sys.exc_info()[2], e)

    def selectlcn(self, lcn):
        """Select the service for the <Primary> filter from a logical channel number"""
        try:
            return self.doCommand(f"selectlcn {lcn}")
        except Exception as e:
            errorNotify(sys.exc_info()[2], e)

    def lsmfs(self):
        """List current filters"""
        try:
            cmd = "lsmfs"
            return self.doCommand(cmd)
        except Exception as e:
            errorNotify(sys.exc_info()[2], e)
