from collections import Mapping
from flask import request,make_response
from flask.json import dumps
from flask.views import MethodView

class RestException(Exception):
    """
    异常基类
    """
    def __init__(self,code,message):
        """
        初始化异常
        Args:
        code(int):http 状态码
        message(str):错误信息
        """
        self.code = code
        self.message = message
        super(RestException,self).__init__()

class RestView(MethodView):
    """
    customer class View
    json serialize , exception handler , decorator support
    """
    content_type = 'application/json;charset=utf-8'
    method_decorators = []

    def handler_error(self,exception):
        """
        handler exception
        """
        data={
        'ok':False,
        'message':exception.message
        }
        result = dumps(data)+'\n'
        resp = make_response(result,exception.code)
        return resp

    def dispatch_request(self,*args,**kwargs):
        """
        rewrite ,support auto serialize data
        """
        #get http request method
        method = getattr(self,request.method.lower(),None)
        if method is None and request.method == 'HEAD':
            method = getattr(self,'get',None)
        assert method is not None,'Unimplemented method %r' % request.method

        #http request method difinite difference decorators
        if isinstance(self.method_decorators,Mapping):
            decorators = self.method_decorators.get(request.method.lower(),[])
        else:
            decorators = self.method_decorators

        for decorator in decorators:
            method = decorator(method)

        try:
            resp = method(*args,**kwargs)
        except RestException as e:
            resp = self.handler_error(e)

        #if result is http response,direct turn back
        if isinstance(resp,Response):
            return resp

        #from response get code,header
        data,code,headers = RestView.unpack(resp)

        #code>400 is error,handler it 
        #return error such as {'name': ['redis server already exist']}
        #change to {'ok': False, 'message': 'redis server already exist'}
        if code>=400 and isinstance(data,dict):
            for key in data:
                if isinstance(data[key],list) and len(data[key])>0:
                    message = data[key][0]
                else:
                    message = data[key]
            data = {'ok':False,'message':message}
        result = dumps(data)+'\n'
        #get http response
        response = make_response(result,code)
        response.headers.extend(headers)
        response.headers['content_type'] = self.content_type
        return response
    @staticmethod
    def unpack(value):
        headers = {}
        if not isinstance(value,tuple):
            return value,200,{}
        if len(value) == 3:
            data,code,headers = value
        elif len(value) == 2:
            data,code = value
        return data,code,headers

