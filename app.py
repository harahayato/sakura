from flask import Flask, render_template, session, redirect, jsonify, request, url_for
from kokuhaku import calculate_kokuhaku
import io
import os
import json

app = Flask(__name__)

import os
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

from forms import InputForm

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/form', methods = ['GET', 'POST'])
def text_form():
    form = InputForm()
    #POST
    if form.validate_on_submit():
        session['line_file'] = form.line_file.data
        session['your_name'] = form.your_name.data
        session['partner_name'] = form.partner_name.data 
        return redirect(url_for('loading'))
    #GET
    if 'line_file' in session:
        form.line_file = session['line_file']
        form.your_name = session['your_name']  
        form.partner_name = session['partner_name']
    return render_template('text_form.html', form = form)

@app.route('/loading', methods = ['GET', 'POST'])
def loading():
    line_file = session['line_file'] 
    line_file_after = calculate_kokuhaku.change_line_file(line_file)
    negaposi_late = calculate_kokuhaku.calculate_negaposi(line_file_after)
    kokuhaku_late = calculate_kokuhaku.calculate_kokuhaku_late(negaposi_late)
    

    # 結果を表示するテンプレートにリダイレクト
    return render_template('loading.html', result = kokuhaku_late)

@app.route('/result')
def result():
    return render_template('result.html')

if __name__ == '__main__':
    app.run()