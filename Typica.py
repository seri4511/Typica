#-*- coding: utf-8 -*-
from flask import Flask, render_template, request, make_response, url_for, session, g, redirect
from flask.ext.mysql import MySQL
from werkzeug.security import check_password_hash, generate_password_hash
import json

# configuration
app = Flask(__name__)
# app.config.from_object(__name__)
# app.config.from_envvar('FLASK EXAMPLE_SETTINGS', silent=True)

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'as147852'
app.config['MYSQL_DATABASE_DB'] = 'typica_db'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)



def connect_db():
    return mysql.connect()


def init_db():
    """Creates the database tables."""
    db = connect_db()

    with app.open_resource('typica_db.sql', mode='r') as f:
        sql_statements = " ".join(f.readlines())
        for sql in sql_statements.split(";"):
            if not sql:
                cursor = db.cursor()
                cursor.execute(sql)
                cursor.close()
    db.close()


def query_db(query, args=(), one=False):
    """Queries the database and returns a list of dictionaries."""
    g.db.execute(query, args)
    print (g.db), "1"

    data = g.db.fetchall()
    print data, "2"
    rv = [dict((g.db.description[idx][0], value)
               for idx, value in enumerate(row)) for row in data]
    return (rv[0] if rv else None) if one else rv

@app.before_request
def before_request():
    print ("Start Application","3")
    db_connect = connect_db()
    db_connect.autocommit(1)

    g.db = db_connect.cursor()
    g.user = None
    print type(g.db), "4"
    if 'idStudent' in session:
        g.user= query_db('select * from Student where idStudent = %s',
                          [session['idStudent']], one=True)



@app.route('/')
@app.route('/login')
def login():
    return render_template('login_page.html')


@app.route('/login_test',  methods=["POST"])
def login_test():
    if request.method == "POST":
        id = request.form['id']
        password = request.form['password']
        user =  query_db('''select * from Student where idStudent = %s''', [id], one=True)
        print password, "0 "
        print id, "print0"
        print user, "1"
        print user['StudentPW'], "3"

        if check_password_hash(user['StudentPW'], request.form['password']):

            session['idStudent'] = user['idStudent']
            print "pasword good"
            return render_template('main_page.html')
        else:
            print "password bad"
            return render_template('login_page.html')
        # if check_password_hash(user['UserPassword'], request.form['password']):
        #
        #           session['user_id'] = user['StudentID']
        #           return redirect(url_for('information'))
        #       else:
        #           error = 'Invalid password'
        #           return render_template('login.html', error=error)


    return "ok"




@app.route('/main')
def main():
    return render_template('main_page.html')

@app.route('/a_map')
def a_map():
    return render_template('A_map.html')


@app.route('/b_map')
def b_map():
    return render_template('B_map.html')

@app.route('/c_map')
def C_map():
    return render_template('C_map.html')


@app.route('/total_map')
def total_map():
    return render_template('total_map.html')

@app.route('/find')
def find_password():
    return render_template('find_Password.html')


@app.route('/change_first_pw', methods=['GET', 'POST'])
def change_first_pw():
    error= None
    if request.method == 'POST':
        if request.form['password'] != request.form['password2']:
            error = 'The two password do not match'
        elif request.form['email'] != request.form['email2']:
            error = 'The two email do not match'
        else:
            return redirect(url_for('main'))
    return render_template('change_FIrstPassword.html')

@app.route('/adminstudent' )
def adminstudent():
    return render_template('adminStudent.html')


@app.route('/adminstudentregister', methods=["POST"])
def insert_new_user():
    if request.method == "POST":
        print "17"
        idd = request.form['id']
        name = request.form['username']
        birth = request.form['birthdate']
        password = generate_password_hash(request.form['birthdate'])
        email = request.form['email']
        print "18"
        g.db.execute('''insert into Student (idStudent, StudentName, StudentBirthDate, StudentPW, StudentEmail) values (%s, %s, %s, %s, %s)''', [idd, name, birth, password, email])
        print "19"
        return render_template('main_page.html')
    print "20"
    return "error"

@app.route('/adminfee')
def adminfee_register():
    return render_template('adminStudentFee.html')



if __name__ == '__main__':
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.debug = True
    app.run()