from numpy import genfromtxt
from eClusterTools.paths import get_scratch_dir
import os

# path_file = os.path.join(get_scratch_dir(), "pyCh_repos/EMBLclusterTools/configs/pycharm_paths.csv")
path_file = "/Users/alberto-mac/EMBL_repos/EMBLclusterTools/configs/pycharm_paths.csv"

pycharm_paths = genfromtxt(path_file, delimiter=';',encoding="utf8", dtype=None)

for local_path, remote_path in pycharm_paths:
    # if "nifty" in local_path:
    print("\n\n## ---- Copying {} ---- ##".format(local_path))
    command = "rsync -chavzP --stats {}/ sergio:{}".format(local_path, remote_path)
    unknown_dir = os.system(command)
