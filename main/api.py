# *-* coding:utf-8 *-*
'''
@author: ioiogoo
@date: 2016/12/14 14:31
'''
from flask_restful import Resource, reqparse, request
import requests
import json
from main.log import logger
from flask import abort
from functools import wraps

str, unicode = unicode, str
urls = {
    'getOtherAttr': 'http://192.168.88.3:1024/kggraph/api/synonymAttribute?attribute=%(bestAttr)s&domain=%(domain)s',
    'getBestAttr': 'http://192.168.88.3:1024/kggraph/api/domainProperty?orderby=optime&count=%(count)d&domain=%(domain)s&offset=%(offset)d',
    'addOtherAttr': 'http://192.168.88.3:1024/kggraph/api/addSynonymAttribute?attribute=%(otherAttr)s&domain=%(domain)s&formalAttribute=%(fromAttr)s',
    'delOtherAttr': 'http://192.168.88.3:1024/kggraph/api/deleteSynonymAttribute?attribute=%(otherAttr)s&domain=%(domain)s',
    'delBestAttr': 'http://192.168.88.3:1024/kggraph/api/deleteFormalAttribute?attribute=%(bestAttr)s&domain=%(domain)s'
}
logging_format = 'ip: %(ip)s - url: %(url)s - data: %(data)s'


def handle_error(func):
    @wraps(func)
    def wrapper(*args, **kw):
        try:
            return func(*args, **kw)
        except Exception as e:
            logger.error(logging_format % {'ip': request.remote_addr, 'url': request.url, 'data': e})
            return logging_format % {'ip': request.remote_addr, 'url': request.url, 'data': 'server error'}, 500
    return wrapper




class getAttribute(Resource):
    '''查找属性'''

    def __init__(self):
        super(getAttribute, self).__init__()
        self.getAttributeParse = reqparse.RequestParser()
        self.getAttributeParse.add_argument('domain', type=str, required=False, location='args', default='person')
        self.getAttributeParse.add_argument('bestAttr', type=str, required=False, location='args')
        self.getAttributeParse.add_argument('type', type=int, required=False, location='args', default=0)
        self.getAttributeParse.add_argument('pn', type=int, required=False, location='args')
        self.getAttributeParse.add_argument('rn', type=int, required=False, location='args', default=5)

    @handle_error
    def get(self):
        args = self.getAttributeParse.parse_args()
        # 查询最优属性
        if args['type'] == 0:
            pn = args['pn'] if args['pn'] else 1
            rn = args['rn'] if args['rn'] else 5
            offset = (pn - 1) * rn
            data = requests.get(urls['getBestAttr'] % {'domain': args['domain'], 'count': rn, 'offset': offset}).json()
            data['message'] = 'success'
            logger.info(logging_format % {'ip': request.remote_addr, 'url': request.url, 'data': json.dumps(data)})
            return data

        # 查询同义属性
        elif args['type'] == 1:
            data = requests.get(urls['getOtherAttr'] % args).json()
            data['message'] = 'success'
            logger.info(logging_format % {'ip': request.remote_addr, 'url': request.url, 'data': json.dumps(data)})
            return data


class deleteAttribute(Resource):
    '''删除属性'''

    def __init__(self):
        super(deleteAttribute, self).__init__()
        self.parse = reqparse.RequestParser()
        self.parse.add_argument('domain', type=str, required=True, location='form')
        self.parse.add_argument('otherAttr', type=str, required=False, location='form')
        self.parse.add_argument('type', type=int, required=True, location='form')
        self.parse.add_argument('bestAttr', type=str, required=False, location='form')

    @handle_error
    def post(self):
        args = self.parse.parse_args()
        if args['type'] == 0:
            data = requests.get(urls['delBestAttr'] % args).json()
            data['message'] = 'success'
            logger.info(logging_format % {'ip': request.remote_addr, 'url': request.url, 'data': json.dumps(data)})
            return data

        elif args['type'] == 1:
            data = requests.get(urls['delOtherAttr'] % args).json()
            data['message'] = 'success'
            logger.info(logging_format % {'ip': request.remote_addr, 'url': request.url, 'data': json.dumps(data)})
            return data


class addAttribute(Resource):
    '''增加属性'''

    def __init__(self):
        super(addAttribute, self).__init__()
        self.parse = reqparse.RequestParser()
        self.parse.add_argument('domain', type=str, required=True, location='form')
        self.parse.add_argument('otherAttr', type=str, required=True, location='form')
        self.parse.add_argument('fromAttr', type=str, required=True, location='form')

    @handle_error
    def post(self):
        args = self.parse.parse_args()
        data = requests.get(urls['addOtherAttr'] % args).json()
        data['message'] = 'success'
        logger.info(logging_format % {'ip': request.remote_addr, 'url': request.url, 'data': json.dumps(data)})
        return data
