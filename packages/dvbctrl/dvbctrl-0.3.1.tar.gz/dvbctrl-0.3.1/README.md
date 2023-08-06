# dvbctrl

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
