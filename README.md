# python-bghive
Python interface to British Gas Hive API

- Start by creating a session

```
import bghive
session = bghive.Session(username, password)
```

- Get a node by name

```
bedroom_light = session.get_node("Bedroom")
```

- Get the attributes of the node:

```
bedroom_light.attributes
```

- Set an attribute on the node

```
bedroom_light.set_attribute("state", "OFF")
```
