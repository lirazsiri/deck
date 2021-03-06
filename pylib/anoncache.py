# Copyright (c) TurnKey Linux - http://www.turnkeylinux.org
#
# This file is part of Deck
#
# Deck is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3 of the License, or (at your
# option) any later version.

import os
import time
import random
import hashlib
from utils import makedirs

from os.path import *

class Error(Exception):
    pass

class AnonCache:
    """Class that maintains anonymous file blobs in a directory structure"""
    Error = Error

    def __init__(self, path):
        makedirs(path)
        self.path = path

    def _get_blob_path(self, id):
        if not id or len(id) < 3 or not id.isalnum():
            raise Error("illegal blob id `%s'" % id)
        
        return join(self.path, id[:2], id[2:])

    def exists(self, id):
        return exists(self._get_blob_path(id))
    
    def new_id(self, seed=None):
        def digest(s):
            return hashlib.md5(s).hexdigest()

        id = digest(`seed` + `time.time()` + `random.SystemRandom().getrandbits(128)`)
        while self.exists(id):
            id = digest(id)

        makedirs(dirname(self._get_blob_path(id)))
        return id

    def blob(self, id, mode=None, buffering=None):
        """opens a blob -> file object"""
        kws = {}
        if mode:
            kws['mode'] = mode

        if buffering:
            kws['buffering'] = buffering

        blob_path = self._get_blob_path(id)
        try:
            return file(blob_path, **kws)
        except IOError, e:
            raise Error(e)

    def delete(self, id):
        os.remove(self._get_blob_path(id))
        

