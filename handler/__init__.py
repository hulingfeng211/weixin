# -*- coding:utf-8 -*-
import json

from bson.objectid import ObjectId
from tornado.gen import coroutine
from tornado.web import RequestHandler, HTTPError

from core import generate_response, is_json_request, bson_encode, clone_dict_without_id

__author__ = 'george'


class CRUDHandler(RequestHandler):
    """针对mongogdb的简单的CRUD操作的RequestHandler的封装"""

    def initialize(self, *args, **kwargs):
        # cname 为对应的mongodb的集合的名字
        if kwargs:
            for key, val in kwargs.items():
                if not hasattr(self, key):
                    setattr(self, key, val)
        super(CRUDHandler,self).initialize()
    @coroutine
    def get(self, *args, **kwargs):

        id = args[0] if len(args) > 0 else None
        if id:
            db = self.settings['db']
            role = yield db[self.cname].find_one({"_id": ObjectId(id)})
            self.write(bson_encode(role))
            return
        # get all role
        db = self.settings['db']
        roles = yield db[self.cname].find({}).to_list(length=None)
        self.write(bson_encode(
            roles))

    @coroutine
    def delete(self, *args, **kwargs):
        id = args[0] if len(args) > 0 else None
        if id:
            db = self.settings['db']
            yield db[self.cname].remove({"_id": ObjectId(id)})

    @coroutine
    def post(self, *args, **kwargs):
        if is_json_request(self.request):
            body = json.loads(self.request.body)
        else:
            raise HTTPError(status_code=500, log_message="仅支持Content-type:application/json")

        db = self.settings['db']
        if body.get('_id', None):  # update
            yield db[self.cname].update({"_id": ObjectId(body.get('_id'))}, {
                "$set": clone_dict_without_id(body)
            })

        else:
            yield db[self.cname].insert(clone_dict_without_id(body))
        self.write(generate_response(message="保存成功"))


def get_user_menu_tree(db):
    def get_node_child(node):
            if not node:
                return
            child_list=db.menu.find({"parent_uid":node.get('uid')})
            node['children']=[]
            node['children']=[get_node_child(item) for item in child_list]
            return node
    root_node= db.menu.find({"parent_uid":{"$exists":False}})
    return [get_node_child(itm) for itm  in root_node]

