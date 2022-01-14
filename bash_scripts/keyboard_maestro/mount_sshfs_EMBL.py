import os
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scripts parameters')
    parser.add_argument('--password', required=True, type=str)
    args = parser.parse_args()

    password = args.password

    os.system("umount -f /Users/alberto-mac/sshfs_vol")
    os.system("sshpass -p {} /usr/local/bin/sshfs bailoni@datatransfer.embl.de:/home/bailoni/ /Users/alberto-mac/sshfs_vol".format(password))

