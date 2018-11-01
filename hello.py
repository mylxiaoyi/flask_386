from flask import Flask, render_template, request, url_for, redirect
from werkzeug.utils import secure_filename
import sqlite3
import os
import math
import json

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

@app.route('/events_json')
def events_json():
    start = request.args.get('start')
    end = request.args.get('end')
    data = get_events_between_start_and_end(start, end)
    events = []
    for d in data:
        events.append({'id':d[0], 'title':d[1], 'start':d[2], 'end':d[3]})
    return json.dumps(events)

@app.route('/events_update_json', methods=['POST'])
def events_update_json():
    if request.method == 'POST':
        data = {}
        data['event_id'] = request.form['id']
        data['event_title'] = request.form['title']
        data['event_starttime'] = request.form['start']
        data['event_endtime'] = request.form['end']
        do_events_update(data)
        return 'success'

@app.route('/events/add')
def events_add():
    return render_template('event/add.html', menu_flag = 'event')

@app.route('/events/save', methods=['POST'])
def events_save():
    if request.method == 'POST':
        data = {}
        data['event_id'] = None
        try:
            data['event_id'] = request.form['eventid']
        except KeyError:
            pass
        data['event_title'] = request.form['eventtitle']
        data['event_starttime'] = request.form['starttime']
        data['event_endtime'] = request.form['endtime']

        if data['event_id'] is None:
            do_events_save(data)
        else:
            do_events_update(data)

        return redirect(url_for('events_list'))

@app.route('/events/update/<int:event_id>')
def events_update(event_id):
    data = get_event_by_id(event_id)
    return render_template('event/edit.html', event = data, menu_flag = 'event')

def do_events_save(data):
    db = sqlite3.connect('hello.db')
    cur = db.cursor()
    sql = 'insert into events(title, starttime, endtime) values("{}", "{}", "{}")'.format(data['event_title'], data['event_starttime'], data['event_endtime'])
    cur.execute(sql)
    db.commit()
    db.close()

def do_events_update(data):
    db = sqlite3.connect('hello.db')
    cur = db.cursor()
    sql = 'update events set title="{}", starttime="{}", endtime="{}" where id={}'.format(data['event_title'], data['event_starttime'], data['event_endtime'], data['event_id'])
    cur.execute(sql)
    db.commit()
    db.close()

def get_events_between_start_and_end(start, end):
    db = sqlite3.connect('hello.db')
    cur = db.cursor()
    sql = 'select * from events where starttime >= "{}" and endtime <= "{}"'.format(start, end)
    cur.execute(sql)
    data = cur.fetchall()
    db.close()
    return data

def get_event_by_id(event_id):
    db = sqlite3.connect('hello.db')
    cur = db.cursor()
    sql = 'select * from events where id={}'.format(event_id)
    cur.execute(sql)
    data = cur.fetchall()
    db.close()
    return data[0]

if __name__ == '__main__':
    app.run(debug=True)
