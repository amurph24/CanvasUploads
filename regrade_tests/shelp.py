
import os

### creates a dir if it doesn't already exist
def make_dir_if_missing(dirname):
    if os.path.isdir(dirname):
        print(f"{dirname} exists")
        return
    os.mkdir(dirname)
    print(f"{dirname} created")


### get file name segment after first string
def get_file_type(file_path):
    return os.path.splitext(file_path)[1]

### get file name before extension
def get_file_name(file_path):
    return os.path.splitext(file_path)[0]

### validates directory at a given path
def validate_dir(dir_path):
    # Check if the path exists
    if not os.path.exists(dir_path):
        print(f"The directory '{dir_path}' does not exist.")
        return False

    # Check if the path is a directory
    if not os.path.isdir(dir_path):
        print(f"The specified path '{dir_path}' is not a directory.")
        return False
    
    return True


### returns a list of non-hidden files
def list_dir_contents(dir_path):
    contents = os.listdir(dir_path)

    # filter out hidden files and directories
    contents = [item for item in contents if not item.startswith(".")]
    return contents