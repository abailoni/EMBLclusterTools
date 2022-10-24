import os

"""
In this version:
 - if a directory path is given, we only update its content at the top level.
 - if a file path is given, we only update the content of the folder it is contained into.


"""


def check_dir_and_create(directory):
    '''
    if the directory does not exist, create it
    '''
    folder_exists = os.path.exists(directory)
    if not folder_exists:
        os.makedirs(directory)
    return folder_exists

import argparse

MAIN_DIR_MAC = ["/Users/alberto-mac/Documents/DA_ESPORTARE/LOCAL_EMBL_FILES/scratch",
                "/Users/alberto-mac/Documents/DA_ESPORTARE/LOCAL_EMBL_FILES/g_shared",
                "/Users/alberto-mac/Documents/DA_ESPORTARE/LOCAL_EMBL_FILES/data_bailoni",
                ]
SSHFS_DIR_MAC = ["/Users/alberto-mac/sshfs_vol/scratch",
                 "/Users/alberto-mac/sshfs_vol/g_shared",
                 "/Users/alberto-mac/sshfs_vol/data_bailoni", # FIXME
                 ]
MAIN_DIR_SERVER = ["/scratch/bailoni",
                   "/g/scb/alexandr",
                   "/home/bailoni/data_bailoni"
                   ]
MAIN_DIR_DATATRANSFERR = ["/home/bailoni/scratch3",
                          "/home/bailoni/g_shared3",
                          "/home/bailoni/data_bailoni",
                          ]
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scripts parameters')
    parser.add_argument('--dir', required=False,
                        default=[], type=str, help='folder containing data to run or train on')
    args = parser.parse_args()

    dir_path = args.dir
    containing_dir, path_tail = os.path.split(dir_path)
    extension = os.path.splitext(path_tail)[1]
    is_dir = extension == ""
    # assert extension == "", "This is not a directory but a file!"

    # If a file is given, update the containing folder:
    if not is_dir:
        dir_path = containing_dir

    # Create dir:
    given_path_base = None
    for idx in range(len(MAIN_DIR_MAC)):
        if MAIN_DIR_SERVER[idx] in dir_path:
            given_path_base = MAIN_DIR_SERVER[idx]
        elif MAIN_DIR_MAC[idx] in dir_path:
            given_path_base = MAIN_DIR_MAC[idx]
        elif SSHFS_DIR_MAC[idx] in dir_path:
            given_path_base = SSHFS_DIR_MAC[idx]
        if given_path_base is not None:
            selected_path_type = idx
            break

    assert isinstance(given_path_base, str), "Path not recognised"

    rel_path = os.path.relpath(dir_path, given_path_base)
    dir_path_mac = os.path.join(MAIN_DIR_MAC[selected_path_type], rel_path)
    dir_data_transfer = os.path.join(MAIN_DIR_DATATRANSFERR[selected_path_type], rel_path)

    target_dir = dir_path_mac
    check_dir_and_create(target_dir)

    # Open folder in Finder app:
    # open_finder = '''osascript -e 'tell application "Finder"
    # if not (exists Finder window 1) or (get collapsed of the front Finder window) then
    #     make new Finder window
    # end if
    # set thePath to POSIX file {}
    # set the target of the front Finder window to folder thePath
    # activate
    # end tell'
    # '''.format(target_dir)

    print(target_dir)
    print(dir_data_transfer)

    open_finder = 'open "{}"'.format(target_dir)
    os.system(open_finder)

    # Now start syncing:
    rsync_options = "-zar -f '- /*/*'"
    command = 'rsync {} --protect-args --progress -e "ssh -p 22" "datatransfer:{}" "{}"'.format(
        rsync_options, os.path.join(dir_data_transfer, "*"), target_dir)
    # command = 'gpg -d -q --pinentry-mode=loopback --passphrase 8426 ~/.embl2.gpg > fifo; sshpass -f fifo rsync {} --protect-args --progress -e "ssh -p 22" "datatransfer:{}" "{}"'.format(
    #     rsync_options, os.path.join(dir_data_transfer, "*"), target_dir)
    # print(command)
    os.system(command)

