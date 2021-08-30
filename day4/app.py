from flask import Flask,render_template,flash

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z*^#/'  # secret_key

@app.route('/index') # 路由
def index(): # 视图函数
    flash('这是flash:闪现一个消息')  # 消息闪现
    return render_template('index.html')  # 渲染模板
