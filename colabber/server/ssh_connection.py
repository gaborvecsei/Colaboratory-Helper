"""
Code/idea is adapted from https://imadelhanafi.com/posts/google_colal_server/
"""

import getpass
import random
import shlex
import string
import subprocess


def _generate_random_str(length: int):
    rnd_str = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(length))
    return rnd_str


def _run_cmd(cmd: str, verbose: bool = True):
    # args = shlex.split(cmd)
    # TODO: do not use shell=True
    subprocess.check_call(cmd, shell=True)


def _setup_sshd():
    cmd = "apt-get install -qq -o=Dpkg::Use-Pty=0 openssh-server pwgen > /dev/null"
    _run_cmd(cmd)


def _set_root_pwd_random() -> tuple:
    pwd = _generate_random_str(30)
    _run_cmd("echo root:{0} | chpasswd".format(pwd))
    _run_cmd(" mkdir -p /var/run/sshd")
    _run_cmd('echo "PermitRootLogin yes" >> /etc/ssh/sshd_config')
    _run_cmd('echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config')

    return "root", pwd


def _run_sshd():
    _run_cmd('/usr/sbin/sshd -D &')


def _download_ngrok():
    _run_cmd('wget -q -c -nc https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip')
    _run_cmd('unzip -qq -n ngrok-stable-linux-amd64.zip')


def _setup_ngrok():
    authtoken = getpass.getpass()
    _run_cmd('./ngrok authtoken {0} && ./ngrok tcp 22 &'.format(authtoken))


def setup_ssh_port_forwarding():
    _setup_sshd()
    username, password = _set_root_pwd_random()
    print("[*] Username: {0}".format(username))
    print("[*] Password (Use this for your SSH connection): {0}".format(password))
    # _run_sshd()
    _download_ngrok()
    print("Get your authtoken from https://dashboard.ngrok.com/auth")
    print("Please enter you authtoken below:")
    _setup_ngrok()
    print("SSH Port Forwarding is setup up via Ngrok")
    print("You can use it like: ssh root@0.tcp.ngrok.io -p [ngrok_port]")


def terminate_ssh_port_forwarding():
    _run_cmd("kill $(ps aux | grep './ngrok' | awk '{print $2}')")
