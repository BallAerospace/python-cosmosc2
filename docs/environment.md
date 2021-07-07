> Copyright 2021 Ball Aerospace & Technologies Corp.
>
> All Rights Reserved.
>
> This program is free software; you can modify and/or redistribute it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation; version 3 with attribution addendums as found in the LICENSE.txt

## Environment Variables

### COSMOS_VERSION


If you are using cosmos v5 you MAY want to set the environment variable `COSMOSC2_VERSION` to equal anything. This will be used in the User-Agent header of the request. Tt will default to use the libary version. You can use this to track requests from an external application to cosmos.

```python
import os

try:
    os.environ["COSMOSC2_VERSION"]
except KeyError:
    os.environ["COSMOSC2_VERSION"] = "1.2.3"
```

In v1 the libary can log much more of what is happening in the libary. If you wish to enable this you can set the environment variable `COSMOS_DEBUG` to equal "DEBUG". If this is not set you will not get log messages if this is an incorrect log level you will get a ValueError.

```python
import os

try:
    os.environ["COSMOS_DEBUG"]
except KeyError:
    os.environ["COSMOS_DEBUG"] = "DEBUG"
```

### COSMOS_SCHEMA

In v1 you MAY want to set the hostname for Cosmos. The schema can now be set via an environment variable `COSMOS_SCHEMA` to the network schema that Cosmos is running with. Normal options are `http` or `https`. The default is `http`

```python
import os

try:
    os.environ["COSMOS_SCHEMA"]
except KeyError:
    os.environ["COSMOS_SCHEMA"] = "http"
```

### COSMOS_HOSTNAME

In v1 you MAY want to set the hostname for all Cosmos v4 scripts. In v0 of cosmosc2 it would default to 127.0.0.1. The hostname can now be set via an environment variable `COSMOS_HOSTNAME` to network address of the computer running Cosmos.

```python
import os

try:
    os.environ["COSMOS_HOSTNAME"]
except KeyError:
    os.environ["COSMOS_HOSTNAME"] = "127.0.0.1"
```

### COSMOS_PORT

In v1 you MAY want to set the port for all cosmos v5 scripts. The port can be set via an environment variable `COSMOS_PORT` to the network port of the computer running Cosmos. Note the new port for Cosmos v5 is 2900

```python
import os

try:
    os.environ["COSMOS_PORT"]
except KeyError:
    os.environ["COSMOS_PORT"] = "7777"
```

### COSMOS_TOKEN

In Cosmos v5 the api is password protected by default, so you need to make sure to set the password before you can use the api. If you need to use a different password you can set the environment variable `COSMOS_TOKEN` to the password on your Cosmos v5 instance. If this is not set the password will default to SuperSecret.

```python
import os

try:
    os.environ["COSMOS_TOKEN"]
except KeyError:
    os.environ["COSMOS_TOKEN"] = ""
```
