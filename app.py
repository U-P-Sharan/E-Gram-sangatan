from flask import Flask, render_template, url_for, request, jsonify
import sqlite3
import telepot
import time

bot = telepot.Bot('5505770046:AAHZ00lFDyhh9AL_r7XFrzKaqDT2LWp52V4')

connection = sqlite3.connect('user_data.db')
cursor = connection.cursor()

command = """CREATE TABLE IF NOT EXISTS user(name TEXT, password TEXT, mobile TEXT, email TEXT, home TEXT)"""
cursor.execute(command)

command = """CREATE TABLE IF NOT EXISTS pdo(name TEXT, password TEXT, mobile TEXT, email TEXT)"""
cursor.execute(command)

command = """CREATE TABLE IF NOT EXISTS admin(name TEXT, password TEXT)"""
cursor.execute(command)

command = """CREATE TABLE IF NOT EXISTS complaints(name TEXT, subject TEXT)"""
cursor.execute(command)

command = """CREATE TABLE IF NOT EXISTS billing(home TEXT, name TEXT, current TEXT, water TEXT, loan TEXT)"""
cursor.execute(command)

command = """CREATE TABLE IF NOT EXISTS birth(home TEXT, name TEXT, place TEXT, date TEXT)"""
cursor.execute(command)

command = """CREATE TABLE IF NOT EXISTS death(home TEXT, name TEXT, place TEXT, date TEXT)"""
cursor.execute(command)

command = """CREATE TABLE IF NOT EXISTS land(home TEXT, name TEXT, place TEXT, area TEXT)"""
cursor.execute(command)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/adminlog', methods=['GET', 'POST'])
def adminlog():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']

        print(name, password)

        query = "SELECT * FROM admin WHERE name = '"+name+"' AND password= '"+password+"'"
        cursor.execute(query)

        result = cursor.fetchall()

        if result:
            return render_template('adminlog.html')
        else:
            return render_template('index.html', msg='Sorry, Incorrect Credentials Provided,  Try Again')
    return render_template('index.html')

@app.route('/pdolog', methods=['GET', 'POST'])
def pdolog():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']

        query = "SELECT * FROM pdo WHERE name = '"+name+"' AND password= '"+password+"'"
        cursor.execute(query)
        result = cursor.fetchall()

        if result:
            query = "SELECT * FROM complaints"
            cursor.execute(query)
            results = cursor.fetchall()

            query = "SELECT name, mobile, email, home FROM user"
            cursor.execute(query)
            details = cursor.fetchall()

            query = "SELECT * FROM land"
            cursor.execute(query)
            lands = cursor.fetchall()

            query = "SELECT * FROM birth"
            cursor.execute(query)
            births = cursor.fetchall()

            query = "SELECT * FROM death"
            cursor.execute(query)
            deaths = cursor.fetchall()

            query = "SELECT * FROM billing"
            cursor.execute(query)
            billings = cursor.fetchall()

            return render_template('pdolog.html', results=results, details=details, lands=lands, births=births, deaths=deaths, billings=billings)
        else:
            return render_template('index.html', msg='Sorry, Incorrect Credentials Provided,  Try Again')
    return render_template('index.html')

@app.route('/pdoreg', methods=['GET', 'POST'])
def pdoreg():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']
        mobile = request.form['phone']
        email = request.form['email']
        
        print(name, mobile, email, password)
        cursor.execute("INSERT INTO pdo VALUES ('"+name+"', '"+password+"', '"+mobile+"', '"+email+"')")
        connection.commit()

        return render_template('index.html', msg='Successfully Registered')
    
    return render_template('index.html')

@app.route('/userlog', methods=['GET', 'POST'])
def userlog():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']

        query = "SELECT * FROM user WHERE name = '"+name+"' AND password= '"+password+"'"
        cursor.execute(query)

        result = cursor.fetchone()

        if result:
            home = result[-1]
            cursor.execute("SELECT * FROM billing WHERE home = '"+home+"'")
            billing = cursor.fetchall()

            cursor.execute("SELECT * FROM birth WHERE home = '"+home+"'")
            births = cursor.fetchall()
            cursor.execute("SELECT * FROM death WHERE home = '"+home+"'")
            deaths = cursor.fetchall()
            cursor.execute("SELECT * FROM land WHERE home = '"+home+"'")
            land = cursor.fetchall()
            return render_template('userlog.html', billing=billing, births=births, deaths=deaths, land=land)
        else:
            return render_template('index.html', msg='Sorry, Incorrect Credentials Provided,  Try Again')
    return render_template('index.html')

@app.route('/userreg', methods=['GET', 'POST'])
def userreg():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']
        mobile = request.form['phone']
        email = request.form['email']
        home = request.form['home']
        
        print(name, mobile, email, password, home)

        query = "SELECT * FROM user WHERE home = '"+home+"'"
        cursor.execute(query)
        details = cursor.fetchall()
        if details:
            return render_template('index.html', msg='Home no already exists')
        else:
            cursor.execute("INSERT INTO user VALUES ('"+name+"', '"+password+"', '"+mobile+"', '"+email+"', '"+home+"')")
            connection.commit()

            return render_template('index.html', msg='Successfully Registered')
    return render_template('index.html')

@app.route('/billing', methods=['GET', 'POST'])
def billing():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        home = request.form['home']
        name = request.form['name']
        cbill = request.form['cbill']
        wbill = request.form['wbill']
        loan = request.form['loan']
        
        print(home, name, cbill, wbill, loan)
        cursor.execute("INSERT INTO billing VALUES ('"+home+"','"+name+"', '"+cbill+"', '"+wbill+"', '"+loan+"')")
        connection.commit()

        return render_template('adminlog.html', msg='Successfully updated')
    
    return render_template('adminlog.html')

@app.route('/birth', methods=['GET', 'POST'])
def birth():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        home = request.form['home']
        name = request.form['name']
        place = request.form['place']
        date = request.form['date']
        
        print(home, name, place, date)
        cursor.execute("INSERT INTO birth VALUES ('"+home+"','"+name+"', '"+place+"', '"+date+"')")
        connection.commit()

        return render_template('adminlog.html', msg='Successfully updated')
    
    return render_template('adminlog.html')

@app.route('/death', methods=['GET', 'POST'])
def death():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        home = request.form['home']
        name = request.form['name']
        place = request.form['place']
        date = request.form['date']
        
        print(home, name, place, date)
        cursor.execute("INSERT INTO death VALUES ('"+home+"','"+name+"', '"+place+"', '"+date+"')")
        connection.commit()

        return render_template('adminlog.html', msg='Successfully updated')
    
    return render_template('adminlog.html')

@app.route('/land', methods=['GET', 'POST'])
def land():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        home = request.form['home']
        name = request.form['name']
        place = request.form['place']
        area = request.form['land']
        
        print(home, name, place, area)
        cursor.execute("INSERT INTO land VALUES ('"+home+"','"+name+"', '"+place+"', '"+area+"')")
        connection.commit()

        return render_template('adminlog.html', msg='Successfully updated')
    
    return render_template('adminlog.html')

@app.route("/complaint",methods=["POST","GET"])
def complaint():
    if request.method == 'POST':
        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()
        name = request.form["q1"]
        sub = request.form["q2"]
        cursor.execute("insert into complaints values('"+name+"', '"+sub+"')")
        connection.commit()
        return jsonify("complaint submited successfully")
    return jsonify("error")


@app.route('/logout')
def logout():
    return render_template('index.html')

@app.route('/live')
def live():
    return render_template('live.html')

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    time.sleep(10)
    response = bot.getUpdates()
    for message in response:
        content_type = message['message']['chat']['type']
        chat_id = message['message']['chat']['id']
        if content_type == 'private' and 'text' in message['message']:
            text = message['message']['text']
    print(text)
    return text

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
