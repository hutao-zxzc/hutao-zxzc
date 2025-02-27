from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)

# 数据文件路径
PASSAGES_FILE = os.path.join('data', 'passages.json')
USERS_FILE = os.path.join('data', 'users.json')
FILL_BLANKS_FILE = os.path.join('data', 'fill_blanks.json')

# 加载数据
def load_data(file):
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# 保存数据
def save_data(file, data):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 首页
@app.route('/')
def index():
    return render_template('index.html')

# 用户信息输入页面
@app.route('/user_info', methods=['GET', 'POST'])
def user_info():
    if request.method == 'POST':
        username = request.form['username']
        classname = request.form['classname']
        return redirect(url_for('select_mode', username=username, classname=classname))
    return render_template('user_info.html')

# 选择游戏模式页面
@app.route('/select_mode')
def select_mode():
    username = request.args.get('username')
    classname = request.args.get('classname')
    return render_template('select_mode.html', username=username, classname=classname)

# 默写测试页面
@app.route('/quiz')
def quiz():
    username = request.args.get('username')
    classname = request.args.get('classname')
    passages = load_data(PASSAGES_FILE)
    return render_template('quiz.html', passages=passages, username=username, classname=classname)

# 选字填空页面
@app.route('/fill_blanks')
def fill_blanks():
    username = request.args.get('username')
    classname = request.args.get('classname')
    questions = load_data(FILL_BLANKS_FILE)
    return render_template('fill_blanks.html', questions=questions, username=username, classname=classname)

# 提交答案（默写模式）
@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    user_answers = request.json.get('answers')
    username = request.json.get('username')
    classname = request.json.get('classname')
    passages = load_data(PASSAGES_FILE)
    results = []
    total_score = 0

    for i, passage in enumerate(passages):
        correct_answer = passage['content']
        user_answer = user_answers.get(str(i), '')
        score = 1 if user_answer == correct_answer else 0
        results.append({
            'passage_title': passage['title'],
            'correct_answer': correct_answer,
            'user_answer': user_answer,
            'score': score
        })
        total_score += score

    # 保存用户信息和分数
    user_data = {
        'username': username,
        'classname': classname,
        'score': total_score,
        'mode': '默写'
    }
    users = load_data(USERS_FILE)
    users.append(user_data)
    save_data(USERS_FILE, users)

    return jsonify({
        'results': results,
        'total_score': total_score
    })

# 提交答案（选字填空模式）
@app.route('/submit_fill_blanks', methods=['POST'])
def submit_fill_blanks():
    user_answers = request.json.get('answers')
    username = request.json.get('username')
    classname = request.json.get('classname')
    questions = load_data(FILL_BLANKS_FILE)
    results = []
    total_score = 0

    for i, question in enumerate(questions):
        correct_answer = question['correct_answer']
        user_answer = user_answers.get(str(i), '')
        score = 1 if user_answer == correct_answer else 0
        results.append({
            'question': question['question'],
            'correct_answer': correct_answer,
            'user_answer': user_answer,
            'score': score
        })
        total_score += score

    # 保存用户信息和分数
    user_data = {
        'username': username,
        'classname': classname,
        'score': total_score,
        'mode': '选字填空'
    }
    users = load_data(USERS_FILE)
    users.append(user_data)
    save_data(USERS_FILE, users)

    return jsonify({
        'results': results,
        'total_score': total_score
    })

if __name__ == '__main__':
    app.run(debug=True)