import os
import sys

import argparse

shortcuts_keys = ["s", "g", "d", "a"]

MAIN_DIR_MAC = ["/Users/alberto-mac/Documents/DA_ESPORTARE/LOCAL_EMBL_FILES/scratch",
                "/Users/alberto-mac/Documents/DA_ESPORTARE/LOCAL_EMBL_FILES/g_shared/shared/alberto",
                "/Users/alberto-mac/Documents/DA_ESPORTARE/LOCAL_EMBL_FILES/data_bailoni",
                "/Users/alberto-mac/Documents/DA_ESPORTARE/LOCAL_EMBL_FILES/alexandr/alberto",
                ]
MAIN_DIR_SERVER = ["/scratch/bailoni",
                   "/g/scb/alexandr/shared/alberto",
                   "/home/bailoni/data_bailoni",
                   "/g/alexandr/alberto"]


if __name__ == '__main__':
    assert len(sys.argv) == 4
    dir_path = sys.argv[1]
    args_source = sys.argv[2]
    args_target = sys.argv[3]


    # parser = argparse.ArgumentParser(description='Scripts parameters')
    # parser.add_argument('-p', '--path', required=True,
    #                     type=str, help='folder containing data to run or train on')
    # parser.add_argument('-t', '--target', required=True,
    #                     type=str, help='Choose target between "s, g, d, a"')
    # parser.add_argument('-s', '--source', required=False, default=None,
    #                     type=str, help='Choose source between "s, g, d, a"')
    # args = parser.parse_args()
    #
    # dir_path = args.path
    # args_target = args.target
    # args_source = args.source


    containing_dir, path_tail = os.path.split(dir_path)
    extension = os.path.splitext(path_tail)[1]
    is_dir = extension == ""
    # assert extension == "", "This is not a directory but a file!"
    assert args_target in shortcuts_keys, "Target not recognized"
    target_index = shortcuts_keys.index(args_target)

    # Create dir:
    source_index = None
    if os.path.isabs(dir_path):
        given_path_base = None
        for idx in range(len(MAIN_DIR_MAC)):
            if MAIN_DIR_SERVER[idx] in dir_path:
                given_path_base = MAIN_DIR_SERVER[idx]
            elif MAIN_DIR_MAC[idx] in dir_path:
                given_path_base = MAIN_DIR_MAC[idx]
            if given_path_base is not None:
                source_index = idx
                break

        assert isinstance(given_path_base, str), "Path not recognised"

        rel_path = os.path.relpath(dir_path, given_path_base)
        rel_path_containing_dir = os.path.relpath(containing_dir, given_path_base)
    else:
        assert args_source is not None, "Source is required with relative paths"
        assert args_source in shortcuts_keys, "Source not recognized"
        source_index = shortcuts_keys.index(args_source)
        rel_path = dir_path
        rel_path_containing_dir = containing_dir


    # Compose rsync command:
    source_rsync = os.path.join(MAIN_DIR_SERVER[source_index],
                                rel_path)
    target_rsync = os.path.join(MAIN_DIR_SERVER[target_index],
                                rel_path_containing_dir)

    # Create destination folder:
    os.makedirs(target_rsync, exist_ok=True)


    command = 'rsync -a --delete --progress "{}" "{}"'.format(
        source_rsync, target_rsync)
    # command = 'rsync -avxHAX --progress "{}" "{}"'.format(
    #     source_rsync, target_rsync)
    os.system(command)
