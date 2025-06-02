from flask import Flask, flash, redirect, render_template, request, url_for, session
from config import Config
from flask_mysqldb import MySQL
import MySQLdb.cursors
import MySQLdb.cursors, re, hashlib

class Portal:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = '1234'
        self.app.config.from_object(Config)
        self.mysql = MySQL(self.app)
        self.routes()
        
    def routes(self):
        @self.app.route('/testdb')
        def test_db():
            try:
                if self.con is not None:
                    return "Database connection is successful!"
            except Exception as e:
                return f"Database connection failed: {e}"
                
        @self.app.route('/login',  methods=['GET', 'POST'])
        def login():
            msg = ''
            if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
                username = request.form['username']
                password = request.form['password']
                cursor = self.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM user WHERE username = %s AND password = %s', (username, password,))
                account = cursor.fetchone()
                if account:
                    session['loggedin'] = True
                    session['id'] = account['id']
                    session['username'] = account['username']
                    return redirect(url_for('dashboard'))
                else:
                    msg = 'Incorrect username/password!'
            return render_template('login.html', msg=msg)
        
        @self.app.route('/login/createaccount', methods=['GET', 'POST'])
        def createaccount():
            msg = 'aduh error'
            return render_template('createaccount.html')
        
        @self.app.route('/dashboard')
        def dashboard():
            return render_template('dashboard.html')
    
    def run(self):
        self.app.run(debug=True)
        
if __name__ == '__main__':
    portal = Portal()
    portal.run()