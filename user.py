from misc import *


def user_command(uname, group="test", uid="1001"):
    return "sudo useradd -g {} -u {} {}".format(group, uid, uname)


def create_user(uname, group="test", uid="1001"):
    return_value, out, err = execute_command(user_command(uname, group, uid))
    if return_value != 0:
        print("Error occurred during user creation: {} {} ".format(out, err))
        return False
    else:
        print("Created user {} within group {}".format(uname, group))
        return True


def group_command(group="test", gid="1001"):
    return "sudo groupadd -g {} {}".format(gid, group)


def create_group(group="test", uid="1001"):
    return_value, out, err = execute_command(group_command(group, uid))
    if return_value != 0:
        print("Error occurred during group creation: {} {}".format(out, err))
        return False
    else:
        print("Created group {}".format(group))
        return True