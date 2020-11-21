#! /usr/bin/env python
from ibackuptool import ibackup
from argparse import ArgumentParser


if __name__ == "__main__":
    parser = ArgumentParser(
        description=''
    )
    parser.add_argument('backup', help='the path of the backup to work on')
    args = parser.parse_args()

    bkp = ibackup.IBackup(args.backup)
    if not bkp.check_lock():
        raise Exception('Database is writable')

