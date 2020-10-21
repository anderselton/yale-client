# Yale Client
Yale client is a python client for interacting with the Yale APIs.

This project is largely taken from https://github.com/domwillcode/yale-smart-alarm-client

The API has been split into alarm and lock, and the auth parts has been moved
away into a separate class to keep things noise free.

The codebase has also been updated be more python3 ish, dropping the ancient string formats etc.


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

### Usage
Create a client with:
```
client = YaleClient(username, password)
```
where username and password are your Yale Smart Alarm credentials.

#### Locks
Iterate the connected locks
```pyhon
client = YaleClient(username, password)
for lock in client.lock.locks():
    print(f"{lock}")
```

lock a single lock
```pyhon
lock = client.lock.get(name="myfrontdoor"):
lock.close()
```

unlock:
```pyhon
lock = client.lock.get(name="myfrontdoor"):
lock.open(pin_code="1234566")
```


#### Alarm
Change the alarm state with:
```
client.alarm.arm_full()
client.alarm.arm_partial()
client.alarm.disarm()
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
client.alarm.is_armed() # == True
```

or return alarm status. eg.
```
client.alarm.get_armed_status() is YALE_STATE_ARM_FULL
```

