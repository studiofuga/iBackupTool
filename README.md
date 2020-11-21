# iBackupTool

This tool allows the easy extraction of iOS backup extracted with idevicebackup2

The reconstruct the structure of the file system by extracting data from the Manifest.db file (sqlite3 database), 
it rebuilds the directory structure from the entrie tagged with flag=2 (directory), and by linking the files
with the proper hash file in the backup.

## Usage

The tool requires that the database is not writable. If it can be written by the current user, the tool quits.

The proper way to make it not-writable is to remove the write flag.

```$ chmod -R -w 123456...```

Then you can use the tool to rebuild the file system:

```$ ./backuptool --unpack destination_directory backup_directory```

if the backup is `123456...` then

```$ ./backuptool --unpack outdir 123456...```

