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

MAIN_DIR_MAC = ["/Users/alberto-mac/Documents/DA_ESPORTARE/LOCAL_EMBL_FILES/scratch/bailoni",
                "/Users/alberto-mac/Documents/DA_ESPORTARE/LOCAL_EMBL_FILES/g_shared/shared",
                "/Users/alberto-mac/Documents/DA_ESPORTARE/LOCAL_EMBL_FILES/data_bailoni",
                "/Users/alberto-mac/Documents/DA_ESPORTARE/LOCAL_EMBL_FILES/g_alexandr/bailoni",
                ]
# SSHFS_DIR_MAC = ["/Users/alberto-mac/sshfs_vol/scratch",
#                  "/Users/alberto-mac/sshfs_vol/g_shared",
#                  "/Users/alberto-mac/sshfs_vol/data_bailoni", # FIXME
#                  ]
MAIN_DIR_SERVER = ["/scratch/bailoni",
                   "/g/scb/alexandr/shared",
                   "/home/bailoni/data_bailoni",
                   "/g/alexandr/bailoni"
                   ]
MAIN_DIR_DATATRANSFERR = ["/scratch/bailoni",
                          "/g/scb/alexandr/shared",
                          "/home/bailoni/data_bailoni",
                          "/g/alexandr/bailoni"
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

    # Create dir:
    given_path_base = None
    selected_path_type = None
    for idx in range(len(MAIN_DIR_MAC)):
        if MAIN_DIR_MAC[idx] in dir_path:
            given_path_base = MAIN_DIR_MAC[idx]
        if given_path_base is not None:
            selected_path_type = idx
            break

    assert isinstance(given_path_base, str), "Path not recognised"


    # Choose to which server to connect:
    server_name = "login" if selected_path_type == 0 else "datatransfer"


    rel_path = os.path.relpath(dir_path, given_path_base)
    rel_path_containing_dir = os.path.relpath(containing_dir, given_path_base)
    dir_path_mac = os.path.join(MAIN_DIR_MAC[selected_path_type], rel_path)
    containing_dir_path_mac = os.path.join(MAIN_DIR_MAC[selected_path_type], rel_path_containing_dir)
    dir_data_transfer = os.path.join(MAIN_DIR_DATATRANSFERR[selected_path_type], rel_path)
    containing_dir_data_transfer = os.path.join(MAIN_DIR_DATATRANSFERR[selected_path_type], rel_path_containing_dir)

    target_dir = dir_data_transfer if is_dir else containing_dir_data_transfer
    # check_dir_and_create(target_dir)

    # os.system(open_finder)

    # Now start syncing:
    print(is_dir)
    source_dir = os.path.join(dir_path_mac, "") if is_dir else dir_path_mac
    rsync_options = "-zar" if is_dir else "-avz"
    # TODO: add customizable exclude and include arguments
    command = 'rsync {} --progress --rsync-path="mkdir -p {} && rsync" --protect-args -e "ssh -p 22" "{}" "{}:{}"'.format(
        rsync_options, target_dir, source_dir, server_name, target_dir)
    # command = 'rsync {} --progress --rsync-path="mkdir -p {} && rsync" --protect-args --include="*/" --include="*.h5ad" --exclude="*" -e "ssh -p 22" "{}" "{}:{}"'.format(
    print(command)
    os.system(command)
