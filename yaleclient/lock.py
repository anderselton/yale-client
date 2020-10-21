# -*- coding: utf-8 -*-
from enum import Enum


class YaleLockState(Enum):
    LOCKED = 1
    UNLOCKED = 2
    DOOR_OPEN = 3
    UNKNOWN = 4


class YaleLock:
    DEVICE_TYPE = "device_type.door_lock"
    """ 
    This is an abstraction of a remove Yale lock.
    The object created by this class attempts to reflect the remote state, and also has the possibilty of 
    locking/unlocking the lock state.
    
    Objects of this class shall usually be craeted by the lock_api class.
    """

    def __init__(self, device: dict, lock_api):
        self._lock_api = lock_api
        self._device: dict = device
        self.name: str = device['name']
        self._state: YaleLockState = YaleLockState.UNKNOWN
        self.update(device)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.name == other.name
        elif isinstance(other, str):
            return self.name == other
        else:
            return False

    def __str__(self):
        return f"{self.name} [{self.state()}]"

    def update(self, device: dict):
        self._device = device
        self.name = device['name']
        self._state = self._calc_state()

    def state(self):
        return self._state

    def area(self):
        return self._device['area']

    def sid(self):
        return self._device['address']

    def device_type(self):
        return self._device['type']

    def zone(self):
        return self._device['no']

    def set_state(self, new_state: YaleLockState):
        self._state = new_state

    def _calc_state(self):
        state = self._device['status1']

        lock_status_str = self._device['minigw_lock_status']
        if lock_status_str != '':
            lock_status = int(lock_status_str, 16)
            closed = ((lock_status & 16) == 16)
            locked = ((lock_status & 1) == 1)
            if closed is True and locked is True:
                state = YaleLockState.LOCKED
            elif closed is True and locked is False:
                state = YaleLockState.UNLOCKED
            elif not closed:
                state = YaleLockState.DOOR_OPEN
        elif "device_status.lock" in state:
            state = YaleLockState.LOCKED
        elif "device_status.unlock" in state:
            state = YaleLockState.UNLOCKED
        else:
            state = YaleLockState.UNKNOWN
        return state

    def close(self):
        """
        Attempt to close the remote lock.
        Returns:

        """
        return self._lock_api.close_lock(lock=self)

    def open(self, pin_code: str):
        return self._lock_api.open_lock(lock=self, pin_code=pin_code)


class YaleDoorManAPI:
    """
    Represents the yale doorman api.

    Example: iterating
        >>> client = YaleClient(username, password)
        >>> for lock in client.lock.locks():
        >>>     print(f"{lock}")
        >>>     lock.close()
        >>>     print(f"{lock}")
        >>>     lock.open()
        myfrontdoor [YaleLockState.UNLOCKED]
        myfrontdoor [YaleLockState.LOCKED]
        myfrontdoor [YaleLockState.UNLOCKED]

    Example: getting
        >>> client = YaleClient(username, password)
        >>> lock = client.lock.get("myfrondoor"):
        >>> print(f"{lock}")
        >>> lock.close()
        >>> print(f"{lock}")
        >>> lock.open()
        myfrontdoor [YaleLockState.UNLOCKED]
        myfrontdoor [YaleLockState.LOCKED]
        myfrontdoor [YaleLockState.UNLOCKED]

    """
    CODE_SUCCESS = "000"
    # lock status
    _ENDPOINT_DEVICES_STATUS = "/api/panel/device_status/"
    # lock door
    _ENDPOINT_DEVICES_CONTROL = "/api/panel/device_control/"
    _ENDPOINT_DEVICES_UNLOCK = "/api/minigw/unlock/"

    def __init__(self, auth):
        self.auth = auth

    def locks(self):
        """
        Iterate through the locks we have available for this user.
        Yields: the locks

        Example:
            >>> client = YaleClient(username, password)
            >>> for lock in client.lock.locks():
            >>>     print(f"{lock}")
            myfrontdoor [YaleLockState.UNLOCKED]
        """
        devices = self.auth.get_authenticated(self._ENDPOINT_DEVICES_STATUS)
        for device in devices['data']:
            if device['type'] == YaleLock.DEVICE_TYPE:
                lock = YaleLock(device, lock_api=self)
                yield lock

    def get(self, name: str):
        """
        Get a single lock with matching name.

        Args:
            name: The lock name

        Returns:
            An object representing the lock
            or None

        Example:
            >>> client = YaleClient(username, password)
            >>> lock = client.lock.get("myfrontdoor"):
            >>> print(f"{lock}")
            myfrontdoor [YaleLockState.UNLOCKED]
        """
        for lock in self.locks():
            if lock == name:
                return lock
        return None

    def close_lock(self, lock: YaleLock):
        """
        Close the specified lock.  If the operation is successful the lock state will be updated to reflect this.
        Notes:
            the lock object has methods to do this, see YaleLock:close()
        Args:
            lock: The lock you want to close.

        Returns: True if the operation was a success.

        Example:
            >>> client = YaleClient(username, password)
            >>> lock = client.lock.get("myfrontdoor"):
            >>> client.lock.close_lock(lock)
            >>> print(f"{lock}")
            myfrontdoor [YaleLockState.LOCKED]
        """
        params = {
            "area": lock.area(),
            "zone": lock.zone(),
            "device_sid": lock.sid(),
            "device_type": lock.device_type(),
            "request_value": "1"
        }
        operation_status = self.auth.post_authenticated(self._ENDPOINT_DEVICES_CONTROL, params=params)
        success = operation_status['code'] == self.CODE_SUCCESS
        if success:
            lock.set_state(YaleLockState.LOCKED)
        return success

    def open_lock(self, lock: YaleLock, pin_code: str):
        """
        Opens the specified lock.
        If the operation is a success the local state of lock will be updated to reflect this.
        Args:
            lock: the lock to open
            pin_code: a valid pin code for the door.

        Returns:
            True if the operation was a success.

        Example:
            >>> client = YaleClient(username, password)
            >>> lock = client.lock.get("myfrontdoor"):
            >>> client.lock.open_lock(lock, pin_code="123456")
            >>> print(f"{lock}")
            myfrontdoor [YaleLockState.UNLOCKED]
        """
        params = {
            "area": lock.area(),
            "zone": lock.zone(),
            "pincode": pin_code
        }
        operation_status = self.auth.post_authenticated(self._ENDPOINT_DEVICES_UNLOCK, params=params)
        success = operation_status['code'] == self.CODE_SUCCESS
        if success:
            lock.set_state(YaleLockState.UNLOCKED)
        return success