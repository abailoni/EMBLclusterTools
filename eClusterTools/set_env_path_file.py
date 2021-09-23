from numpy import genfromtxt
from eClusterTools.paths import get_scratch_dir
import os
import setuptools

path_file = os.path.join(get_scratch_dir(), "pyCh_repos/EMBLclusterTools/configs/python_include_paths.csv")
# path_file = "/Users/alberto-mac/EMBL_repos/EMBLclusterTools/configs/pycharm_paths.csv"

pycharm_paths = genfromtxt(path_file, delimiter=';',encoding="utf8", dtype=None)

def create_pth_file(config_name='my_config.pth', create_in_site_package_dir=True):
    assert config_name.endswith('.pth')
    if create_in_site_package_dir:
        output_file = os.path.join(setuptools.__path__[0], "../", config_name)
    else:
        output_file = os.path.join(os.getcwd(), config_name)
    with open(output_file, "w") as f:
        for remote_path in pycharm_paths:
            f.write("{}\n".format(remote_path))


if __name__ == "__main__":
    # execute only if run as a script
    create_pth_file()
