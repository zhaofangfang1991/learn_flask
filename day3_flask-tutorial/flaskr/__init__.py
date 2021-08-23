'''
这个文件的作用：
    1、包含应用工厂
    2、告诉python，flaskr是一个包
'''

import os
from flask import Flask

# 这个函数，就是一个应用工厂
def create_app(test_config=None):
    # 创建Flask实例 __name__是当前模块的名称，让应用知道在哪里设置路径
    # instance_relative_config指相对于instance folder的相对路径
    app = Flask(__name__, instance_relative_config=True)
    # 设置应用的缺省配置，app.instance_path在根目录下的instance文件夹下
    app.config.from_mapping(
        SECRET_KEY='dev', # 开发阶段用；发布版本时需要用随机值来替代
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    # test_config为假， 开发环境   和  正式开发环境
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)  # 测试阶段

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'hello, world'

    # 初始化数据库部分
    from . import db
    db.init_app(app)

    # 注册蓝图部分
    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp) # 注册蓝图
    app.add_url_rule('/', endpoint='index')

    return app

