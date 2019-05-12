from pathlib import Path
from google.colab import files
import subprocess


def setup_my_ssh_key(key_string:str=None, regex_for_file_name: str = "*id_rsa"):
    if key_string is None:
        # Open file uploader
        _ = files.upload()
    else:
        # Write the provided contents of the key file to a file
        with open("custom_id_rsa", "w") as f:
            f.write(key_string)

    # Find the uploaded ssh key file
    ssh_key_file_name = list(Path(".").glob(regex_for_file_name))
    if len(ssh_key_file_name) == 0:
        raise FileNotFoundError("Could not find a file with the following regex: {0}".format(regex_for_file_name))
    ssh_key_file_name = str(ssh_key_file_name[0])
    print("[*] Selected SSH key file: {0}".format(ssh_key_file_name))

    # Setup the key file
    _ = subprocess.check_call(["add_ssh_key.sh", ssh_key_file_name])
