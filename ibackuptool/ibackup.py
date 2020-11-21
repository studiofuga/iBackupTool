import os
import stat


class IBackup:
    _DBFILE = "Manifest.db"

    def __init__(self, path):
        self.path = path

    def check_lock(self):
        '''
        Check if the backup is "locked" / Read Only by checking the permissions on dhe Manifest.db file
        :return: true if the backup is read only, false if it is writable
        '''
        if os.access(os.path.join(self.path, self._DBFILE), os.W_OK):
            return False
        return True
