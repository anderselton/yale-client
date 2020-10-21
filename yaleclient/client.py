#!/usr/bin/env python
"""The Yale client is meant to be used on Yale systems.  Its largely based on
https://github.com/domwillcode/yale-smart-alarm-client

However, some major refactorings have been done in an attempt to get it more pythonish and with a cleaner api.

"""

import logging

from .auth import YaleAuth
from .alarm import YaleSmartAlarmAPI
from .lock import YaleDoorManAPI

_LOGGER = logging.getLogger(__name__)


class YaleClient:

    def __init__(self, username, password, area_id=1):
        self.auth: YaleAuth = YaleAuth(username=username, password=password)
        self.area_id = area_id
        self.alarm: YaleSmartAlarmAPI = YaleSmartAlarmAPI(auth=self.auth, area_id=area_id)
        self.lock: YaleDoorManAPI = YaleDoorManAPI(auth=self.auth)

