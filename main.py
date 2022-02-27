
from unittest import result
from flask import Flask, render_template, request

# For DATABASE
from flask_mysqldb import MySQL

app = Flask(__name__)

#Database settings for mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_travelapp'

mysql = MySQL(app)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/doLogin', methods=['POST'])
def doLogin():
    email = request.form['email']
    password = request.form['psw']

    cursor = mysql.connection.cursor()
    resp = cursor.execute(''' SELECT * FROM users WHERE email = %s and password = %s;''',(email, password))

    user = cursor.fetchone()
    cursor.close()
    if resp == 1:
            return render_template('home.html', result= user)
    else:
        return render_template('login.html', result="Invalid Credentials :(")

@app.route('/doRegister', methods=['POST'])
def doRegister():
    full_name = request.form['full_name']
    address = request.form['address']
    email = request.form['email']
    phone_number = request.form['phone_number']
    password = request.form['psw']

    cursor = mysql.connection.cursor()
    cursor.execute('''INSERT INTO users VALUE (NULL, %s, %s, %s, %s, %s);''', (full_name, email, phone_number, address, password))
    mysql.connection.commit()
    cursor.close()

    return render_template('login.html', result = "Registered Successfully! Please login to continue...")

@app.route('/treks')
def allTreks():
    cursor = mysql.connection.cursor()
    cursor.execute(''' SELECT td.id as 'SNO', td.title as 'Title', td.days as 'Days', td.difficulty as 'Difficulty', td.total_cost as 'Total Cost', td.upvotes as 'Upvotes', u.full_name as 'Full Name' FROM `trek_destinations` as td join `users` as u on td.user_id = u.id; ''')
    treks = cursor.fetchall()
    print(treks)
    cursor.close()

    return render_template('listing.html', result = treks)
    

app.run()