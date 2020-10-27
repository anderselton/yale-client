# Yale Client
Yale client is a python client for interacting with the Yale APIs.

This project is largely taken from https://github.com/domwillcode/yale-smart-alarm-client

There exists a cli and programming interface to interact with the yale apis.

Supported functions:
- alarm api:
    - Arm full (away)
    - Arm partial (away/night)
    - Disarm
    - Get alarm status
- lock api
    - get status
    - lock
    - unlock

### Python version
Tested with the following python versions
* Python 3.7
* Python 3.6

## CLI
The cli can be used as a standalone python program.  Just instsall the client as you usually would
by doing a pip install:
```bash
pip install yaleclient
```
The cli optionally reads these variables from envrionment, so you do not have to 
specify them as arguments.
* YALE_USERNAME
* YALE_PASSWORD
* LOCK_PIN_CODE

### Usage
```bash
> export YALE_USERNAME=foo
> export YALE_PASSWORD=bar
> export LOCK_PIN_CODE=123456

> yaleclient --api=LOCK --operation=STATUS --lock_id=mydoor
mydoor [YaleLockState.LOCKED]

> yaleclient --api=LOCK --operation=STATUS
mydoor [YaleLockState.LOCKED]
mydoor2 [YaleLockState.LOCKED]

> yaleclient --api=LOCK --operation=OPEN
mydoor [YaleLockState.OPEN]
mydoor2 [YaleLockState.OPEN]

> yaleclient --api=LOCK --operation=CLOSE
mydoor [YaleLockState.LOCKED]
mydoor2 [YaleLockState.LOCKED]

> yaleclient --api=LOCK --help
> yaleclient --api=ALARM --help
```

## Programming api
### Usage
Create a client with:
```
from yaleclient import YaleClient
client = YaleClient(username="", password="")
```
where username and password are your Yale credentials.

#### Locks
Iterate the connected locks
```pyhon
for lock in client.lock_api.locks():
    print(lock)
```

lock a single lock
```pyhon
lock = client.lock_api.get(name="myfrontdoor"):
lock.close()
```

unlock:
```pyhon
lock = client.lock_api.get(name="myfrontdoor"):
lock.open(pin_code="1234566")
```


#### Alarm
Change the alarm state with:
```
client.alarm_api.arm_full()
client.alarm_api.arm_partial()
client.alarm_api.disarm()
```
or 
```
client.alarm.set_alarm_state(<mode>)
```
where 'mode' is one of:
```
from yaleclient.alarm import (YALE_STATE_ARM_PARTIAL,
                              YALE_STATE_DISARM,
                              YALE_STATE_ARM_FULL)
```

Is the alarm armed fully or partially:
```
client.alarm_api.is_armed() # == True
```

or return alarm status. eg.
```
client.alarm_api.get_armed_status() is YALE_STATE_ARM_FULL
```

