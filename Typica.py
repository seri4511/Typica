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
app.config['MYSQL_DATABASE_PASSWORD'] = 'seri1005'
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
    print (g.db)

    data = g.db.fetchall()
    print data
    rv = [dict((g.db.description[idx][0], value)
               for idx, value in enumerate(row)) for row in data]
    return (rv[0] if rv else None) if one else rv

@app.before_request
def before_request():
    print ("Start Application")
    db_connect = connect_db()
    db_connect.autocommit(1)

    g.db = db_connect.cursor()
    print type(g.db)


@app.route('/login')
def login():
    return render_template('login_page.html')

@app.route('/login_test',  methods=["POST"])
def login_test():
    if request.method == "POST":
        id = request.form['ID']
        password = request.form['password']

        user = query_db('''select * from User where idStudent = %s''', [id], one=True)
        print user
        print generate_password_hash(password)
        print user['UserPassword']
        if check_password_hash(user['StudentPW'], request.form['password']):

            session['user_id'] = user['idStudent']
            return render_template('main_page.html')
        else:
            error = 'Invalid password'
            return "Error"


    return id + " "  + password




@app.route('/main')
def main():
    return render_template('main_page.html')



@app.route('/total_map')
def total_map():
    return render_template('total_map.html')



@app.route('/find')
def find_password():
    return render_template('find_Password.html')


@app.route('/change_first_pw')
def change_first_pw():
    return render_template('change_FirstPassword.html')


@app.route('/adminstudent')
def adminstudent():
    return render_template('adminStudent.html')

@app.route('/adminfee')
def adminfee():
    return render_template('adminStudentFee.html')



if __name__ == '__main__':
    app.debug = True
    app.run()

