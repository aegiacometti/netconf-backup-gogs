from sys import argv, exit
from time import localtime, strftime
from glob import glob
from os import remove, rename, path, mkdir
from shutil import copy

device_hostname = argv[1]
backup_dir = argv[2]
keep_local_history = argv[3]
historic_files_to_keep = argv[4]

if not backup_dir.endswith('/'):
    backup_dir = backup_dir + '/'


def remove_old_files():
    list_files = glob(backup_dir + '{}*'.format(device_hostname))

    if len(list_files) >= int(historic_files_to_keep):
        list_files.sort()
        for index in range(int(historic_files_to_keep)-1, len(list_files)-1):
            remove(list_files[index])


def rename_current_file():
    get_date = localtime()
    current_date = strftime('%Y-%m-%d-%H-%M-%S', get_date)

    filename = backup_dir + '{}-{}.ucs'.format(device_hostname, current_date)

    rename(backup_dir + 'backup.ucs', filename)


def check_dir():
    if not path.exists(backup_dir):
        try:
            mkdir(backup_dir)
        except OSError:
            print("Creation of backup directories at %s failed" % backup_dir)
            return False
        else:
            return True

    if not path.exists(backup_dir + 'gogs-staging'):
        try:
            mkdir(backup_dir + 'gogs-staging')
        except OSError:
            print("Creation of backup directories at %s failed" % backup_dir)
            return False
        else:
            return True
    else:
        return True


def save_file_to_gogs_staging():
    filename = backup_dir + 'gogs-staging/{}.cfg'.format(device_hostname)
    copy(backup_dir + 'backup.ucs', filename)


if __name__ == '__main__':
    if check_dir():
        save_file_to_gogs_staging()
        if keep_local_history == 'yes':
            rename_current_file()
            remove_old_files()
        else:
            remove(backup_dir + 'backup.ucs')
    else:
        exit(1)
