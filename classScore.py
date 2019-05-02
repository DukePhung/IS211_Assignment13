#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, flash, session, redirect
import sqlite3 as sql

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/addStud')
def addStud():
    return render_template('student.html')

@app.route('/addStudRec', methods=['GET', 'POST'])
def addStudRec():
    if request.method=='POST':
        first_name=request.form['first_name']
        last_name=request.form['last_name']
        with sql.connect('hw13.db') as conn:
            cur = conn.cursor()
            cur.execute("insert into student (First_name, Last_name) Values (?,?)",
                        (first_name, last_name))
            conn.commit()
    return render_template('home.html')

@app.route('/viewStud')
def studList():
    with sql.connect('hw13.db') as conn:
        conn.row_factory = sql.Row
        cur = conn.cursor()
        cur.execute("select * from student")
        rows = cur.fetchall()
        return render_template('studList.html', rows = rows)
    
@app.route('/addQuiz')
def addQuiz():
    return render_template('quiz.html')

@app.route('/addQuizRec', methods=['GET', 'POST'])
def addQuizRec():
    if request.method=='POST':
        name=request.form['name']
        question=request.form['question']
        date = request.form['date']
        with sql.connect('hw13.db') as conn:
            cur = conn.cursor()
            cur.execute("insert into quiz (Name, Questions, Date) values(?,?,?)",
                        (name, question, date))
            conn.commit()
    return render_template('home.html')

@app.route('/viewQuiz')
def quizList():
    with sql.connect('hw13.db') as conn:
        conn.row_factory = sql.Row
        cur = conn.cursor()
        cur.execute("select * from quiz")
        rows = cur.fetchall()
        return render_template('quizList.html', rows = rows)

@app.route('/addScore')
def addScore():
    return render_template('score.html')

@app.route('/addResult', methods=['GET', 'POST'])
def addResult():
    if request.method=='POST':
        student_ID = request.form['student_id']
        quiz_ID = request.form['quiz_id']
        score = request.form['score']
        with sql.connect('hw13.db') as conn:
            cur = conn.cursor()
            cur.execute("insert into score (Student_ID, Quiz_ID, Score) Values (?,?,?)",
                        (student_ID, quiz_ID, score))
            conn.commit()
    return render_template('home.html')

@app.route('/list')
def list():
    with sql.connect('hw13.db') as conn:
        conn.row_factory = sql.Row
        cur = conn.cursor()
        cur.execute("Select st.First_name, st.Last_name, q.Name, q.Date, sc.Score \
From student as st join score as sc on st.ID=sc.Student_id \
join quiz as q on q.ID=sc.Quiz_ID")
        rows = cur.fetchall()
        return render_template('list.html', rows = rows)

@app.route('/remrecs')
def remrecs():
    with sql.connect("hw13.db") as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM student")
        cur.execute('DELETE FROM quiz')
        cur.execute('delete from score')
        conn.commit()
    return render_template('home.html')

@app.route('/delStud')
def delStud():
    return render_template('removeStudent.html')

@app.route('/delStudRec', methods=['GET', 'POST'])
def delStudRec():
    student_id=request.form['student_ID']
    with sql.connect("hw13.db") as conn:
        cur = conn.cursor()
        cur.execute("delete from student where ID = ?",(student_id,))
        cur.execute('delete from score where Student_ID = ?', (student_id,))
        conn.commit()
    return render_template('home.html')

@app.route('/delQuiz')
def delQuiz():
    return render_template('removeQuiz.html')

@app.route('/delQuizRec', methods=['GET', 'POST'])
def delQuizRec():
    quiz_id=request.form['quiz_ID']
    with sql.connect("hw13.db") as conn:
        cur = conn.cursor()
        cur.execute("delete from quiz where ID = ?",(quiz_id,))
        cur.execute('delete from score where Quiz_ID = ?', (quiz_id,))
        conn.commit()
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)


























    
