from flask import Flask,render_template,flash

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/index')
def index():
    flash('这是flash:闪现一个消息')
    return render_template('index.html')
