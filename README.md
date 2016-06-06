# 项目说明
  
# tornado 源码修改说明
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
## pycurl导入错误处理
      运行下面的指令安装pycurl
      yum -y install curl curl-devel 
      pip -y install pycurl 
  安装后，如果提示有下面错误
  
      libcurl line-time ssl backend(nss) is different from comple-time ssql backend(penssl)
  需要进行下面的配置才能正常
  
      pip uninstall pycurl #先卸载
      cat 'export PYCURL_SSL_LIBRARY = nss '>>~/.bash_profile
      source ~/.bash_profile
      pip install pycurl

## git 
###  create a new repository on the command line
  echo "# test" >> README.md
  git init
  git add README.md
  git commit -m "first commit"
  git remote add origin https://github.com/hulingfeng211/weixin.git
  git push -u origin master

### push an existing repository from the command line

  git remote add origin https://github.com/hulingfeng211/weixin.git
  git push -u origin master
  



      
   
   
    
      
      
      
