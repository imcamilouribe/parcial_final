from flask import Flask, request, render_template, jsonify, url_for, session, g, redirect
import redis, json
#the getparams function will return a datetime object with these parameters '%Y-%m-%d_%H:%M:%S' followed by temperature in the form of a float
from params import getparams, justtime
from flask_redis import FlaskRedis
from flask_mysqldb import MySQL
from flask_mqtt import Mqtt




#weather api http://api.openweathermap.org/data/2.5/weather?id=3687238&appid=9583c3b4fa60a5323f4d1d115a5f2592
#Flask configs
app = Flask(__name__)
mqtt = Mqtt()

redis_host = "localhost"
redis_port = 6379
redis_password = ""

def init_db():
    db = redis.StrictRedis(
        host=DB_HOST,
        port=DB_PORT,
        db=DB_NO)
    return db
db=init_db

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '54321'
app.config['MYSQL_DB'] = 'flaskapp'
mysql = MySQL(app)
r = redis.Redis(host='localhost', port=6379, db=0)

#"Gets the temperature and timestamp of the IOTD in the form of a json"
def jsoniot():
    y= getparams()
    t = justtime()
    x =  ('{ "temperature":"%s", "timestamp":"%s"}') % (y,t)
    j = json.loads((x))
    return (j)

#Adapter to make the json data into variables
def readjson(j, human):
    temp = j["temperature"]
    times = j["timestamp"]
    if human == 0:
        addstuffdb(temp, times, human)
    return(temp, times)

#Here's where the service adds the data to both databases
def addstuffdb(temp, times , human):
    cur = mysql.connection.cursor()

    if human == 1:


        #Adding params to redis
        r.rpush("temperatures",str(temp))
        r.rpush("timestamps",str(times))
        r.rpush("humantime",str(times))
        #r.lrange("list",-1,-1) Prints the last object of the list
        #adding params to mysql
        try:
            time = str(justtime())
            temp = str(getparams())
            humantime = str(justtime())
            cur.execute("INSERT INTO human(time, temp, humantime) VALUES(%s, %s, %s)",(time, temp, humantime))
            mysql.connection.commit()
            cur.close()
        except:
            cur.execute("CREATE TABLE human(time VARCHAR(100), temp varchar(20), humantime varchar(100))")
            time = justtime()
            temp = getparams()
            cur.execute("INSERT INTO human(time, temp, humantime) VALUES(%s, %s)",(time, temp))
            mysql.connection.commit()
            cur.close()
    else:
        #Adding params to redis
        r.rpush("temperatures",str(temp))
        r.rpush("timestamps",str(times))
        #r.lrange("list",-1,-1) Prints the last object of the list
        #adding params to mysql
        try:
            time = str(justtime())
            temp = str(getparams())
            cur.execute("INSERT INTO iot(time, temp) VALUES(%s, %s)",(time, temp))
            mysql.connection.commit()
            cur.close()
        except:
            cur.execute("CREATE TABLE iot(time VARCHAR(100), temp varchar(20))")
            time = justtime()
            temp = getparams()
            cur.execute("INSERT INTO iot(time, temp) VALUES(%s, %s)",(time, temp))
            mysql.connection.commit()
            cur.close()
#routes
@app.route('/index')
def index():
    return (render_template('index.html'))



@app.route("/=<var>", methods=['GET', 'POST'])
def asdf(var):
    if var == 'iot':
        j = jsoniot()
        temp, times =readjson(j,0)
        return(render_template('iot.html', data = temp ))


#This route will show every object added to the db
@app.route("/", methods=['GET', 'POST'])
def writehash():

    if request.method == 'POST':
        j = jsoniot()
        temp, times = readjson(j,0)
        return(render_template('post.html', data= temp))
    elif request.method == 'GET':
        j = jsoniot()
        temp, times = readjson(j,1)
        return render_template('get.html', title= "Show temps", data = temp)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port = 8000)
