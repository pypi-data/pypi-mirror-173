from typing import Dict


def read_yaml(file_path: str) -> Dict:
    import yaml

    with open(file_path, "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            return {}

def get_tf_files_paths(folder_path: str):
    from os.path import isfile, join
    import glob

    # List .tf files in the folder
    tf_globs = glob.glob(join(folder_path,"*.tf"))
    # Keep files only
    tf_files = [f for f in tf_globs if isfile(f)]
    return tf_files