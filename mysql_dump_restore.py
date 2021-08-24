#!/usr/bin/env python3
import sys
import time
import json
import subprocess
import os


FROM_USER = "root"
FROM_PASSWD = ""
FROM_DBNAME = "pdb"
FROM_HOST = "106.14.116.170"
FROM_PORT = "3307"
BACKUP_PATH = "/tmp/SQL"
TARGET_USER = "root"
TARGET_PASSWD = "root"
TARGET_DBNAME = "pdb"
TARGET_PORT = "3306"

def run_cmd_check(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     print('Running (%s)' % cmd)
    out, err = p.communicate()
    if err:
        print(err)
        sys.exit(1)
    if out:
        print(out)
        return out

def sql_dump():
    """sql dump"""
    timeStruct = time.localtime()
    current_date = time.strftime("%Y-%m-%d-%H%M%S",timeStruct)
    if not os.path.exists(BACKUP_PATH):
            run_cmd_check("mkdir -p {}".format(BACKUP_PATH))
    backup_file_name = "{}/{}-{}.sql".format(BACKUP_PATH, FROM_DBNAME, current_date)

    print("\nDump {} {} to {}...".format(FROM_HOST, FROM_DBNAME, backup_file_name))
    dump_cmd = "mysqldump -u{} -p{} {} --host {} --port={} > {}".format(FROM_USER, FROM_PASSWD, FROM_DBNAME, FROM_HOST, FROM_PORT, backup_file_name)

    child = subprocess.Popen(dump_cmd, shell=True)
    while child.poll() is None:
        subprocess.call('echo "#"', shell=True)
        time.sleep(10)

    if child.returncode == 0:
        print('\nmysql dump {} successfully!\n'.format(backup_file_name))
        time.sleep(5)
        return backup_file_name
    else:
        print('\nmysql dump {} fail!\n'.format(backup_file_name))
        sys.exit(1)


def sql_restore(backup_file_name):
    """sql restore"""
    print("Restore {} to {}...".format(backup_file_name, TARGET_DBNAME))
    restore_cmd = "mysql -u{} -p{} {} --port={} < {}".format(TARGET_USER, TARGET_PASSWD, TARGET_DBNAME, TARGET_PORT, backup_file_name)

    child = subprocess.Popen(restore_cmd, shell=True)
    while child.poll() is None:
        subprocess.call('echo "#"', shell=True)
        time.sleep(10)

    if child.returncode == 0:
        print('\nmysql restore {} successfully!\n'.format(backup_file_name))
        time.sleep(5)
        return 0
    else:
        print("\nmysql restore {} fail!\n".format(backup_file_name))
        sys.exit(1)


if __name__ == "__main__":
    backup_file_name = sql_dump()
    sql_restore(backup_file_name)

