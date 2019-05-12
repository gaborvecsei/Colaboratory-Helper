from pathlib import Path
from google.colab import files
import subprocess
import os


def setup_my_ssh_key(key_string: str = None, regex_for_file_name: str = "*id_rsa"):
    if key_string is None:
        # Open file uploader
        _ = files.upload()
    else:
        # Write the provided contents of the key file to a file
        with open("custom_id_rsa", "w") as f:
            f.write(key_string)

    # Find the uploaded ssh key file
    ssh_key_file_path = list(Path(".").glob(regex_for_file_name))
    if len(ssh_key_file_path) == 0:
        raise FileNotFoundError("Could not find a file with the following regex: {0}".format(regex_for_file_name))
    ssh_key_file_path = ssh_key_file_path[0]
    print("[*] Selected SSH key file: {0}".format(ssh_key_file_path))

    # Setup the key file
    ssh_folder = Path("/root/.ssh/")
    new_ssh_key_path = ssh_folder / "id_rsa"
    known_hosts_file_path = ssh_folder / "known_hosts"

    ssh_folder.mkdir(parents=True, exist_ok=True)
    new_ssh_key_path.write_text(ssh_key_file_path.read_text())
    subprocess.check_call(["chmod", "600", str(new_ssh_key_path)])
    keyscan_out = subprocess.check_output(["ssh-keyscan", "github.com"])
    known_hosts_file_path.write_bytes(keyscan_out)
