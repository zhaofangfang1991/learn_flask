import sqlite3
import click
from flask import current_app,g
from flask.cli import with_appcontext

# 将db存在g中，全局都可以通过g来获取到。可以多次使用，不用在同一个请求中每次调用get_db时都创建一个新的连接
# current_app它指向Flask应用。
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row  # 可以通过列名称来操作数据

    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


# 初始化数据库
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# @click.command 定义一个命令： flask init-db
@click.command('init-db')
@with_appcontext
def init_db_command():
    # 清除已存在的数据， 并创建新的表
    init_db()
    click.echo('initialized the database')

# 把应用作为参数，在函数中进行注册
def init_app(app):
    app.teardown_appcontext(close_db) # 告诉 Flask 在返回响应后进行清理的时候调用此函数。
    app.cli.add_command(init_db_command) # 添加一个命令



