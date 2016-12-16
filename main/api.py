# *-* coding:utf-8 *-*
'''
@author: ioiogoo
@date: 2016/12/14 14:31
'''
from flask_restful import Resource, reqparse
import requests

str, unicode = unicode, str
urls = {
    'getOtherAttr': 'http://192.168.88.3:1024/kggraph/api/synonymAttribute?attribute=%(bestAttr)s&domain=%(domain)s',
    'getBestAttr': 'http://192.168.88.3:1024/kggraph/api/domainProperty?orderby=optime&count=%(count)d&domain=%(domain)s&offset=%(offset)d',
    'addOtherAttr': 'http://192.168.88.3:1024/kggraph/api/addSynonymAttribute?attribute=%(otherAttr)s&domain=%(domain)s&formalAttribute=%(fromAttr)s',
    'delOtherAttr': 'http://192.168.88.3:1024/kggraph/api/deleteSynonymAttribute?attribute=%(otherAttr)s&domain=%(domain)s',
    'delBestAttr': 'http://192.168.88.3:1024/kggraph/api/deleteFormalAttribute?attribute=%(bestAttr)s&domain=%(domain)s'
}

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

    def get(self):
        args = self.getAttributeParse.parse_args()
        # 查询最优属性
        if args['type'] == 0:
            pn = args['pn'] if args['pn'] else 1
            rn = args['rn'] if args['rn'] else 5
            offset = (pn - 1) * rn
            data = requests.get(urls['getBestAttr'] % {'domain': args['domain'], 'count': rn, 'offset': offset}).json()
            data['message'] = 'success'
            return data

        # 查询同义属性
        elif args['type'] == 1:
            data = requests.get(urls['getOtherAttr'] % args).json()
            data['message'] = 'success'
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

    def post(self):
        args = self.parse.parse_args()
        if args['type'] == 0:
            data = requests.get(urls['delBestAttr']%args).json()
            data['message'] = 'success'
            return data

        elif args['type'] == 1:
            data = requests.get(urls['delOtherAttr']%args).json()
            data['message'] = 'success'
            return data

    # def delBestAttr(self, bestAttr, domain):
    #     '''删除最优属性下全部同义属性'''
    #     result = requests.get(urls['getOtherAttr'] % {'bestAttr': bestAttr, 'domain': domain}).json()
    #     if result['status'] != 0:
    #         result['message'] = 'error'
    #         return result
    #     data = result['data']
    #     for each in data:
    #         result = requests.get(urls['delOtherAttr'] % {'otherAttr': each, 'domain':domain}).json()
    #         if result['status'] !=0:
    #             result['message'] = 'error'
    #             return result
    #     result['message'] = 'success'
    #     return result




class addAttribute(Resource):
    '''增加属性'''

    def __init__(self):
        super(addAttribute, self).__init__()
        self.parse = reqparse.RequestParser()
        self.parse.add_argument('domain', type=str, required=True, location='form')
        self.parse.add_argument('otherAttr', type=str, required=True, location='form')
        self.parse.add_argument('fromAttr', type=str, required=True, location='form')

    def post(self):
        args = self.parse.parse_args()
        data = requests.get(urls['addOtherAttr'] % args).json()
        data['message'] = 'success'
        return data
