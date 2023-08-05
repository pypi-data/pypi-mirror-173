import os
import subprocess

from ppcmd.common.print import print_cmd_step__


def run__(cmd):
    print_cmd_step__(cmd)
    return os.system(cmd)


def run___(cmd):
    print_cmd_step__(cmd)
    params = cmd.split(" ")
    return str(subprocess.run(params, capture_output=True, check=True).stdout, "utf-8")
