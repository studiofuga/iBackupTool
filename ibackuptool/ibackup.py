import os
import sqlite3


class IBackup:
    _DBFILE = "Manifest.db"

    def __init__(self, path):
        self.path = os.path.abspath(path)

    def check_lock(self):
        """
        Check if the backup is "locked" / Read Only by checking the permissions on dhe Manifest.db file
        :return: true if the backup is read only, false if it is writable
        """
        if os.access(self._manifest_file(), os.W_OK):
            return False
        return True

    def open(self):
        url = "file:{}?mode=ro&immutable=1".format(self._manifest_file())
        print("Opening: {}".format(url))
        self.db = sqlite3.connect(url, uri=True)

    def get_all_directories(self):
        sql = "SELECT relativePath, domain FROM Files WHERE flags=2 AND relativePath != ''"
        cursor = self.db.execute(sql)
        all = cursor.fetchall()
        return ((a[0], a[1]) for a in all)

    def get_all_files(self):
        sql = "SELECT relativePath,domain, fileID FROM Files WHERE flags=1 AND relativePath != ''"
        cursor = self.db.execute(sql)
        all = cursor.fetchall()
        return ((a[0], a[1], a[2]) for a in all)

    def get_full_filename_for_fileId(self, fileId):
        sub = fileId[:2]
        return os.path.join(self.path, sub, fileId)

    def _manifest_file(self):
        return os.path.join(self.path, self._DBFILE)