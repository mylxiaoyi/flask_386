from flask import Flask, render_template, request, url_for, redirect
from werkzeug.utils import secure_filename
import sqlite3
import os
import math

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.context_processor
def utility_processor():
    return dict(ceil=math.ceil, len=len)

@app.route('/')
def index():
    return render_template('department/index.html')

@app.route('/departments')
def departments_list():
    data = get_departments_list()
    return render_template('department/list.html', departments=data, menu_flag = 'department')

@app.route('/departments/add')
def departments_add():
    return render_template('department/add.html', menu_flag = 'department')

@app.route('/departments/edit')
def departments_edit():
    return render_template('department/edit.html', menu_flag = 'department')

@app.route('/departments/save', methods=['POST'])
def departments_save():
    if request.method == 'POST':
        data = {}
        data['department_id'] = None
        try:
            data['department_id'] = int(request.form['department_id'])
        except KeyError:
            pass
        data['name'] = request.form['name']
        data['headofdepartment'] = request.form['headofdepartment']
        data['address'] = request.form['address']
        data['phone'] = request.form['phone']
        data['noofstudent'] = request.form['noofstudent']
        data['status'] = request.form['status']
        
        if data['department_id'] is None:
            do_departments_save(data)
        else:
            do_departments_update(data)

        return redirect(url_for('departments_list'))

@app.route('/departments/update/<int:department_id>')
def departments_update(department_id):
    data = get_department_by_id(department_id)
    return render_template('department/edit.html', data = data, menu_flag = 'department')

@app.route('/departments/delete/<int:department_id>')
def departments_delete(department_id):
    delete_department_by_id(department_id)
    return redirect(url_for('departments_list'))

def do_departments_save(data):
    db = sqlite3.connect('hello.db')
    cur = db.cursor()
    cur.execute('insert into departments(name, head, address, phone, noofstudent, status) values( "{}", "{}", "{}", "{}", {}, "{}")'.format(data["name"], data["headofdepartment"], data["address"], data["phone"], data["noofstudent"], data["status"]))
    db.commit()
    db.close()

def do_departments_update(data):
    db = sqlite3.connect('hello.db')
    cur = db.cursor()
    cur.execute('update departments set name = "{}", head = "{}", address = "{}", phone = "{}", noofstudent = {}, status = "{}" where id = {}'.format(data['name'], data['headofdepartment'], data['address'], data['phone'], data['noofstudent'], data['status'], data['department_id']))
    db.commit()
    db.close()

def get_departments_list():
    db = sqlite3.connect('hello.db')
    cur = db.cursor()
    cur.execute('select * from departments as d order by d.id')
    data = cur.fetchall()
    db.close()
    return data

def get_department_by_id(department_id):
    db = sqlite3.connect('hello.db')
    cur = db.cursor()
    cur.execute('select * from departments where id={}'.format(department_id))
    data = cur.fetchall()
    db.close()
    return data[0]

def delete_department_by_id(department_id):
    db = sqlite3.connect('hello.db')
    cur = db.cursor()
    cur.execute('delete from departments where id={}'.format(department_id))
    db.commit()
    db.close()

@app.route('/courses')
def courses_list():
    data = get_courses_list()
    return render_template('course/list.html', courses = data, menu_flag = 'course')

@app.route('/courses/add')
def courses_add():
    return render_template('course/add.html', menu_flag = 'course')

@app.route('/courses/update/<int:course_id>')
def courses_update(course_id):
    data = get_course_by_id(course_id)
    return render_template('course/edit.html', course = data, menu_flag = 'course')

@app.route('/courses/delete/<int:course_id>')
def courses_delete(course_id):
    delete_course_by_id(course_id)
    return redirect(url_for('courses_list'))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/courses/save', methods=['POST'])
def courses_save():
    if request.method == 'POST':
        data = {}
        file = request.files['file[0]']
        print(type(file))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        data['course_image'] = filename
        data['course_id'] = None
        try:
            data['course_id'] = request.form['course_id']
        except KeyError:
            pass
        data['course_name'] = request.form['coursename']
        data['course_description'] = request.form['description']

        if data['course_id'] is None:
            do_courses_save(data)
        else:
            do_courses_update(data)

        return redirect(url_for('courses_list'))

def get_courses_list():
    db = sqlite3.connect('hello.db')
    cur = db.cursor()
    cur.execute('select * from courses')
    data = cur.fetchall()
    db.close()
    return data

def do_courses_save(data):
    db = sqlite3.connect('hello.db')
    cur = db.cursor()
    cur.execute('insert into courses(name, image, description) values("{}", "{}", "{}")'.format(data['course_name'], data['course_image'], data['course_description']))
    db.commit()
    db.close()

def do_courses_update(data):
    db = sqlite3.connect('hello.db')
    cur = db.cursor()
    sql = 'update courses set name="{}", image="{}", description="{}" where id={}'.format(data['course_name'], data['course_image'], data['course_description'], data['course_id'])
    cur.execute(sql)
    db.commit()
    db.close()

def get_course_by_id(course_id):
    db = sqlite3.connect('hello.db')
    cur = db.cursor()
    sql = 'select * from courses where id={}'.format(course_id)
    cur.execute(sql)
    data = cur.fetchall()
    db.close()
    return data[0]

def delete_course_by_id(course_id):
    db = sqlite3.connect('hello.db')
    cur = db.cursor()
    sql = 'delete from courses where id={}'.format(course_id)
    cur.execute(sql)
    db.commit()
    db.close()

@app.route('/events')
def events_list():
    return render_template('event/list.html', menu_flag = 'event')

@app.route('/events/add')
def events_add():
    return render_template('events/add.html', menu_flag = 'event')

if __name__ == '__main__':
    app.run(debug=True)
