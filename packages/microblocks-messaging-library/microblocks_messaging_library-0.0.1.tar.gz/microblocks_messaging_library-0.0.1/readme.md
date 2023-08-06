# readme

MicroBlocks and Python Communication with Messages.

# Install

```bash
# Python3
python -m pip install microblocks_messaging_library
```

# Usage

```python
import time
from microblocks_messaging_library import MicroblocksMessage

m = MicroblocksMessage()
m.connect('/dev/tty.usbmodem1402') # replace the string with micro:bit port

# broadcast message from Python to MicroBlocks
m.sendBroadcast('happy')
time.sleep(1)
m.sendBroadcast('sad')

# receive broadcasts from MicroBlocks
while True:
    message = m.receiveBroadcasts()
    print(message)
```
