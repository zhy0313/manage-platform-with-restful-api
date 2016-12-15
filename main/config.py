# *-* coding:utf-8 *-*
'''
@author: ioiogoo
@date: 2016/12/14 14:39
'''
class Config:
    """docstring for Config"""
    SECRET_KEY = 'asdjoicyhvmnrfgoipbvc'

class productConfig(Config):
    DEBUG = False
    DATABASE = {
        'name': 'lagou',
        'engine': 'peewee.MySQLDatabase',
        'user': 'root',
        'passwd': 'qwer'
    }

class defaultConfig(Config):
    DEBUG = True



config = {
    'productConfig': productConfig,
    'defaultConfig': defaultConfig
}