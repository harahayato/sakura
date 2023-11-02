from flask import Flask, render_template, session, redirect, jsonify, request, url_for
from kokuhaku import calculate_kokuhaku
import os
import line_read

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
        file = os.path.abspath(form.line_file.data)
        session['line_file'] = file
        session['your_name'] = form.your_name.data
        session['partner_name'] = form.partner_name.data 
        return redirect(url_for('result'))
    #GET
    if 'line_file' in session:
        form.line_file = session['line_file']
        form.your_name = session['your_name']  
        form.partner_name = session['partner_name']
    return render_template('text_form.html', form = form)

@app.route('/result')
def result():
    line_file = session['line_file'] 
    your_name = session['your_name']
    partner_name = session['partner_name']
    line_file_after = line_read.translate_line(line_file)
    line_file_pick = line_read.pick_linelog('log.tsv', partner_name)
    negaposi_late = calculate_kokuhaku.calculate_negaposi(line_file_pick)
    kokuhaku_late = calculate_kokuhaku.calculate_kokuhaku_late(negaposi_late)
    kokuhaku_advice = calculate_kokuhaku.kokuhaku_advice(kokuhaku_late)
    your_replay_speed = line_read.calculate_your_replay_speed('log.tsv', your_name)
    partner_replay_speed = line_read.calculate_partner_replay_speed('log.tsv', partner_name)
    replay_advice = calculate_kokuhaku.replay_advice(your_replay_speed, partner_replay_speed, partner_name)
    return render_template('result.html', kokuhaku_late = kokuhaku_late, kokuhaku_advice = kokuhaku_advice, replay_advice = replay_advice, negaposi_late = negaposi_late)

if __name__ == '__main__':
    app.run()