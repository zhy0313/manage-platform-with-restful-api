# *-* coding:utf-8 *-*
'''
@author: ioiogoo
@date: 2016/12/19 11:27
'''
import logging
import os

if not os.path.exists('logs'):
    os.mkdir('logs')

logger = logging.getLogger('access_log')


sh = logging.StreamHandler()
fh = logging.FileHandler('logs/access.log')
fh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.setLevel(logging.DEBUG)
logger.addHandler(fh)
logger.addHandler(sh)