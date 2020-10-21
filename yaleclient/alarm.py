#!/usr/bin/env python
"""

"""

import logging

_LOGGER = logging.getLogger(__name__)

YALE_STATE_ARM_FULL = "arm"
YALE_STATE_ARM_PARTIAL = "home"
YALE_STATE_DISARM = "disarm"

YALE_DOOR_CONTACT_STATE_CLOSED = "closed"
YALE_DOOR_CONTACT_STATE_OPEN = "open"
YALE_DOOR_CONTACT_STATE_UNKNOWN = "unknown"


class YaleSmartAlarmAPI:
    """
    This class handles interactions with the Alarm API.
    """
    _ENDPOINT_SERVICES = "/services/"
    _ENDPOINT_GET_MODE = "/api/panel/mode/"
    _ENDPOINT_SET_MODE = "/api/panel/mode/"
    _ENDPOINT_DEVICES_STATUS = "/api/panel/device_status/"

    _REQUEST_PARAM_AREA = "area"
    _REQUEST_PARAM_MODE = "mode"

    def __init__(self, auth, area_id=1):
        self.auth = auth
        self.area_id = area_id

    def get_doors_status(self):
        devices = self.auth.get_authenticated(self._ENDPOINT_DEVICES_STATUS)
        doors = {}
        for device in devices['data']:
            if device['type'] == "device_type.door_contact":
                state = device['status1']
                name = device['name']
                if "device_status.dc_close" in state:
                    state = YALE_DOOR_CONTACT_STATE_CLOSED
                elif "device_status.dc_open" in state:
                    state = YALE_DOOR_CONTACT_STATE_OPEN
                else:
                    state = YALE_DOOR_CONTACT_STATE_UNKNOWN
                doors[name] = state
        return doors

    def get_armed_status(self):
        alarm_state = self.auth.get_authenticated(self._ENDPOINT_GET_MODE)
        return alarm_state.get('data')[0].get('mode')

    def set_armed_status(self, mode):
        params = {
            self._REQUEST_PARAM_AREA: self.area_id,
            self._REQUEST_PARAM_MODE: mode
        }

        return self.auth.post_authenticated(self._ENDPOINT_SET_MODE, params=params)

    def arm_full(self):
        self.set_armed_status(YALE_STATE_ARM_FULL)

    def arm_partial(self):
        self.set_armed_status(YALE_STATE_ARM_PARTIAL)

    def disarm(self):
        self.set_armed_status(YALE_STATE_DISARM)

    def is_armed(self):
        """Return True or False if the system is armed in any way"""
        alarm_code = self.get_armed_status()

        if alarm_code == YALE_STATE_ARM_FULL:
            return True

        if alarm_code == YALE_STATE_ARM_PARTIAL:
            return True

        return False

