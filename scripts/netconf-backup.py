from sys import argv, exit
from time import localtime, strftime
from glob import glob
from os import remove, path, mkdir

device_hostname = argv[1]
output = argv[2]
backup_dir = argv[3]
keep_local_history = argv[4]
historic_files_to_keep = argv[5]

if not backup_dir.endswith('/'):
    backup_dir = backup_dir + '/'


def remove_old_files():
    list_files = glob(backup_dir + '{}*'.format(device_hostname))

    if len(list_files) >= int(historic_files_to_keep):
        list_files.sort()
        for index in range(int(historic_files_to_keep)-1, len(list_files)-1):
            remove(list_files[index])


def search_changed_config_file():
    list_files = glob(backup_dir + '{}*'.format(device_hostname))

    if len(list_files) == 0:
        return True

    list_files.sort(reverse=True)

    last_file = open(list_files[0], 'r')
    last_file_text = last_file.read()

    return output != last_file_text


def save_file_with_date():
    get_date = localtime()
    current_date = strftime('%Y-%m-%d-%H-%M-%S', get_date)

    filename = backup_dir + '{}-{}.cfg'.format(device_hostname, current_date)
    file = open(filename, 'w')
    file.write(output)
    file.close()


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
            print("Creation of backup directories at %s failed" % (backup_dir + 'staging'))
            return False
        else:
            return True
    else:
        return True


def save_file_to_gogs_staging():
    filename = backup_dir + 'gogs-staging/{}.cfg'.format(device_hostname)

    if path.exists(filename):
        current_filename = open(filename, 'r')
        current_filename_text = current_filename.read()
        current_filename.close()

        if output != current_filename_text:
            file = open(filename, 'w')
            file.write(output)
            file.close()
    else:
        file = open(filename, 'w')
        file.write(output)
        file.close()


if __name__ == '__main__':
    if check_dir():
        save_file_to_gogs_staging()
        if keep_local_history == 'yes':
            if search_changed_config_file():
                save_file_with_date()
            remove_old_files()
    else:
        exit(1)
