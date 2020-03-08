from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '54321'
app.config['MYSQL_DB'] = 'flaskapp'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        # Fetch form data
        try:
            userDetails = request.form
            name = userDetails['name']
            email = userDetails['email']
            cur.execute("INSERT INTO flaskapp(name, email) VALUES(%s, %s)",(name, email))
            mysql.connection.commit()
            cur.close()
            return redirect('/users')
        except:
            cur.execute("CREATE TABLE temperatuire (time VARCHAR(100), temp varchar(20))")
            userDetails = request.form
            name = userDetails['name']
            email = userDetails['email']
            cur.execute("INSERT INTO users(name, email) VALUES(%s, %s)",(name, email))
            mysql.connection.commit()
            cur.close()
            return redirect('/users')
    return render_template('index.html')

@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM users")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('users.html',userDetails=userDetails)

if __name__ == '__main__':
    app.run(debug=True)
