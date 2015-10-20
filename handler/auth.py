# -*- coding:utf-8 -*-
import json
import logging

from bson.objectid import ObjectId
from tornado.escape import json_decode
from tornado.gen import coroutine

from tornado.web import RequestHandler, HTTPError

from core import is_json_request, bson_encode
from core.utils import make_password
from handler import get_user_menu_tree

__author__ = 'george'


class LoginHandler(RequestHandler):
    """用户登陆"""

    @coroutine
    def post(self, *args, **kwargs):
        logging.info(self.request.body)
        user = {}
        if is_json_request(self.request):
            user = json_decode(self.request.body)
        logging.info('email:%s' % user.get('token')['principal'])
        logging.info('password:%s' % user.get('token')['credentials'])
        email = user.get('token')['principal']
        password = user.get('token')['credentials']
        db = self.settings['db']
        dbsync = self.settings['dbsync']
        current_user = yield db.user.find_one({"email": email})
        if current_user:
            if make_password(password) == current_user['password']:  # login success

                # 当前登陆用户的角色必须在角色列表中存在
                if current_user.get('selected_roles', None):
                    user_roles = current_user.get('selected_roles')
                    role_id_list = [ObjectId(item.get('_id')) for item in user_roles]
                    roles = yield db.role.find({"_id": {'$in': role_id_list}}).to_list(length=None)
                    if roles and len(roles) > 0:
                        current_user['roles'] = [item.get('name') for item in roles]

                # 当前登陆用户的权限必须在权限列表中存在
                if current_user.get('selected_permissons', None):
                    user_permissions = current_user.get('selected_permissons')
                    permission_id_list = [ObjectId(item.get('_id')) for item in user_permissions]
                    permissions = yield db.permission.find({"_id": {'$in': permission_id_list}}).to_list(length=None)
                    if permissions and len(permissions) > 0:
                        current_user['permissions'] = [item.get('name') for item in permissions]
                menu_tree = []
                # 当前菜单必须在菜单表中存在
                if current_user.get('selected_menus'):
                    user_menu = current_user.get('selected_menus')
                    menu_tree = get_user_menu_tree(dbsync)
                    menu_id_list = [item["_id"] for item in user_menu]
                    # print menu_id_list
                    # 3 level
                    for l1 in menu_tree:  # 1 level
                        for l2 in l1.get('children'):  # 2 level
                            for l3 in l2.get('children'):  # 3 level
                                if l3['_id'] in menu_id_list:
                                    continue
                                else:
                                    # remove item from children list
                                    l2.get('children').remove(l3)

                result = {
                    "info": {
                        "authc": {
                            "principal": {
                                "name": current_user.get('name'),
                                "login": current_user.get('login'),
                                "email": current_user.get('email')
                            },
                            "credentials": {
                                "name": current_user.get('name'),
                                "login": current_user.get('login'),
                                "email": current_user.get('email')
                            },
                            "menu": menu_tree
                        },
                        "authz": {
                            "roles": current_user.get('roles', []),
                            "permissions": current_user.get('permissions', [])
                        }
                    }
                }

                self.write(bson_encode(result))
            else:
                self.write("密码输入错误")
                self.finish()

        else:
            self.write("当前登陆用户不存在")
            self.finish()


class LogoutHandler(RequestHandler):
    """用户登出"""

    @coroutine
    def get(self, *args, **kwargs):
        logging.info(args)
        pass


class SignupHandler(RequestHandler):
    """用户注册"""

    @coroutine
    def post(self, *args, **kwargs):
        logging.info(self.request.body)
        if not is_json_request(self.request):
            raise HTTPError(status_code=500, log_message="目前仅支持application/json的请求")
        body = json.loads(self.request.body)
        db = self.settings['db']
        olduser = yield db.user.find({"name": body.get("name")}).to_list(length=None)
        if olduser and len(olduser) > 0:
            self.write("当前用户%s已经存在" % body.get("name"))
            self.finish()
        else:
            body['password'] = make_password(body.get('password'))
            yield db.user.insert(body)
            self.write(bson_encode({"user": body}))


route = [
    # 用户登陆
    (r'/auth/login', LoginHandler),
    # 用户注册
    (r'/auth/signup', SignupHandler),
    # 用户登出
    (r'/auth/logout', LogoutHandler)
]
