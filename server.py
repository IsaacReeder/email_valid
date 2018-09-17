from flask import Flask, request, render_template, redirect, session, flash, url_for
# import the function connectToMySQL from the file mysqlconnection.py
from mysqlconnection import connectToMySQL
mysql = connectToMySQL("email_validation") #
import re
from datetime import datetime, date, time
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
passwordRegex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$')

app = Flask(__name__)
app.secret_key = 'ThisIsSecret'

# invoke the connectToMySQL function and pass it the name of the database we're using
# connectToMySQL returns an instance of MySQLConnection, which we will store in the variable 'mysql'


@app.route('/', methods=['GET'])
def index():
    
    return render_template('index.html')
    


@app.route('/check', methods=['POST'])
def check():
    if len(request.form['email']) < 1:
        flash('Email cannot be blank!')
    elif not EMAIL_REGEX.match(request.form['email']):
        flash('Email is invalid!')
    else:
        query = ("INSERT INTO emails (email, dateadded) " +
                 "VALUES (:email, NOW(), NOW())"
                )
        data = {
            'email' : request.form['email']
        }
        mysql.query_db(query, data) #We put this beacause it opens the db and takes the info and closes it each time.
        
        session['email'] = request.form['email']
        return redirect('/success')
    return redirect('/')


@app.route('/success', methods=['GET'])
def success():
    query = ('SELECT emails.id, emails.email, emails.dateadded FROM emails')
   
    
    emails = mysql.query_db(query)
    
    return render_template('success.html', emails=emails)









app.run(debug=True)
