from subprocess import Popen, PIPE
import os
import sys


def execute_command(cmd, log=True, env=None):
    print("Executing: {}".format(cmd))
    all_env = os.environ.copy()
    if env is not None:
        all_env.update(env)
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True, env=all_env)
    out, err = proc.communicate()
    exitcode = proc.returncode
    if log:
        print("command '{}' exited with {}: {} {}".format(
            cmd, str(exitcode), out, err))
    return exitcode, out, err


def execute_as_user(command, user, log=True):
    pargs = ["sudo", "-i", "-u", user] + command.split(" ")
    print("Executing: " + " ".join(pargs))
    proc = Popen(
        args=pargs,
        stdout=PIPE,
        stderr=PIPE)
    (outdata, errdata) = proc.communicate()
    if log:
        print("RetCode: " + str(proc.returncode))
        print("output: " + outdata)
        print("error(s): " + errdata)
    return proc.returncode, outdata, errdata


def exit_with_code(code):
    if code != 0:
        print("Exiting.")
    sys.exit(code)


def check_root():
    if not os.geteuid() == 0:
        print("User doesn't have root privileges")
        return False
    else:
        print("User is root")
        return True