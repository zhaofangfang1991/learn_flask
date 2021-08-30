# flasker是一个包含应用代码和文件的python包

import os
from flask import Flask

# 应用工厂函数，用来装配和应用相关的所有配置、注册和其他设置
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True) # 创建flask实例
    app.config.from_mapping(
        SECRET_KEY='DEV',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    )

    # test_config如果存在，就会替换9-12行的配置，实现测试和开发的配置分离，相互分离
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # 确保实例文件夹存在
    # 这里会创建一个instance文件夹，SQLite数据库文件会保存在里面
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 一个简单的路由
    @app.route('/hello')
    def hello():
        return 'hello, world'

    # 在工厂中导入并调用数据库相关的内容
    from . import db
    db.init_app(app)

    # 蓝图的第二步：在工厂函数中注册蓝图
    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index') # 将项目端点名称index 和 / 相关联

    return app