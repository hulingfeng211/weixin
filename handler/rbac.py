# -*- coding:utf-8 -*-
#负责角色、权限的相关管理界面的处理
import json
import logging
from bson.objectid import ObjectId
from tornado.gen import coroutine
from tornado.web import RequestHandler, HTTPError
from core import json_encode, is_json_request, generate_response, clone_dict_without_id, make_password
from handler import CRUDHandler

__author__ = 'george'

class UserHandler(RequestHandler):
    @coroutine
    def get(self, *args, **kwargs):
        user_id=args[0] if len(args)>0 else None
        db=self.settings['db']
        if user_id:
            user =yield db.user.find_one({"_id":ObjectId(user_id)})
            self.write(json_encode(user))
        else:
            users=yield db.user.find({}).to_list(length=None)
            self.write(json_encode(users))
    @coroutine
    def delete(self, *args, **kwargs):
        id = args[0] if len(args) > 0 else None
        if id:
            db = self.settings['db']
            yield db.user.remove({"_id": ObjectId(id)})
    @coroutine
    def post(self, *args, **kwargs):
        if is_json_request(self.request):
            body=json.loads(self.request.body)
        else:
            raise HTTPError(status_code=500,log_message="仅支持Content-type:application/json")

        db=self.settings['db']
        if body.get('_id',None):#update
            user_dict=clone_dict_without_id(body)
            user_dict.pop('password')
            yield db.user.update({"_id":ObjectId(body.get('_id'))},{
                "$set":user_dict
            })
        else:
            body['password']=make_password(body.get('password','111111'))
            yield db.user.insert(body)
        self.write(generate_response(message="保存成功"))
class MenuHandler(RequestHandler):
    def get(self, *args, **kwargs):
        db=self.settings['dbsync']
        def get_node_child(node):
            if not node:
                return
            child_list=db.menu.find({"parent_uid":node.get('uid')})
            node['children']=[]
            node['children']=[get_node_child(item) for item in child_list]
            return node
        if args[0] if len(args)>0 else None and args[0]=='all_leaf':#取所有的叶子节点
            leaf_node=list(db.menu.find({"is_leaf":True}))
            self.write(json_encode(leaf_node))
        else:
            root_node= db.menu.find({"parent_uid":{"$exists":False}})
            result=[get_node_child(itm) for itm  in root_node]
            self.write(json_encode(result))
    def post(self, *args, **kwargs):
        if is_json_request(self.request):
            body=json.loads(self.request.body)
        else:
            raise HTTPError(status_code=500,log_message="仅支持Content-type:application/json")
        db=self.settings['dbsync']
        db.menu.remove({})
        def save_node(item):
            for innerItem in item.get('children',[]):
                save_node(innerItem)
            item['selected']=False
            item['is_leaf']=len(item['children'])==0
            item.pop('children')
            db.menu.insert(item)
        #body is array
        for item in body:
            save_node(item)


route=[
    (r'/rbac/user',UserHandler),
    (r'/rbac/user/(.*)',UserHandler),

    (r'/rbac/menu',MenuHandler),
    (r'/rbac/menu/(.*)',MenuHandler),
    (r'/rbac/role',CRUDHandler,{'cname':'role'}),
    (r'/rbac/role/(.*)',CRUDHandler,{'cname':'role'}),
    (r'/rbac/permission',CRUDHandler,{'cname':'permission'}),
    (r'/rbac/permission/(.*)',CRUDHandler,{'cname':'permission'})

]




