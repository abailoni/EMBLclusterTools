import os

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
                "/Users/alberto-mac/Documents/DA_ESPORTARE/LOCAL_EMBL_FILES/g_shared"]
SSHFS_DIR_MAC = ["/Users/alberto-mac/sshfs_vol/scratch",
                 "/Users/alberto-mac/sshfs_vol/g_shared",]
MAIN_DIR_SERVER = ["/scratch/bailoni",
                   "/g/scb/alexandr"]
MAIN_DIR_DATATRANSFERR = ["/home/bailoni/scratch",
                          "/home/bailoni/g_shared"]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scripts parameters')
    parser.add_argument('--dir', required=False,
                        default=[], type=str, help='folder containing data to run or train on')
    args = parser.parse_args()

    dir_path = args.dir

    given_path_base = None
    is_mac_address = False
    for idx in range(2):
        if MAIN_DIR_SERVER[idx] in dir_path:
            given_path_base = MAIN_DIR_SERVER[idx]
        elif MAIN_DIR_DATATRANSFERR[idx] in dir_path:
            given_path_base = MAIN_DIR_DATATRANSFERR[idx]
        elif MAIN_DIR_MAC[idx] in dir_path:
            is_mac_address = True
            given_path_base = MAIN_DIR_MAC[idx]
        elif SSHFS_DIR_MAC[idx] in dir_path:
            is_mac_address = True
            given_path_base = SSHFS_DIR_MAC[idx]
        if given_path_base is not None:
            selected_path_type = idx
            break

    assert isinstance(given_path_base, str), "Path not recognised"


    dir_data_transfer = os.path.join(MAIN_DIR_DATATRANSFERR, rel_path)
    dir_server = os.path.join(MAIN_DIR_SERVER, rel_path)
    dir_mac = os.path.join(SSHFS_DIR_MAC, rel_path)

    if is_mac_address:
        # Return server path and copy it to clipboard:
        copy_to_clipboard = "printf '{}' | pbcopy".format(dir_server)
        os.system(copy_to_clipboard)
        print("{} copied to clipboard!".format(dir_server))
    else:
        # Return Mac address and open Finder, if mounted:
        copy_to_clipboard = "printf '{}' | pbcopy".format(dir_mac)
        os.system(copy_to_clipboard)
        open_finder = 'open {}'.format(dir_mac)
        os.system(open_finder)




