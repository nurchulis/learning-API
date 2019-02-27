import os
from pprint import pprint
from flask import Flask
from flask import render_template
from flask import request
from flask import json
import simplejson
from werkzeug.security import generate_password_hash, check_password_hash
from flaskext.mysql import MySQL

project_root = os.path.dirname(__name__)
template_path = os.path.join(project_root)

mysql = MySQL()
app = Flask(__name__,template_folder=template_path)
# mysql configuratoin
app.config['MYSQL_DATABASE_HOST']       = 'localhost'
app.config['MYSQL_DATABASE_USER']       = 'root'
app.config['MYSQL_DATABASE_PASSWORD']   = 'root'
app.config['MYSQL_DATABASE_DB']         = 'learning'
mysql.init_app(app)

@app.route('/')
def main_world():
    return render_template('static/index.html')

@app.route('/api/v1/signup',methods=['POST'])
def signUp():
    # open connection

    # read request from UI
    _ava   = request.form['avatar']
    _user  = request.form['username']
    _email   = request.form['email']
    _pass   = request.form['password']
    _prodi   = request.form['prodi']
    _ver   = request.form['verifed']
    _hash_pass = generate_password_hash(_pass)

    if _ava and _user and _email and _pass and _prodi and _ver:
        insert(_ava,_user,_email, _pass,_prodi,_ver)
        return json.dumps({'html':'<span>Data Inserted </span>'})
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})

def insert(avatar,username,email,password,prodi,verifed):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO User (
                avatar,
                username,
                email,
                password,
                prodi,
                verifed
            ) 
            VALUES (%s,%s,%s,%s,%s,%s)""",(avatar,username,email,password,prodi,verifed))
    conn.commit()
    conn.close()

@app.route('/api/v1/show/<id>')
def show(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM User WHERE id_user = %s",int(id))
    data = cursor.fetchall()
    
    if data is not None:
        for item in data:
            dataResponse = {
                'id_user'     : item[0],
                'avatar'      : item[1],
                'username'    : item[2],
                'email'       : item[3]
            }
        return json.dumps(dataResponse)
    else:
        return 'data kosong'

## For Auth login


@app.route('/api/v1/auth', methods=['POST'])
def auth():
    conn = mysql.connect()
    cursor = conn.cursor()
    result=cursor.execute("SELECT * FROM User WHERE username = %s and password = %s",(request.form['username'], request.form['password']))
    data = cursor.fetchall()
    
    if(result):
        for item in data:
            dataResponse = {
                'success'     : 'true',
                'id_user'     : item[0],
                'username'    : request.form['username']
            }
 
        return json.dumps(dataResponse)

    else:
        return json.dumps({'success':'false'})


@app.route('/api/v1/update/<id>',methods=['POST'])
def update(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    result = cursor.execute("UPDATE User SET avatar = %s, username = %s, email = %s, password = %s, prodi = %s, verifed = %s WHERE id_user = %s",
                            (request.form['avatar'],request.form['username'],request.form['email'],request.form['password'],request.form['prodi'],request.form['verifed'],int(id)))
    conn.commit()
    conn.close()
    if(result):
        return json.dumps({'success':'true'})
    else:
        return json.dumps({'success':'false'})

@app.route('/delete/<id>')
def delete(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    result = cursor.execute("DELETE FROM User WHERE id_user = %s",int(id))
    conn.commit()
    conn.close()
    if(result):
        return json.dumps({'success':'true'})
    else:
        return json.dumps({'success':'false'})


@app.route('/api/v1/class/<id>')
def get_class(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    result = cursor.execute("SELECT Join_class.rule, Class.id_class, Class.name_class, Class.id_teach, Class.description, Class.prodi, Class.sesi FROM Join_class JOIN User JOIN Class WHERE Join_class.id_user = User.id_user AND Class.id_class = Join_class.id_class AND User.id_user = %s ",int(id))
    data = cursor.fetchall()
    results = []
    if(result):
        for item in data:
            dataResponse = {
                'id_class'     : item[0],
                'id_teach'     : item[1],
                'name_class'   : item[2],
                'description'  : item[3],
                'prodi'        : item[4],
                'semester'     : item[5],
                'sesi'         : item[6],
            }
            results.append(dataResponse)
        return json.dumps(results)
    else:
        return json.dumps({'data':'null'})

@app.route('/api/v1/getclass/<id>')
def get_class_post(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    result = cursor.execute("SELECT * FROM Posting WHERE id_class=%s",int(id))
    data = cursor.fetchall()

    results = []
    if (result):
        for item in data:
            dataResponse = {
            'id_posting' : item[0],
            'id_class'   : item[1],
            'id_user'    : item[2],
            'caption'    : item[3],
            'category'   : item[4],
            'file'       : item[5],
            'time'       : item[6],
            }
            results.append(dataResponse)
        return json.dumps(results)
    else:
        return json.dumps({'data':'null'})



@app.route('/api/v1/post',methods=['POST'])
def posting():
    # open connection
    
    # read request from UI
    _id_class   = request.form['id_class']
    _id_user  = request.form['id_user']
    _caption   = request.form['caption']
    _category   = request.form['category']
    _file   = request.form['file']
    
    if _id_class and _id_user and _caption and _category and _file:
        insert_posting(_id_class,_id_user,_caption, _category,_file)
        return json.dumps({'html':'<span>Data Inserted </span>'})
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})

def insert_posting(id_class,id_user,caption,category,file):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO Posting (
                id_class,
                id_user,
                caption,
                category,
                file
            ) 
            VALUES (%s, %s, %s, %s, %s)""",(id_class, id_user, caption, category,file))
    conn.commit()
    conn.close()   


@app.route('/api/v1/update_post/<id>',methods=['POST'])
def update_post_(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    result = cursor.execute("UPDATE Posting SET caption = %s, file = %s WHERE id_posting = %s",
                            (request.form['caption'],request.form['file'],int(id)))
    conn.commit()
    conn.close()
    if(result):
        return json.dumps({'success':'true'})
    else:
        return json.dumps({'success':'false'})

@app.route('/api/v1/delete/<id>')
def delete_post(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    result = cursor.execute("DELETE FROM Posting WHERE id_posting = %s",int(id))
    conn.commit()
    conn.close()
    if(result):
        return json.dumps({'success':'true'})
    else:
        return json.dumps({'success':'false'})

        
if __name__ == '__main__':
    app.run()