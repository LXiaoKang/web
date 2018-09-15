# blog source
在原来环境中，项目根目录下，执行命令收集所有包 

pip freeze > plist.txt 
首先下载一个新虚拟环境，并且创建一个新的虚拟环境

sudo apt-get install python-virtualenv
python -m venv  venv__ [虚拟环境名称]
使用新的虚拟化环境并检查当前的包

source venv/bin/activate
pip list


 

将 你的代码中除了 原虚拟环境之外的代码 拷贝到当前环境下，



安装所需要的包

pip install -r plist.txt
这个plist.txt 是 原来环境的包导出的包的版本号

安装完毕后 查看当前虚拟环境中的 包

pip list



然后就可以执行了

python3 manage.py runserver 8000
然后在网页中输入 127.0.0.0:8000
设置成局域网来访问

python3 manage.py runserver 0.0.0.0:8000
在网页中输入 你的ip和端口号  ××××××:8000
 

关闭虚拟环境

deactivate

 

