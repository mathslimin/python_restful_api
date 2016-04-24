新后台，在原来的基础上修改

现在本地
vim ~/.bash_profile
添加
export PYTHON_ENVIRONMENT='local'
然后
source ~/.bash_profile

表示使用本地环境

添加git submodule

git submodule init
git submodule update

更新请使用
git submodule foreach git pull origin master


python 运行环境配置
先升级pip
pip install -U pip
virtualenv v25
source v25/bin/activate
安装所有的库
sudo apt-get install libffi-dev
pip install -r requirements.txt --trusted-host mirrors.aliyun.com --trusted-host pypi.douban.com


统一格式化代码
yapf -i  --style='{based_on_style: google, indent_width: 4, spaces_before_comment = 4, split_before_logical_operator = true}'  xxx.py

格式化目录
yapf -i -r --style='{based_on_style: google, indent_width: 4, spaces_before_comment = 4, split_before_logical_operator = true}' dir
