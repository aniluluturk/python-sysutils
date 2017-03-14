import platform
from misc import *

WARN = "Warning: Your OS ({}) may not be supported by this tool"


def get_platform():
    global WARN
    osinfo = [x.lower() for x in platform.linux_distribution()]
    if osinfo is None or osinfo == []:
        print("Error while retrieving platform info")
        return None
    elif osinfo[0] == "":
        if platform.system().lower() == "darwin":
            return "Mac"
    elif "red hat" in osinfo[0]:
        return "RedHat"
    elif "cent os" in osinfo[0] or "centos" in osinfo[0]:
        return "CentOs"
    elif "suse" in osinfo[0]:
        return "Suse/OpenSuse"
    elif "ubuntu" in osinfo[0] or "mint" in osinfo[0] or "debian" in osinfo[0]:
        return "Debian"
    print(WARN.format(osinfo))
    return osinfo
