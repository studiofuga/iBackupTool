#! /usr/bin/env python
from ibackuptool import ibackup
from argparse import ArgumentParser
import os
from pathlib import Path


class IBackupToolApp:
    def __init__(self):
        pass

    def reconstruct(self, bck :ibackup, outdir:str):
        try:
            Path(outdir).mkdir(parents=True)
        except FileExistsError:
            # If already exists, skip it
            pass
        bck.open()
        dirs = bck.get_all_directories()
        for dir in dirs:
            print("Extracting Dir: {}".format(dir))
            try:
                Path(os.path.join(outdir, dir)).mkdir(parents=True)
            except FileExistsError:
                pass


if __name__ == "__main__":
    parser = ArgumentParser(
        description=''
    )
    parser.add_argument('backup', help='the path of the backup to work on')
    parser.add_argument('--unpack', help='Unpack the backup into a File System directory using symlinks')
    args = parser.parse_args()

    bkp = ibackup.IBackup(args.backup)
    if not bkp.check_lock():
        raise Exception('Database is writable')

    app = IBackupToolApp()

    if args.unpack is not None:
        app.reconstruct(bkp, args.unpack)
