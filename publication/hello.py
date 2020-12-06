from flask import Flask, render_template, request, redirect, url_for, session 
from flask_mysqldb import MySQL 
from flask import jsonify
import MySQLdb.cursors 
import re 
from gevent.pywsgi import WSGIServer

  
app = Flask(__name__,template_folder='template') 

  
app.secret_key = '123456789'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456789'
app.config['MYSQL_DB'] = 'publication3'
  
  
mysql = MySQL(app) 
#home page
@app.route('/') 
def root():
    session['login'] = True
    return render_template("homepage.html")

#login của ban biên tập    
@app.route('/loginBBT', methods =['GET', 'POST']) 
def loginBBT(): 
    msg = '' 
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form  : 
        username = request.form['username'] 
        password = request.form['password'] 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM LOGIN,BANBIENTAP WHERE Users = % s AND Passwords = % s AND LOGIN.MS=BANBIENTAP.MaSoBBT ' , (username, password, )) 
        account = cursor.fetchone() 
        if account: 
            session['loggedinBBT'] = True
            session['MSBBT'] = account['MS']
            session['UsersBBT'] = account['Users'] 
            msg = 'Logged in successfully !'
            return render_template('indexBBT.html', msg = msg) 
        else: 
            msg = 'Incorrect username / password !'
    return render_template('loginBBT.html', msg = msg)

# Trang của ban biên tập
@app.route("/indexBBT") 
def indexBBT(): 
    if 'loggedinBBT' in session:  
        return render_template("indexBBT.html") 
    return redirect(url_for('login'))
#Trang 1 
@app.route("/indexBBT1") 
def indexBBT1(): 
    if 'loggedinBBT' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM BAIBAO') 
        account = cursor.fetchall()
        return render_template("indexBBT1.html",account=account)
    return redirect(url_for('login'))
#Trang 2  
@app.route("/indexBBT2", methods =['GET', 'POST']) 
def indexBBT2(): 
    if 'loggedinBBT' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM BAIBAO')
        account=cursor.fetchall()

        if request.method == 'POST' and 'MSNPB' in request.form and 'TrangThai' in request.form and 'KetQua' in request.form :
            MSNPB = request.form['MSNPB']
            TrangThai = request.form['TrangThai']
            KetQua= request.form['KetQua']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('UPDATE BAIBAO SET MaSoNPB= % s,TrangThai= % s, KetQua=% s WHERE BAIBAO.MaSoBB = "TQ1"',(MSNPB,TrangThai,KetQua))
            mysql.connection.commit()      
        return render_template("indexBBT2.html",account=account)
    return redirect(url_for('login')) 
    

#Login của tác giả
@app.route('/loginTG', methods =['GET', 'POST']) 
def loginTG(): 
    msg = '' 
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form  : 
        username = request.form['username'] 
        password = request.form['password'] 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM LOGIN,TACGIA WHERE Users = % s AND Passwords = % s AND LOGIN.MS=TACGIA.MaSoTG ' , (username, password, )) 
        account = cursor.fetchone() 
        if account: 
            session['loggedinTG'] = True
            session['MSTG'] = account['MS'] 
            session['UsersTG'] = account['Users'] 
            msg = 'Logged in successfully !'
            return render_template('indexTG.html', msg = msg) 
        else: 
            msg = 'Incorrect username / password !'
    return render_template('loginTG.html', msg = msg)

#Trang của tác giả
@app.route("/indexNPB") 
def indexTG(): 
    if 'loggedin' in session:  
        return render_template("indexBBT.html") 
    return redirect(url_for('login')) 

#Login của Người phản biện
@app.route('/loginNPB', methods =['GET', 'POST']) 
def loginNPB(): 
    msg = '' 
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form  : 
        username = request.form['username'] 
        password = request.form['password'] 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM LOGIN,NGUOIPHANBIEN WHERE Users = % s AND Passwords = % s AND LOGIN.MS=NGUOIPHANBIEN.MaSoNPB ' , (username, password, )) 
        account = cursor.fetchone() 
        if account: 
            session['loggedinNPB'] = True
            session['MSNPB'] = account['MS'] 
            session['UsersNPB'] = account['Users'] 
            msg = 'Logged in successfully !'
            return render_template('indexNPB.html', msg = msg) 
        else: 
            msg = 'Incorrect username / password !'
    return render_template('loginNPB.html', msg = msg)

#Trang của người phản biện
@app.route("/indexNPB") 
def indexNPB(): 
    if 'loggedin' in session: 
        return render_template("indexNPB.html") 
    return redirect(url_for('login'))

if __name__ == "__main__": 
    app.run()
     