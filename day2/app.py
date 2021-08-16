from flask import Flask

app = Flask(__name__)

@app.route("/hello")
def hello():
    return 'hello flask  23456'

# html转义的问题：任何时候不要忘了转义用户的输入
# jinja2会自动做这件事
from markupsafe import escape

@app.route('/<name>')
def hello_name(name):
    return f"hello, {escape(name)}!"

@app.route('/user/<username>')
def show_user_profile(username):
    return f'User {escape(username)}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f'POST {post_id}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    return f'subpath {escape(subpath)}'


from flask import url_for

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login2')
def login2():
    return 'login2'

@app.route('/user/<username>')
def profile(username):
    return f'{username} \'s  profile'

# test_request_context()直接在命令行中就执行了。不需要在浏览器中访问
with app.test_request_context():
    print(url_for('index'))
    print(url_for('login2'))
    print(url_for('login2', next='/'))
    print(url_for('profile', username='john doe'))

from flask import request,flash
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        # 接收到数据，先验证合法性，再验证账号密码是否匹配
        if request.form['username'] != 'root' or request.form['password'] != '123456':
            error = 'Invalid username/password'
        else:
            flash('logged!', 'error')
            return redirect(url_for('index'))
            # return 'username and password is correct'
    return render_template('login.html', error=error)

# 渲染模板
from flask import render_template
@app.route('/show/')
@app.route('/show/<name>')
def show_something(name=None):
    return render_template('hello.html', name=name)

# 重定向和错误
from flask import abort,redirect,url_for

@app.route('/index')
def index2():
    return redirect(url_for('login'))

@app.route('/abort_login')
def abort_login():
    abort(404)
    # 下面的代码永远不会执行

# 装饰器errorhandler用于定制出错页面
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

from flask import session
app.secret_key = b'jfdi89XJF*&5JFK'


