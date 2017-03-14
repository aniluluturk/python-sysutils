import pwd
import grp
import os
from misc import *


def chown_path(path, user, group):
    try:
        uid = pwd.getpwnam(user).pw_uid
        gid = grp.getgrnam(group).gr_gid
        os.chown(path, uid, gid)
    except KeyError as err:
        print("Could not find user or group: {}:{}. {}".format(
            user, group, err))
        return False
    except OSError as err:
        print("Could not set ownership: {}".format(err))
        return False
    return True


def create_file_force(path, permission, owneru=None, ownerg=None):
    try:
        os.remove(path)
        create_file(path, permission, owneru, ownerg)
    except Exception as e:
        print("Could not force-create file: {}".format(str(e)))
        return False
    return True


def create_file(path, permission, owneru=None, ownerg=None):
    try:
        with open(path, "w+") as fh:
            fh.write("")
        os.chmod(path, permission)
        if not owneru is None and not ownerg is None:
            chown_path(path, owneru, ownerg)
    except Exception as e:
        print("Could not create file: {}".format(str(e)))
        return False
    return True


def create_dir(path, permission, owneru=None, ownerg=None):
    original_umask = os.umask(0)
    try:
        os.makedirs(path, permission)
    except Exception as err:
        print("Could not create directory: {}".format(str(err)))
        return False
    if owneru is not None and ownerg is not None:
        try:
            chown_path(path, owneru, ownerg)
            return True
        except OSError as err:
            print("Could not set permissions, file: {} ({}, {}, {}). Error: {}".format(
                             path, permission, owneru, ownerg, err))
            return False
        finally:
            os.umask(original_umask)
    return True


def mask_permission(path, permission):
    try:
        cur_perm = os.stat(path)
    except OSError as err:
        print("File status could not be retrieved: {}".format(err))
        return err
    try:
        os.chmod(path, cur_perm.st_mode | permission)
    except OSError as err:
        return err
    return None