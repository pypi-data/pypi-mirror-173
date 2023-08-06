# dvbctrl

Module to control a local [dvbstreamer](http://sourceforge.net/projects/dvbstreamer/).  On Arch you can install dvbstreamer from
the [AUR](https://aur.archlinux.org/packages/dvbstreamer).

## starting

```python
from dvbctrl.dvbstreamer import DVBStreamer

adapter = 0
dvbs = DVBStreamer(adapter)
running = dvbs.start()
if not running:
    raise Exception(f"Failed to start dvbstreamer on adapter {adapter}")
```

## stopping

```python
from dvbctrl.dvbstreamer import DVBStreamer

adapter = 0
dvbs = DVBStreamer(adapter)

...

if dvbs.isRunning():
    dvbs.stop()
```

## commands

```python
from dvbctrl.commands import DVBCommand

kwargs = {
    "adapter": 0,
    "host": "127.0.0.1"
    "pass": "dvbctrl"
    "user": "dvbctrl"
}
dvbc = DVBCommand(**kwargs)

# services (channels)
chans = dvbc.lsservices()
```

## dvbctrl commands

1.       select - Select a new service to stream.
1.       setmrl - Set the MRL of the primary service filter.
1.       getmrl - Get the primary service filter MRL.
1.        addsf - Add a service filter.
1.         rmsf - Remove a service filter.
1.        lssfs - List all service filters.
1.        setsf - Set the service to be filtered by a service filter.
1.        getsf - Get the service to stream to a secondary service output.
1.     setsfmrl - Set the service filter's MRL.
1.     getsfmrl - Get the service filter's MRL.
1. setsfavsonly - Enable/disable streaming of Audio/Video/Subtitles only.
1. getsfavsonly - Get whether Audio/Video/Subtitles only streaming is enabled.
1.   lsservices - List all services or for a specific multiplex.
1.      lsmuxes - List multiplexes.
1.       lspids - List the PIDs for a specified service.
1.  serviceinfo - Display information about a service.
1.      muxinfo - Display information about a mux.
1.        stats - Display the stats for the PAT,PMT and service PID filters.
1.     festatus - Displays the status of the tuner.
1.         scan - Scan the specified multiplex(es) for services.
1.   cancelscan - Cancel the any scan that is in progress.
1.        lslcn - List the logical channel numbers to services.
1.      findlcn - Find the service for a logical channel number.
1.    selectlcn - Select the service from a logical channel number.
1.      current - Print out the service currently being streamed. (NOT IMPLEMENTED)
1.     feparams - Get current frontend parameters. (NOT IMPLEMENTED)
1.      lsprops - List available properties. (NOT IMPLEMENTED)
1.      getprop - Get the value of a property. (NOT IMPLEMENTED)
1.      setprop - Set the value of a property. (NOT IMPLEMENTED)
1.     propinfo - Display information about a property. (NOT IMPLEMENTED)
1.      dumptsr - Dump information from the TSReader (NOT IMPLEMENTED)
1.       lslnbs - List known LNBs (NOT IMPLEMENTED)
1.      epgdata - Register to receive EPG data in XML format. (NOT IMPLEMENTED)
1.         date - Display the last date/time received. (NOT IMPLEMENTED)
1.  enabledsmcc - Enable DSM-CC data download for the specified service filter. (NOT IMPLEMENTED)
1. disabledsmcc - Disable DSM-CC data download for the specified service filter. (NOT IMPLEMENTED)
1.    dsmccinfo - Display DSM-CC info for the specified service filter. (NOT IMPLEMENTED)
1. epgcaprestart - Starts or restarts the capturing of EPG content. (NOT IMPLEMENTED)
1.  epgcapstart - Starts the capturing of EPG content. (NOT IMPLEMENTED)
1.   epgcapstop - Stops the capturing of EPG content. (NOT IMPLEMENTED)
1.          now - Display the current program on the specified service. (NOT IMPLEMENTED)
1.         next - Display the next program on the specified service. (NOT IMPLEMENTED)
1.  addlistener - Add a destination to send event notification to. (NOT IMPLEMENTED)
1.   rmlistener - Remove a destination to send event notification to. (NOT IMPLEMENTED)
1.  lslisteners - List all registered event listener (NOT IMPLEMENTED)
1. addlistenevent - Add an internal event to monitor. (NOT IMPLEMENTED)
1. rmlistenevent - Remove an internal event to monitor (NOT IMPLEMENTED)
1. lslistenevents - List all registered event listener (NOT IMPLEMENTED)
1.        addmf - Add a new destination for manually filtered PIDs. (NOT IMPLEMENTED)
1.         rmmf - Remove a destination for manually filtered PIDs. (NOT IMPLEMENTED)
1.        lsmfs - List current filters.
1.     setmfmrl - Set the filter's MRL. (NOT IMPLEMENTED)
1.     addmfpid - Adds a PID to a filter. (NOT IMPLEMENTED)
1.      rmmfpid - Removes a PID from a filter. (NOT IMPLEMENTED)
1.     lsmfpids - List PIDs for filter. (NOT IMPLEMENTED)
1.    addoutput - Add a new output. (NOT IMPLEMENTED)
1.     rmoutput - Remove an output. (NOT IMPLEMENTED)
1.  enablesicap - Enable the capture of PSI/SI data. (NOT IMPLEMENTED)
1. disablesicap - Disable the capture of PSI/SI data. (NOT IMPLEMENTED)
1.    lsplugins - List loaded plugins. (NOT IMPLEMENTED)
1.   plugininfo - Display the information about a plugin. (NOT IMPLEMENTED)
1.          who - Display current control connections. (NOT IMPLEMENTED)
1.         auth - Login to control dvbstreamer. (NOT IMPLEMENTED)
1.       logout - Close the current control connection. (NOT IMPLEMENTED)
1.         quit - Exit the program. (NOT IMPLEMENTED)
1.         help - Display the list of commands or help on a specific command. (NOT IMPLEMENTED)
