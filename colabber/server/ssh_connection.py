"""
Code/idea is adapted from
https://imadelhanafi.com/posts/google_colal_server/
"""

import getpass
import random
import shlex
import string
import subprocess


def _generate_random_str(length: int):
    rnd_str = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(length))
    return rnd_str


def _run_cmd(cmd: str, in_bg: bool = False):
    # args = shlex.split(cmd)
    # TODO: do not use shell=True
    p = subprocess.Popen(cmd, shell=True)
    if not in_bg:
        p.wait()


def _setup_sshd():
    _run_cmd("apt-get install openssh-server > /dev/null")
    _run_cmd("apt-get install pwgen > /dev/null")


def _set_root_pwd(ssh_pwd: str) -> tuple:
    username = "root"
    if ssh_pwd is None:
        ssh_pwd = _generate_random_str(30)
    _run_cmd("echo {0}:{1} | chpasswd".format(username, ssh_pwd))
    _run_cmd(" mkdir -p /var/run/sshd")
    _run_cmd('echo "PermitRootLogin yes" >> /etc/ssh/sshd_config')
    _run_cmd('echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config')
    return username, ssh_pwd


def _run_sshd():
    _run_cmd('/usr/sbin/sshd -D', in_bg=True)


def _download_ngrok():
    _run_cmd('wget -q -c -nc https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip')
    _run_cmd('unzip -qq -n ngrok-stable-linux-amd64.zip')


def _setup_ngrok(ngrok_authtoken: str):
    _run_cmd('./ngrok authtoken {0}'.format(ngrok_authtoken))
    _run_cmd("./ngrok tcp 22", in_bg=True)


def setup_ssh_port_forwarding(ssh_pwd: str = None, ngrok_authtoken: str = None):
    _setup_sshd()
    username, password = _set_root_pwd(ssh_pwd)
    print("[*] Username: {0}".format(username))
    print("[*] Password (Use this for your SSH connection): {0}".format(password))
    _run_sshd()
    _download_ngrok()
    if ngrok_authtoken is None:
        print("Get your authtoken from https://dashboard.ngrok.com/auth")
        print("Please enter you authtoken below:")
        ngrok_authtoken = getpass.getpass()
    _setup_ngrok(ngrok_authtoken)
    print("SSH Port Forwarding is setup up via Ngrok")
    print("You can use it like: ssh root@0.tcp.ngrok.io -p [ngrok_port]")


def terminate_ssh_port_forwarding():
    _run_cmd("kill $(ps aux | grep './ngrok' | awk '{print $2}')")
