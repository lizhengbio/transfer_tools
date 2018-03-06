#coding:utf-8
from peewee import *
db = MySQLDatabase(
    database = 'transfer_log',
    user = 'root',
    passwd = 'aty1rldu',
    host = '192.168.0.117',
    charset = 'utf8'
)

class FileInfo(Model):
    filename = CharField(max_length = 50)
    filepath = CharField(max_length = 50)
    filesize = CharField(max_length =10240)
    action = CharField(max_length = 50)
    time = CharField(max_length = 50)
    class Meta:
        database = db
if __name__ == '__main__':
    FileInfo.create_table()
