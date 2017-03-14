import os
import glob
from misc import *

def scp_thirdparty(local_path, host, remote_file, username, password):
    import paramiko
    stdout = ""
    local_files = glob.glob(local_path)
    try:
        transport = paramiko.Transport((host, 22))
        transport.connect(username=username, password=password)
        for local_file in local_files:
            filename = os.path.basename(local_file)
            if remote_file.endswith("/") or len(local_files) > 1:
                remote_path = os.path.join(remote_file, filename)
            else:
                remote_path = remote_file
            print("executing: scp {} {}:{}".format(
                local_file, host, remote_path))
            sftp = paramiko.SFTPClient.from_transport(transport)
            out = sftp.put(local_file, remote_path)
            if out is not None:
                stdout += str(out) + "\n"
            sftp.close()
        transport.close()
    except Exception as err:
        print("Scp failed with error: {}".format(err))
        return stdout, err
    return stdout, None

def scp(local_file, host, remote_file, username, options):
    cmd = "scp -r {} {} {}@{}:{}".format(
        options,
        local_file,
        username,
        host,
        remote_file)
    print("executing scp: {}".format(cmd))
    return_value, out, err = execute_command(cmd)
    if return_value == 0:
        return out, None
    else:
        return out, err


def ssh(host, command, username, ignore_return=False, options=""):
    cmd = "ssh {} {}@{} \"{}\"".format(
        options, username, host, command)
    print("executing ssh: {}".format(cmd))
    return_value, out, err = execute_command(cmd)
    if return_value == 0 or ignore_return:
        return out, None
    else:
        return out, err


def ssh_thirdparty(host, command, username, password):
    import paramiko
    stdout = ""
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=username, password=password)

        print("executing ssh: {}".format(command))

        _, stdout, stderr = ssh.exec_command(command)
        ssh.close()
    except Exception as err:
        print("Ssh failed with error: {} {}".format(err, stderr))
        return stdout, err
    return stdout, None