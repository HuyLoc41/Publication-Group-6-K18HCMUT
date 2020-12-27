from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from flask import jsonify
import MySQLdb.cursors
import re
from gevent.pywsgi import WSGIServer
from datetime import date

app = Flask(__name__, template_folder='template')


app.secret_key = '123456789'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456789'
app.config['MYSQL_DB'] = 'publication2'


mysql = MySQL(app)
# home page


@app.route('/')
def root():
    session['login'] = True
    return render_template("homepage.html")

# login của ban biên tập


@app.route('/loginBBT', methods=['GET', 'POST'])
def loginBBT():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM LOGIN,BANBIENTAP WHERE Users = % s AND Passwords = % s AND LOGIN.MS=BANBIENTAP.MaSoBBT ', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedinBBT'] = True
            session['MSBBT'] = account['MS']
            session['UsersBBT'] = account['Users']
            msg = 'Logged in successfully !'
            return render_template('indexBBT.html', msg=msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('loginBBT.html', msg=msg)

# Trang của ban biên tập


@app.route("/indexBBT")
def indexBBT():
    if 'loggedinBBT' in session:
        return render_template("indexBBT.html")
    return redirect(url_for('login'))
# Trang 1


@app.route("/indexBBT1")
def indexBBT1():
    if 'loggedinBBT' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM BAIBAO')
        account = cursor.fetchall()
        return render_template("indexBBT1.html", account=account)
    return redirect(url_for('login'))
# Trang 2


@app.route("/indexBBT2", methods=['GET', 'POST'])
def indexBBT2():
    if 'loggedinBBT' in session:

        if request.method == 'POST' and 'MaSoBB' in request.form and 'MSNPB' in request.form and 'TrangThai' in request.form and 'KetQua' in request.form and 'NgayCapNhatKQ' in request.form:
            MSBB = request.form['MaSoBB']
            MSNPB = request.form['MSNPB']
            TrangThai = request.form['TrangThai']
            KetQua = request.form['KetQua']
            NgayCapNhatKQ=request.form['NgayCapNhatKQ']
            if NgayCapNhatKQ=='':
                NgayCapNhatKQ='0000/00/00'
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('UPDATE BAIBAO SET MaSoNPB= % s,TrangThai= % s, KetQua=% s, NgayCapNhatKQ=%s where MaSoBB=% s ',
                           (MSNPB, TrangThai, KetQua,NgayCapNhatKQ, MSBB))
            mysql.connection.commit()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM BAIBAO')
        account = cursor.fetchall()

        return render_template("indexBBT2.html", account=account)
    return redirect(url_for('login'))

# Trang 3


@app.route("/indexBBT3")
def indexBBT3():
    if 'loggedinBBT' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM BAIBAO WHERE SUBSTRING(MaSoBB,1,2)="NC" AND BAIBAO.MaSoNPB=""')
        accountNC = cursor.fetchall()

        cursor.execute(
            'SELECT * FROM BAIBAO WHERE SUBSTRING(MaSoBB,1,2)="TQ" AND BAIBAO.MaSoNPB=""')
        accountTQ = cursor.fetchall()

        cursor.execute(
            'SELECT * FROM BAIBAO WHERE SUBSTRING(MaSoBB,1,2)="PB" AND BAIBAO.MaSoNPB=""')
        accountPB = cursor.fetchall()
        return render_template("indexBBT3.html", accountNC=accountNC, accountTQ=accountTQ, accountPB=accountPB)
    return redirect(url_for('login'))

# Trang 4


@app.route("/indexBBT4")
def indexBBT4():
    if 'loggedinBBT' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM BAIBAO WHERE SUBSTRING(MaSoBB,1,2)="NC" AND BAIBAO.TrangThai="Xuất bản"')
        accountNC1 = cursor.fetchall()

        cursor.execute(
            'SELECT * FROM BAIBAO WHERE SUBSTRING(MaSoBB,1,2)="TQ" AND BAIBAO.TrangThai="Xuất bản"')
        accountTQ1 = cursor.fetchall()

        cursor.execute(
            'SELECT * FROM BAIBAO WHERE SUBSTRING(MaSoBB,1,2)="PB" AND BAIBAO.TrangThai="Xuất bản"')
        accountPB1 = cursor.fetchall()
        return render_template("indexBBT4.html", accountNC1=accountNC1, accountTQ1=accountTQ1, accountPB1=accountPB1)
    return redirect(url_for('login'))

# Trang 5


@app.route("/indexBBT5")
def indexBBT5():
    if 'loggedinBBT' in session:
        today = date.today()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM BAIBAO WHERE SUBSTRING(MaSoBB,1,2)="NC" AND BAIBAO.TrangThai="Đã đăng" AND BAIBAO.NgayGui >  DATE_SUB(% s, INTERVAL 4 YEAR) AND BAIBAO.NgayGui <= % s ;', (today, today))
        accountNC1 = cursor.fetchall()

        cursor.execute(
            'SELECT * FROM BAIBAO WHERE SUBSTRING(MaSoBB,1,2)="TQ" AND BAIBAO.TrangThai="Đã đăng" AND BAIBAO.NgayGui >  DATE_SUB(% s, INTERVAL 4 YEAR) AND BAIBAO.NgayGui <= % s ;', (today, today))
        accountTQ1 = cursor.fetchall()

        cursor.execute(
            'SELECT * FROM BAIBAO WHERE SUBSTRING(MaSoBB,1,2)="PB" AND BAIBAO.TrangThai="đã đăng" AND BAIBAO.NgayGui >  DATE_SUB(% s, INTERVAL 4 YEAR) AND BAIBAO.NgayGui <= % s ;', (today, today))
        accountPB1 = cursor.fetchall()
        return render_template("indexBBT5.html", accountNC1=accountNC1, accountTQ1=accountTQ1, accountPB1=accountPB1)
    return redirect(url_for('login'))

# Trang 6

@app.route("/indexBBT6", methods=['GET', 'POST'])
def indexBBT6():
    if 'loggedinBBT' in session:
        MSBB = ""
        if request.method == 'POST' and 'MaSoTG' in request.form:
            MSBB = request.form['MaSoTG']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM BAIBAO WHERE BAIBAO.TrangThai="Đã đăng" AND BAIBAO.MaSoTG =% s', (MSBB,))
        account12 = cursor.fetchall()
        return render_template("indexBBT6.html", account12=account12)
    return redirect(url_for('login'))
# Trang 7

@app.route("/indexBBT7", methods=['GET', 'POST'])
def indexBBT7():
    if 'loggedinBBT' in session:
        MSBB = ""
        if request.method == 'POST' and 'MaSoTG' in request.form:
            MSBB = request.form['MaSoTG']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM BAIBAO WHERE BAIBAO.TrangThai="Xuất bản" AND BAIBAO.MaSoTG =% s', (MSBB,))
        account12 = cursor.fetchall()
        return render_template("indexBBT7.html", account12=account12)
    return redirect(url_for('login'))
# Trang 8

@app.route("/indexBBT8")
def indexBBT8():
    if 'loggedinBBT' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT COUNT(*) FROM BAIBAO WHERE BAIBAO.TrangThai="Phản biện"')
        accountNC1 = cursor.fetchall()

        cursor.execute(
            'SELECT COUNT(*) FROM BAIBAO WHERE BAIBAO.TrangThai="Phản hồi phản biện"')
        accountTQ1 = cursor.fetchall()

        cursor.execute(
            'SELECT COUNT(*) FROM BAIBAO WHERE BAIBAO.TrangThai="Xuất bản"')
        accountPB1 = cursor.fetchall()

        return render_template("indexBBT8.html", accountNC1=accountNC1, accountTQ1=accountTQ1, accountPB1=accountPB1)
    return redirect(url_for('login'))
    
# Login của Người phản biện

@app.route('/loginNPB', methods=['GET', 'POST'])
def loginNPB():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM LOGIN,NGUOIPHANBIEN WHERE Users = % s AND Passwords = % s AND LOGIN.MS=NGUOIPHANBIEN.MaSoNPB ', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedinNPB'] = True
            session['MSNPB'] = account['MS']
            session['UsersNPB'] = account['Users']
            msg = 'Logged in successfully !'
            return render_template('indexNPB.html', msg=msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('loginNPB.html', msg=msg)

# Trang của người phản biện

@app.route("/indexNPB")
def indexNPB():
    if 'loggedinNPB' in session:
        return render_template("indexNPB.html")
    return redirect(url_for('login'))

# Trang 1 người phản biện: cập nhật thông tin
@app.route("/indexNPB1", methods=['GET', 'POST'])
def indexNPB1():
    msg = '' 
    if 'loggedinNPB' in session: 
        if request.method == 'POST' and 'SDT' in request.form and 'Ten' in request.form and 'KiNang' in request.form and 'ChuyenMon' in request.form and 'CoQuan' in request.form and 'MailCoQuan' in request.form and 'MailCaNhan' in request.form: 
            SDT = request.form['SDT'] 
            Ten = request.form['Ten'] 
            KiNang = request.form['KiNang']   
            ChuyenMon = request.form['ChuyenMon'] 
            CoQuan = request.form['CoQuan'] 
            MailCoQuan = request.form['MailCoQuan']     
            MailCaNhan = request.form['MailCaNhan']  

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('UPDATE NGUOIPHANBIEN SET  Sdt =% s, Ten =% s, KiNang =% s, ChuyenMon =% s, CoQuan =% s, MailCoQuan =% s, MailCaNhan =% s WHERE MaSoNPB =% s ', (SDT,Ten,KiNang,ChuyenMon,CoQuan,MailCoQuan,MailCaNhan, (session['MSNPB'], ), )) 
            mysql.connection.commit()

            msg = 'You have successfully updated !'
        elif request.method == 'POST': 
            msg = 'Please fill out the form !'
        return render_template("indexNPB1.html", msg = msg) 
    return redirect(url_for('loginNPB'))

# Trang 2 người phản biện: cập nhật phản biện
@app.route("/indexNPB2", methods=['GET', 'POST'])
def indexNPB2():
     
    if 'loggedinNPB' in session: 
        if request.method == 'POST' and 'MaSoBB' in request.form and 'Diem' in request.form and 'GhiChuBBT' in request.form and 'GhiChuTG' in request.form:
            MSBB = request.form['MaSoBB']
            Diem = request.form['Diem']
            GhiChuBBT = request.form['GhiChuBBT']
            GhiChuTG = request.form['GhiChuTG']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('UPDATE BAIBAO SET Diem= % s,GhiChuBBT= % s, GhiChuTG=% s where MaSoBB=% s ',
                           (Diem, GhiChuBBT, GhiChuTG, MSBB))
            mysql.connection.commit()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM BAIBAO WHERE BAIBAO.MaSoNPB=%s',((session['MSNPB'], ),))
        account = cursor.fetchall()

        return render_template("indexNPB2.html", account=account)
    return redirect(url_for('loginNPB'))
#Trang 3 người phản biện.    
@app.route("/indexNPB3")
def indexNPB3():
    if 'loggedinNPB' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM BAIBAO WHERE SUBSTRING(MaSoBB,1,2)="NC" AND (BAIBAO.TrangThai="Phản biện" OR BAIBAO.TrangThai="Phản hồi phản biện") and BAIBAO.MaSoNPB=%s',((session['MSNPB'], ),))
        accountNC1 = cursor.fetchall()

        cursor.execute(
            'SELECT * FROM BAIBAO WHERE SUBSTRING(MaSoBB,1,2)="TQ" AND (BAIBAO.TrangThai="Phản biện" OR BAIBAO.TrangThai="Phản hồi phản biện") and BAIBAO.MaSoNPB=%s',((session['MSNPB'], ),))
        accountTQ1 = cursor.fetchall()

        cursor.execute(
            'SELECT * FROM BAIBAO WHERE SUBSTRING(MaSoBB,1,2)="PB" AND (BAIBAO.TrangThai="Phản biện" OR BAIBAO.TrangThai="Phản hồi phản biện") and BAIBAO.MaSoNPB=%s',((session['MSNPB'], ),))
        accountPB1 = cursor.fetchall()

        return render_template("indexNPB3.html", accountNC1=accountNC1, accountTQ1=accountTQ1, accountPB1=accountPB1)
    return redirect(url_for('login'))
#Trang 4 người phản biện.    
@app.route("/indexNPB4")
def indexNPB4():
    today=date.today()
    if 'loggedinNPB' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM BAIBAO WHERE SUBSTRING(MaSoBB,1,2)="NC" AND BAIBAO.KetQua <>"#" AND BAIBAO.KetQua <>"" AND BAIBAO.NgayCapNhatKQ >  DATE_SUB(% s, INTERVAL 4 YEAR) AND BAIBAO.NgayCapNhatKQ <= % s and BAIBAO.MaSoNPB=%s',(today,today,(session['MSNPB'], ),))
        accountNC1 = cursor.fetchall()

        cursor.execute(
            'SELECT * FROM BAIBAO WHERE SUBSTRING(MaSoBB,1,2)="TQ" AND BAIBAO.KetQua <>"#" AND BAIBAO.KetQua <>"" AND BAIBAO.NgayCapNhatKQ >  DATE_SUB(% s, INTERVAL 4 YEAR) AND BAIBAO.NgayCapNhatKQ <= % s  and BAIBAO.MaSoNPB=%s',(today,today,(session['MSNPB'], ),))
        accountTQ1 = cursor.fetchall()

        cursor.execute(
            'SELECT * FROM BAIBAO WHERE SUBSTRING(MaSoBB,1,2)="PB" AND BAIBAO.KetQua <>"#" AND BAIBAO.KetQua <>"" AND BAIBAO.NgayCapNhatKQ >  DATE_SUB(% s, INTERVAL 4 YEAR) AND BAIBAO.NgayCapNhatKQ <= % s  and BAIBAO.MaSoNPB=%s',(today,today,(session['MSNPB'], ),))
        accountPB1 = cursor.fetchall()

        return render_template("indexNPB4.html", accountNC1=accountNC1, accountTQ1=accountTQ1, accountPB1=accountPB1)
    return redirect(url_for('login'))

#Trang 5 người phản biện.    
@app.route("/indexNPB5")
def indexNPB5():
    
    if 'loggedinNPB' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM BAIBAO WHERE BAIBAO.MaSoNPB=%s ',((session['MSNPB'], ),))
        accountNC1 = cursor.fetchall()

        return render_template("indexNPB5.html", accountNC1=accountNC1)
    return redirect(url_for('login'))

#Trang 6 người phản biện.    
@app.route("/indexNPB6")
def indexNPB6():

    today=date.today()
    if 'loggedinNPB' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM BAIBAO WHERE BAIBAO.KetQua <>"#" AND BAIBAO.KetQua <>"" AND BAIBAO.NgayCapNhatKQ >  DATE_SUB(% s, INTERVAL 4 YEAR) AND BAIBAO.NgayCapNhatKQ <= % s and BAIBAO.MaSoNPB=%s ORDER BY MaSoTG',(today,today,(session['MSNPB'], ),))
        accountNC1 = cursor.fetchall()

        return render_template("indexNPB6.html", accountNC1=accountNC1)
    return redirect(url_for('login'))

#Trang 8 người phản biện.    
@app.route("/indexNPB8")
def indexNPB8():

    today=date.today()
    if 'loggedinNPB' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM BAIBAO WHERE BAIBAO.KetQua <>"#" AND BAIBAO.KetQua <>"" AND BAIBAO.NgayCapNhatKQ >  DATE_SUB(% s, INTERVAL 1 YEAR) AND BAIBAO.NgayCapNhatKQ <= % s and BAIBAO.MaSoNPB=%s ORDER BY MaSoTG',(today,today,(session['MSNPB'], ),))
        accountNC1 = cursor.fetchall()

        return render_template("indexNPB8.html", accountNC1=accountNC1)
    return redirect(url_for('login'))

#Trang 9 người phản biện.    
@app.route("/indexNPB9")
def indexNPB9():
    if 'loggedinNPB' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM BAIBAO WHERE BAIBAO.KetQua="acceptance" and MaSoNPB=%s',((session['MSNPB'], ),))
        accountNC1 = cursor.fetchall()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM BAIBAO WHERE BAIBAO.KetQua="rejection" and MaSoNPB=%s',((session['MSNPB'], ),))
        accountNC2 = cursor.fetchall()
        return render_template("indexNPB9.html", accountNC1=accountNC1,accountNC2=accountNC2)
    return redirect(url_for('login'))

#Trang 10 người phản biện.    
@app.route("/indexNPB10")
def indexNPB10():

    if 'loggedinNPB' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT COUNT(*) FROM BAIBAO WHERE NgayCapNhatKQ>="2020-01-01" and NgayCapNhatKQ<"2021-01-01" and MaSoNPB=%s',((session['MSNPB'], ),))
        Nam2020 = cursor.fetchall()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT COUNT(*) FROM BAIBAO WHERE NgayCapNhatKQ>="2020-01-01" and NgayCapNhatKQ<"2021-01-01"' )
        Nam2020all = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT COUNT(*) FROM BAIBAO WHERE NgayCapNhatKQ>="2019-01-01" and NgayCapNhatKQ<"2020-01-01" and MaSoNPB=%s',((session['MSNPB'], ),))
        Nam2019 = cursor.fetchall()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT COUNT(*) FROM BAIBAO WHERE NgayCapNhatKQ>="2019-01-01" and NgayCapNhatKQ<"2020-01-01"' )
        Nam2019all = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT COUNT(*) FROM BAIBAO WHERE NgayCapNhatKQ>="2018-01-01" and NgayCapNhatKQ<"2019-01-01" and MaSoNPB=%s',((session['MSNPB'], ),))
        Nam2018 = cursor.fetchall()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT COUNT(*) FROM BAIBAO WHERE NgayCapNhatKQ>="2018-01-01" and NgayCapNhatKQ<"2019-01-01"' )
        Nam2018all = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT COUNT(*) FROM BAIBAO WHERE NgayCapNhatKQ>="2017-01-01" and NgayCapNhatKQ<"2018-01-01" and MaSoNPB=%s',((session['MSNPB'], ),))
        Nam2017 = cursor.fetchall()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT COUNT(*) FROM BAIBAO WHERE NgayCapNhatKQ>="2017-01-01" and NgayCapNhatKQ<"2018-01-01"' )
        Nam2017all = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT COUNT(*) FROM BAIBAO WHERE NgayCapNhatKQ>="2016-01-01" and NgayCapNhatKQ<"2017-01-01" and MaSoNPB=%s',((session['MSNPB'], ),))
        Nam2016 = cursor.fetchall()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT COUNT(*) FROM BAIBAO WHERE NgayCapNhatKQ>="2016-01-01" and NgayCapNhatKQ<"2017-01-01"' )
        Nam2016all = cursor.fetchall()

        return render_template("indexNPB10.html",Nam2020=Nam2020,Nam2020all=Nam2020all,Nam2019=Nam2019,Nam2019all=Nam2019all,Nam2018=Nam2018,Nam2018all=Nam2018all,Nam2017=Nam2017,Nam2017all=Nam2017all,Nam2016=Nam2016,Nam2016all=Nam2016all)
    return redirect(url_for('login'))

# Login của tác giả
@app.route('/loginTG', methods=['GET', 'POST'])
def loginTG():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM LOGIN,TACGIALL WHERE Users = % s AND Passwords = % s AND LOGIN.MS=TACGIALL.MaSoTGLL ', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedinTG'] = True
            session['MSTGLL'] = account['MS']
            session['UsersTG'] = account['Users']
            msg = 'Logged in successfully !'
            return render_template('indexTG.html', msg=msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('loginTG.html', msg=msg)

# Trang của tác giả
@app.route("/indexNPB")
def indexTG():
    if 'loggedin' in session:
        return render_template("indexBBT.html")
    return redirect(url_for('login'))

# Trang 1 người phản biện: cập nhật thông tin tác giả
@app.route("/indexTG1", methods=['GET', 'POST'])
def indexTG1():
    msg = '' 
    if 'loggedinTG' in session: 
        if request.method == 'POST' and 'CoQuan' in request.form and 'DiaChi' in request.form and 'Mail' in request.form and 'Nghe' in request.form: 
            CoQuan = request.form['CoQuan'] 
            DiaChi = request.form['DiaChi'] 
            Mail = request.form['Mail']   
            Nghe = request.form['Nghe']
            if(CoQuan!='' and DiaChi!='' and Mail !='' and Nghe !=''): 
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('UPDATE TACGIALL SET  CoQuan =% s, DiaChi =% s, Mail =% s, NgheNghiep =% s WHERE MaSoTGLL =% s ', (CoQuan,DiaChi,Mail,Nghe, (session['MSTGLL'], ), )) 
                mysql.connection.commit()
                msg = 'You have successfully updated !'
            else:
                msg = 'Please fill out the form !'
        return render_template("indexTG1.html", msg = msg) 
    return redirect(url_for('loginTG'))

# Trang 2 người phản biện: cập nhật thông tin bài báo chưa được nộp
@app.route("/indexTG2", methods=['GET', 'POST'])
def indexTG2():
    msg = '' 
    if 'loggedinTG' in session: 
        if request.method == 'POST' and 'MaSoBB' in request.form and 'TacGia' in request.form and 'SoTrang' in request.form and 'TieuDe' in request.form and 'Ten' in request.form and 'TomTat' in request.form and 'TuKhoa' in request.form and 'File' in request.form: 
            MaSoBB = request.form['MaSoBB'] 
            TacGia = request.form['TacGia'] 
            SoTrang = request.form['SoTrang']   
            TieuDe = request.form['TieuDe']
            Ten = request.form['Ten']
            TomTat = request.form['TomTat']
            TuKhoa = request.form['TuKhoa']
            File = request.form['File']

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('UPDATE BAIBAO SET MaSoTG =% s, SoTrang =% s, TieuDe =% s, Ten =% s, TomTat=%s,TuKhoa=%s,FileBB=%s WHERE MaSoBB = % s ', (TacGia,SoTrang,TieuDe,Ten,TomTat,TuKhoa,File, MaSoBB))
            mysql.connection.commit()
            msg = 'You have successfully updated !'

        if 'loggedinTG' in session:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM BAIBAO WHERE MaSoNPB=""')
            account = cursor.fetchall()
        return render_template("indexTG2.html", msg = msg,account=account) 
    return redirect(url_for('loginTG'))

#Trang 3 của tác giả liên lạc
@app.route("/indexTG3", methods=['GET', 'POST'])
def indexTG3():
    MaSoBB=''
    if 'loggedinTG' in session: 
        if request.method == 'POST' and 'MaSoBB' in request.form: 
            MaSoBB = request.form['MaSoBB'] 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * from TACGIA where MaSoTG=(SELECT MaSoTG from BAIBAO where MaSoBB=%s)',(MaSoBB,))
        account = cursor.fetchall()
        MS=MaSoBB
        return render_template("indexTG3.html",MS=MS, account=account) 
    return redirect(url_for('loginTG'))

#Trang 4 của tác giả liên lạc
@app.route("/indexTG4", methods=['GET', 'POST'])
def indexTG4():
    MaSoBB=''
    if 'loggedinTG' in session: 
        if request.method == 'POST' and 'MaSoBB' in request.form: 
            MaSoBB = request.form['MaSoBB'] 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * from BAIBAO where MaSoBB=%s',(MaSoBB,))
        account = cursor.fetchall()
        MS=MaSoBB
        return render_template("indexTG4.html",MS=MS, account=account) 
    return redirect(url_for('loginTG'))

#Trang 5 của tác giả liên lạc
@app.route("/indexTG5", methods=['GET', 'POST'])
def indexTG5():
    MaSoBB=''
    if 'loggedinTG' in session: 
        if request.method == 'POST' and 'MaSoBB' in request.form: 
            MaSoBB = request.form['MaSoBB'] 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * from BAIBAO where MaSoBB=%s',(MaSoBB,))
        account = cursor.fetchall()
        MS=MaSoBB
        return render_template("indexTG5.html",MS=MS, account=account) 
    return redirect(url_for('loginTG'))

#Trang 6 của tác giả liên lạc
@app.route("/indexTG6", methods=['GET', 'POST'])
def indexTG6():
    Nam=''
    if 'loggedinTG' in session: 
        if request.method == 'POST' and 'Nam' in request.form: 
            Nam = request.form['Nam'] 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * from BAIBAO where SUBSTRING(NgayGui, 1, 4)=%s',(Nam,))
        account = cursor.fetchall()
        MS=Nam
        return render_template("indexTG6.html",MS=MS, account=account) 
    return redirect(url_for('loginTG'))

#Trang 7 của tác giả liên lạc
@app.route("/indexTG7", methods=['GET', 'POST'])
def indexTG7():
    Nam=''
    if 'loggedinTG' in session: 
        if request.method == 'POST' and 'Nam' in request.form: 
            Nam = request.form['Nam'] 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * from BAIBAO where TrangThai="Đã đăng" AND SUBSTRING(NgayCapNhatKQ, 1, 4)=%s',(Nam,))
        account = cursor.fetchall()
        MS=Nam
        return render_template("indexTG7.html",MS=MS, account=account) 
    return redirect(url_for('loginTG'))

#Trang 8 của tác giả liên lạc
@app.route("/indexTG8", methods=['GET', 'POST'])
def indexTG8():
    if 'loggedinTG' in session:  
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * from BAIBAO where TrangThai="Xuất bản"')
        account = cursor.fetchall()
        return render_template("indexTG8.html", account=account) 
    return redirect(url_for('loginTG'))

#Trang 9 của tác giả liên lạc
@app.route("/indexTG9", methods=['GET', 'POST'])
def indexTG9():
    if 'loggedinTG' in session:  
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * from BAIBAO where KetQua="rejection"')
        account = cursor.fetchall()
        return render_template("indexTG9.html", account=account) 
    return redirect(url_for('loginTG'))

#Trang 10 của tác giả liên lạc
@app.route("/indexTG10", methods=['GET', 'POST'])
def indexTG10():
    today=date.today()
    a=str(today)
    b=a[0:4]
    b1=a[0:4]
    b2=a[0:4]
    b3=a[0:4]
    b4=a[0:4]
    if 'loggedinTG' in session:  
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) from BAIBAO where ((SELECT convert(% s, unsigned)) - (SELECT CONVERT( SUBSTRING(NgayGui, 1, 4),unsigned))=0);',(b,))
        account = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) from BAIBAO where ((SELECT convert(% s, unsigned)) - (SELECT CONVERT( SUBSTRING(NgayGui, 1, 4),unsigned))=1);',(b1,))
        account1 = cursor.fetchall()
        b1=str(int(b1)-1)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) from BAIBAO where ((SELECT convert(% s, unsigned)) - (SELECT CONVERT( SUBSTRING(NgayGui, 1, 4),unsigned))=2);',(b2,))
        account2 = cursor.fetchall()
        b2=str(int(b2)-2)

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) from BAIBAO where ((SELECT convert(% s, unsigned)) - (SELECT CONVERT( SUBSTRING(NgayGui, 1, 4),unsigned))=3);',(b3,))
        account3 = cursor.fetchall()
        b3=str(int(b3)-3)

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) from BAIBAO where ((SELECT convert(% s, unsigned)) - (SELECT CONVERT( SUBSTRING(NgayGui, 1, 4),unsigned))=4);',(b4,))
        account4 = cursor.fetchall()
        b4=str(int(b4)-4)
        return render_template("indexTG10.html",b=b,b1=b1,b2=b2,b3=b3,b4=b4, account=account,account1=account1,account2=account2,account3=account3,account4=account4) 
    return redirect(url_for('loginTG'))

    #Trang 11 của tác giả liên lạc
@app.route("/indexTG11", methods=['GET', 'POST'])
def indexTG11():
    today=date.today()
    a=str(today)
    b=a[0:4]
    b1=a[0:4]
    b2=a[0:4]
    b3=a[0:4]
    b4=a[0:4]

    b5=a[0:4]
    b6=a[0:4]
    b7=a[0:4]
    b8=a[0:4]
    b9=a[0:4]
    if 'loggedinTG' in session:  
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) from BAIBAO where SUBSTRING(MaSoBB,1,2)="NC" AND TrangThai="Đã đăng" AND ((SELECT convert(% s, unsigned)) - (SELECT CONVERT( SUBSTRING(NgayCapNhatKQ, 1, 4),unsigned))=0);',(b,))
        account = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) from BAIBAO where SUBSTRING(MaSoBB,1,2)="NC" AND TrangThai="Đã đăng" AND ((SELECT convert(% s, unsigned)) - (SELECT CONVERT( SUBSTRING(NgayCapNhatKQ, 1, 4),unsigned))=1);',(b1,))
        account1 = cursor.fetchall()
        b1=str(int(b1)-1)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) from BAIBAO where SUBSTRING(MaSoBB,1,2)="NC" AND TrangThai="Đã đăng" AND ((SELECT convert(% s, unsigned)) - (SELECT CONVERT( SUBSTRING(NgayCapNhatKQ, 1, 4),unsigned))=2);',(b2,))
        account2 = cursor.fetchall()
        b2=str(int(b2)-2)

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) from BAIBAO where SUBSTRING(MaSoBB,1,2)="NC" AND TrangThai="Đã đăng" AND ((SELECT convert(% s, unsigned)) - (SELECT CONVERT( SUBSTRING(NgayCapNhatKQ, 1, 4),unsigned))=3);',(b3,))
        account3 = cursor.fetchall()
        b3=str(int(b3)-3)

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) from BAIBAO where SUBSTRING(MaSoBB,1,2)="NC" AND TrangThai="Đã đăng" AND ((SELECT convert(% s, unsigned)) - (SELECT CONVERT( SUBSTRING(NgayCapNhatKQ, 1, 4),unsigned))=4);',(b4,))
        account4 = cursor.fetchall()
        b4=str(int(b4)-4)

        #####################################################################################3333
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) from BAIBAO where SUBSTRING(MaSoBB,1,2)="TQ" AND TrangThai="Đã đăng" AND ((SELECT convert(% s, unsigned)) - (SELECT CONVERT( SUBSTRING(NgayCapNhatKQ, 1, 4),unsigned))=0);',(b5,))
        account5 = cursor.fetchall()
        b5=str(int(b5))
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) from BAIBAO where SUBSTRING(MaSoBB,1,2)="TQ" AND TrangThai="Đã đăng" AND ((SELECT convert(% s, unsigned)) - (SELECT CONVERT( SUBSTRING(NgayCapNhatKQ, 1, 4),unsigned))=1);',(b6,))
        account6 = cursor.fetchall()
        b6=str(int(b6)-1)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) from BAIBAO where SUBSTRING(MaSoBB,1,2)="TQ" AND TrangThai="Đã đăng" AND ((SELECT convert(% s, unsigned)) - (SELECT CONVERT( SUBSTRING(NgayCapNhatKQ, 1, 4),unsigned))=2);',(b7,))
        account7 = cursor.fetchall()
        b7=str(int(b7)-2)

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) from BAIBAO where SUBSTRING(MaSoBB,1,2)="TQ" AND TrangThai="Đã đăng" AND ((SELECT convert(% s, unsigned)) - (SELECT CONVERT( SUBSTRING(NgayCapNhatKQ, 1, 4),unsigned))=3);',(b8,))
        account8 = cursor.fetchall()
        b8=str(int(b8)-3)

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) from BAIBAO where SUBSTRING(MaSoBB,1,2)="TQ" AND TrangThai="Đã đăng" AND ((SELECT convert(% s, unsigned)) - (SELECT CONVERT( SUBSTRING(NgayCapNhatKQ, 1, 4),unsigned))=4);',(b9,))
        account9 = cursor.fetchall()
        b9=str(int(b9)-4)
        return render_template("indexTG11.html",b=b,b1=b1,b2=b2,b3=b3,b4=b4, account=account,account1=account1,account2=account2,account3=account3,account4=account4,b5=b5,b6=b6,b7=b7,b8=b8,b9=b9, account5=account5,account6=account6,account7=account7,account9=account9,account8=account8) 
    return redirect(url_for('loginTG'))
if __name__ == "__main__":
    app.run()
