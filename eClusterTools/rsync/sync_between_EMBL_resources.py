import os
import sys
from pathlib import Path

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
    assert (len(sys.argv) == 4) or (len(sys.argv) == 5)
    dir_path = sys.argv[1]
    args_source = sys.argv[2]
    args_target = sys.argv[3]
    zip_zarr_microscopy = True
    if len(sys.argv) == 5:
        zip_zarr_microscopy = False

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
    assert args_target in shortcuts_keys, "Target not recognized, choose between {}".format(shortcuts_keys)
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

    if not zip_zarr_microscopy:
        command = 'rsync -a --delete --progress "{}" "{}"'.format(
            source_rsync, target_rsync)
        # command = 'rsync -avxHAX --progress "{}" "{}"'.format(
        #     source_rsync, target_rsync)
        os.system(command)
    else:
        # First, we rsync all files/folders in `source_rsync` that are not folders named `microscopy.zarr` (including subfolders) to `target_rsync`:
        command = 'rsync -a --delete --progress --exclude="microscopy.zarr" --exclude="spatialdata.zarr" "{}" "{}"'.format(
            source_rsync, target_rsync)
        os.system(command)
        # We loop over each folder named `microscopy.zarr` in `source_rsync` (including subfolders named `microscopy.zarr`)
        for root, dirs, files in os.walk(source_rsync):
            for one_dir in dirs:
                if one_dir == "microscopy.zarr" or one_dir == "spatialdata.zarr":
                    microscopy_zarr_folder = os.path.join(root, one_dir)
                    root_folder_target = os.path.join(target_rsync,
                                                                 Path(source_rsync).name,
                                                                 os.path.relpath(root, source_rsync))
                    # Zip the content of the folder named `microscopy.zarr` in `source_rsync`:
                    print("Zipping content of folder '{}'...".format(microscopy_zarr_folder))
                    command = 'cd "{}" && tar -zcf microscopy.zarr.tar.gz {}'.format(
                        root, one_dir)
                    os.system(command)
                    # Copy the zipped content to the correct subfolder of `target_rsync`:
                    os.makedirs(root_folder_target, exist_ok=True)
                    command = 'cp "{}/microscopy.zarr.tar.gz" "{}"'.format(
                        root, root_folder_target)
                    print("Copying zipped content...")
                    os.system(command)
                    # Unzip the zipped content in the correct subfolder of `target_rsync`:
                    print("Unzipping content and cleaning up...")
                    command = 'cd "{}" && tar -xzf microscopy.zarr.tar.gz'.format(
                        root_folder_target)
                    os.system(command)
                    # Remove the zipped content in the correct subfolder of `target_rsync` and the zipped content in `source_rsync`:
                    command = 'rm "{}/microscopy.zarr.tar.gz"'.format(
                        root_folder_target)
                    os.system(command)
                    command = 'rm "{}/microscopy.zarr.tar.gz"'.format(
                        root)
                    os.system(command)

                    # TODO: directly tar and transfer the folder
                    # FIXME: what happens if the folder already exists?

