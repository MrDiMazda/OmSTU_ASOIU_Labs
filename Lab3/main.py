from flask import Flask, render_template, request
import os

app = Flask(__name__,template_folder='templates')


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/', methods=['post', 'get'])
def form():
    if request.method == 'POST':
        deposit = int(request.form.get('deposit'))
        rate = int(request.form.get('rate'))
        time = int(request.form.get('yeartime'))
    return render_template('index.html', ans=deposit * (1 + rate/100) ** time)


if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)