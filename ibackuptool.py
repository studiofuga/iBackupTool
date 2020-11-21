#! /usr/bin/env python
from ibackuptool import ibackup
from argparse import ArgumentParser
import os
from pathlib import Path
from ibackuptool import ibackupstats


class IBackupToolApp:
    def __init__(self):
        self.stats = ibackupstats.IBackupStats()
        pass

    def reconstruct(self, bck :ibackup, outdir:str):
        self._mkoutputdir(outdir)
        bck.open()

        self._extract_directories(bck, outdir, self.stats)
        self._extract_files(bck, outdir, self.stats)

        print("Dirs: {0}".format(self.stats.dirs))
        print("Files: {0}".format(self.stats.files))

    def _extract_files(self, bck :ibackup, outdir:str, stats : ibackupstats=None):
        numfiles = 0
        files = bck.get_all_files()
        for fileInfo in files:
            domain = fileInfo[1]
            path = fileInfo[0]
            target = fileInfo[2]

            if not os.path.exists(os.path.join(outdir, domain)):
                Path(os.path.join(outdir, domain)).mkdir()

            print("Extracting [{0}] {1} -> {2} -> {3}".format(
                domain, path, target, bck.get_full_filename_for_fileId(target)))
            os.symlink(src=bck.get_full_filename_for_fileId(target),
                       dst=os.path.join(outdir, domain, path))
            numfiles = numfiles+1

        if stats is not None:
            stats.files =numfiles
        return numfiles

    def _extract_directories(self, bck : ibackup, outdir:str, stats:ibackupstats = None):
        numdirs = 0
        dirs = bck.get_all_directories()
        for dir in dirs:
            domain = dir[1]
            path=dir[0]
            print("Extracting Dir: [{1}] {0}".format(domain, path))
            try:
                Path(os.path.join(outdir, domain, path)).mkdir(parents=True)
            except FileExistsError:
                pass
            numdirs = numdirs+1

        if stats is not None:
            stats.dirs =numdirs
        return numdirs

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
