# 常用脚本

## MYSQL dump/restore

1. 修改数据库配置信息

   ```python
   # dump 数据库信息
   FROM_USER = "root"
   FROM_PASSWD = ""
   FROM_DBNAME = "pdb"
   FROM_HOST = "106.14.116.170" 
   FROM_PORT = "3307"
   # dump 文件目录
   BACKUP_PATH = "/tmp/SQL"
   # restore 数据库信息
   TARGET_USER = "root"
   TARGET_PASSWD = "root"
   TARGET_DBNAME = "pdb"
   TARGET_PORT = "3306"
   ```

2. 执行文件

   ```shell
   python3 mysql_dump_restore.py
   ```

      

