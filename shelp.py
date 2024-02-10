
import os
import codecs
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

def has_bom(file_path):
    with open(file_path, 'rb') as file:
        bom = file.read(3)
        return bom == b'\xef\xbb\xbf'
    
def remove_bom(file_path):
    if (has_bom):
        with codecs.open(file_path, 'r', encoding='utf-8-sig') as file:
            content = file.read()
    
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f'BOM removed from: {file_path}')
    else:
        print(f'{file_path} does not contain BOM')