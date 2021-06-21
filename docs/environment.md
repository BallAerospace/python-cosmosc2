> Copyright 2021 Ball Aerospace & Technologies Corp.
>
> All Rights Reserved.
>
> This program is free software; you can modify and/or redistribute it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation; version 3 with attribution addendums as found in the LICENSE.txt

## Environment Variables

### COSMOS_VERSION


Updated from v0 to v1 for the cosmosc2 libaray. If you are using cosmos v5 you DO NOT need to set the environment variable `COSMOSC2_VERSION` to equal anything it will default to use the libary version. You can use this to track requests from an external application to cosmos.

```python
import os

try:
    os.environ["COSMOSC2_VERSION"]
except KeyError:
    os.environ["COSMOSC2_VERSION"] = "1.2.3"
```

Updated from v0 to v1 for the cosmosc2 libaray. In v1 the libary can log much more of what is happening in the libary. If you wish to enable this you can set the environment variable `COSMOS_DEBUG` to equal "DEBUG". If this is not set you will not get log messages if this is an incorrect log level you will get a ValueError.

```python
import os

try:
    os.environ["COSMOS_DEBUG"]
except KeyError:
    os.environ["COSMOS_DEBUG"] = ""
```

### COSMOS_HOSTNAME

Updated from v0 to v1 for the cosmosc2 libaray. In v1 you CAN set the hostname for all Cosmos v4 scripts. In v0 of cosmosc2 it would default to 127.0.0.1. The hostname can now be set via an environment variable `COSMOS_HOSTNAME` to network address of the computer running Cosmos.

```python
import os

try:
    os.environ["COSMOS_HOSTNAME"]
except KeyError:
    os.environ["COSMOS_HOSTNAME"] = "127.0.0.1"
```

### COSMOS_PORT

Updated from v0 to v1 for the cosmosc2 libaray. In v1 you MUST set the port for all cosmos v4 scripts. In v0 of cosmosc2 the port was hard coded and would default to 7777 for Cosmos v4. In v1 the port can be set via an environment variable  `COSMOS_PORT` to the network port of the computer running Cosmos. Note the new port for Cosmos v5 is 2900

```python
import os

try:
    os.environ["COSMOS_PORT"]
except KeyError:
    os.environ["COSMOS_PORT"] = "7777"
```

### COSMOS_DEBUG

Updated from v0 to v1 for the cosmosc2 libaray. In v1 the libary can log much more of what is happening in the libary. If you wish to enable this you MUST set the environment variable `COSMOS_DEBUG` to equal "DEBUG". If this is not set you will not get log messages if this is an incorrect log level you will get a ValueError.

```python
import os

try:
    os.environ["COSMOS_DEBUG"]
except KeyError:
    os.environ["COSMOS_DEBUG"] = ""
```
