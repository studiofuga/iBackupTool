#! /usr/bin/env python
from ibackuptool import ibackup
from argparse import ArgumentParser
import os
from pathlib import Path


class IBackupToolApp:
    def __init__(self):
        pass

    def reconstruct(self, bck :ibackup, outdir:str):
        self._mkoutputdir(outdir)
        bck.open()
        self._extract_directories(bck, outdir)

        files = bck.get_all_files()
        for fileInfo in files:
            print("Extracting {0} -> {1} / {2}".format(fileInfo[0], fileInfo[1], bck.get_full_filename_for_fileId(fileInfo[1])))
            os.symlink(src=bck.get_full_filename_for_fileId(fileInfo[1]),
                       dst=os.path.join(outdir, fileInfo[0]))

    def _extract_directories(self, bck, outdir):
        dirs = bck.get_all_directories()
        for dir in dirs:
            print("Extracting Dir: {}".format(dir))
            try:
                Path(os.path.join(outdir, dir)).mkdir(parents=True)
            except FileExistsError:
                pass

    def _mkoutputdir(self, outdir):
        try:
            Path(outdir).mkdir(parents=True)
        except FileExistsError:
            # If already exists, skip it
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
