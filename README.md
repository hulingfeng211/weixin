# 项目说明
 1.为了使tornado template兼容angularjs的模型双向绑定，修改了tornaod template的源码。
      默认情况下在tornado template中{{title}}，表示在编译模版生成python源码时会在服务器端进行模版内容的绑定。而在angularjs
   中则表示该位置与某个模型绑定。
   
   tornado版本4.2.1
   
   文件：template.py
   
   修改位置：
   
     731行              if reader[curly + 1] not in ("{", "%", "#"): 修改为：            if reader[curly + 1] not in ("@", "%", "#"):
   
     752行              if start_brace == "{{":  修改为：   if start_brace == "{@":
   
     753行              end = reader.find("}}")   修改为：  end = reader.find("@}")
   
# cookie_secret 的生成方法
     base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)

# 安装说明
     
     pip install -r requests.txt #安装依赖的组件