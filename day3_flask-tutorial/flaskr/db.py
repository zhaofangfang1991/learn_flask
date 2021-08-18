'''
使用数据库的步骤：
1、创建一个数据库的连接
2、通过这个连接，进行数据的操作
3、关闭连接
'''

import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext

# 配置db
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

# 关闭db连接
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

# 初始化db函数，用于运行这个SQL命令
def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# 定义一个名叫 init-db 的flask命令， flask init-db
@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('initialized the database')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command) # 增加一个flask命令

