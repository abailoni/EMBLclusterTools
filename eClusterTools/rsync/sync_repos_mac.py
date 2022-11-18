import time

import os
import argparse
import subprocess

MAIN_DIR_MAC = "/Users/alberto-mac"
MAIN_DIR_DATATRANSFERR = "/home/bailoni/data_bailoni/pyCh_repos"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scripts parameters')
    parser.add_argument('--repo', required=True,
                        default=[], type=str, help='Name of the repo')
    parser.add_argument('--sync_git', action='store_true', help='Flag to sync git data')
    parser.add_argument('--delete', action='store_true',
                        help='Flag to create a perfect copy and delete extra remote files')
    parser.add_argument('--dirUp', required=False,
                        default="EMBL_repos", type=str, help='Name of the dir containing the repo on Mac')

    args = parser.parse_args()

    repo = args.repo
    dirUp = args.dirUp
    repo_path = os.path.join(MAIN_DIR_MAC, dirUp, repo)
    # print(repo_path)
    assert os.path.exists(repo_path)
    assert os.path.isdir(repo_path)

    # Create dir:
    server_repo_path = os.path.join(MAIN_DIR_DATATRANSFERR)

    # Sync:
    rsync_options = "-zar "
    rsync_exclusions = "--exclude=.svn --exclude=.cvs --exclude=.idea --exclude=.DS_Store --exclude=.hg --exclude=*.hprof --exclude=*.pyc "
    if not args.sync_git:
        rsync_exclusions += " --exclude=.git"
    command = '/opt/homebrew/bin/rsync {} {} --progress --rsync-path="mkdir -p {} && rsync" --protect-args -e "ssh -p 22" "{}" "datatransfer:{}"'.format(
        rsync_options + rsync_exclusions,
        "--delete" if args.delete else "",
        server_repo_path, repo_path, server_repo_path)
    print("###### Rsync command: \n", command)
    # time.sleep(10)
    # subprocess.run(command, shell=True, check=True)
    # proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    # (out, err) = proc.communicate()
    result = subprocess.run(command, capture_output=True,
                            shell=True,
                            # text=True
                            check=False
                            )
    # print(result.stdout)
    # print(result.stderr)
    print("\n\n###### Command output:\n", result.stdout.decode("utf-8"))
    stderr = result.stderr.decode("utf-8")
    if not stderr.endswith("for such purpose.\n"):
        # print("\n\n#### Command error: \n", stderr)
        print("\n\n#### Command error: \n", stderr[-2:])

    # os.system(command)
