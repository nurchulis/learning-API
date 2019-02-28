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


## user sing up
@app.route('/api/v1/signup',methods=['POST'])
def signUp():
     
    requests = json.loads(request.data)
    

    _ava   = requests['avatar']
    _user  = requests['username']
    _email   = requests['email']
    _pass   = requests['password']
    _prodi   = requests['prodi']
    _ver   = requests['verifed']
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

## Show user with id_user
@app.route('/api/v1/user/<id>')
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

## Login with username and password
@app.route('/api/v1/auth', methods=['POST'])
def auth(): 
    try:
        requests = json.loads(request.data)
    except ValueError as e:
        abort(400)

    conn = mysql.connect()
    cursor = conn.cursor()
    result=cursor.execute("SELECT * FROM User WHERE username = %s and password = %s",(requests['username'], requests['password']))
    data = cursor.fetchall()
    
    if(result):
        for item in data:
            dataResponse = {
                'success'     : 'true',
                'id_user'     : item[0],
                'username'    : requests['username']
            }
 
        return json.dumps(dataResponse)

    else:
        return json.dumps({'success':'false'})


## Update User where id_user
@app.route('/api/v1/update/<id>',methods=['POST'])
def update(id):
    try:
        requests = json.loads(request.data)
    except ValueError as e:
        abort(400)
    
    conn = mysql.connect()
    cursor = conn.cursor()
    result = cursor.execute("UPDATE User SET avatar = %s, username = %s, email = %s, password = %s, prodi = %s, verifed = %s WHERE id_user = %s",
                            (requests['avatar'],requests['username'],requests['email'],requests['password'],requests['prodi'],requests['verifed'],int(id)))
    conn.commit()
    conn.close()
    if(result):
        return json.dumps({'success':'true'})
    else:
        return json.dumps({'success':'false'})

## Delete Where Id_user
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


## Get Class where id user 
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


## Get all Post in Where id_class
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


## Insert Posting
@app.route('/api/v1/post',methods=['POST'])
def posting():
    try:
        requests = json.loads(request.data)
    except ValueError as e:
        abort(400)
    
    # read request from UI
    _id_class   = requests['id_class']
    _id_user  = requests['id_user']
    _caption   = requests['caption']
    _category   = requests['category']
    _file   = requests['file']
    
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

## Update post where id_posting
@app.route('/api/v1/update_post/<id>',methods=['POST'])
def update_post_(id):
    try:
        requests = json.loads(request.data)
    except ValueError as e:
        abort(400)

    conn = mysql.connect()
    cursor = conn.cursor()
    result = cursor.execute("UPDATE Posting SET caption = %s, file = %s WHERE id_posting = %s",
                            (requests['caption'],requests['file'],int(id)))
    conn.commit()
    conn.close()
    if(result):
        return json.dumps({'success':'true'})
    else:
        return json.dumps({'success':'false'})

## Delete Post where id_post
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

## Join in the Class, insert join in join_class
@app.route('/api/v1/join',methods=['POST'])
def join_class_():
    try:
        requests = json.loads(request.data)
    except ValueError as e:
        abort(400)
    
    # read request from UI
    _id_user  = requests['id_user']
    _id_class = requests['id_class']
    _rule   = requests['rule']
    _accept   = requests['accept']
    
    if _id_user and _id_class and _rule and _accept:
        insert_join(_id_user,_id_class,_rule, _accept)
        return json.dumps({'success':'true'})
    else:
        return json.dumps({'success':'false'})

def insert_join(id_user,id_class,rule,accept):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO Join_class (
                id_user,
                id_class,
                rule,
                accept
            ) 
            VALUES (%s, %s, %s, %s)""",(id_user, id_class, rule, accept))
    conn.commit()
    conn.close()   

## Accept join 
@app.route('/api/v1/accept_join/<id>/<id_class>',methods=['POST'])
def accept_join(id,id_class):


    conn = mysql.connect()
    cursor = conn.cursor()
    result = cursor.execute("UPDATE Join_class SET accept = 1 WHERE id_user = %s AND id_class = %s ",(int(id),int(id_class)))
    conn.commit()
    conn.close()
    if(result):
        return json.dumps({'success':'true'})
    else:
        return json.dumps({'description':'Your already join','success':'false'})



## Inser Comment with id_posting
@app.route('/api/v1/comment',methods=['POST'])
def comment_():
    try:
        requests = json.loads(request.data)
    except ValueError as e:
        abort(400)
    
    # read request from UI
    _id_posting = requests['id_posting']
    _data   = requests['data']
    
    if _id_posting and _data:
        insert_comment(_id_posting,_data)
        return json.dumps({'success':'true', 'data':_data})
    else:
        return json.dumps({'success':'false'})

def insert_comment(id_posting,data):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO Comment (
                id_posting,
                data
            ) 
            VALUES (%s, %s)""",(id_posting, data))
    conn.commit()
    conn.close()   

## Update Comment By id_comment
@app.route('/api/v1/update_comment/<id>',methods=['POST'])
def update_comment_(id):
    try:
        requests = json.loads(request.data)
    except ValueError as e:
        abort(400)

    conn = mysql.connect()
    cursor = conn.cursor()
    result = cursor.execute("UPDATE Comment SET data = %s WHERE id_comment = %s",
                            (requests['data'],int(id)))
    conn.commit()
    conn.close()
    if(result):
        return json.dumps({'success':'true'})
    else:
        return json.dumps({'success':'false'})


## Delete Comment where id_comment
@app.route('/api/v1/delete_comment/<id>')
def delete_comment_(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    result = cursor.execute("DELETE FROM Comment WHERE id_comment = %s",int(id))
    conn.commit()
    conn.close()
    if(result):
        return json.dumps({'success':'true'})
    else:
        return json.dumps({'success':'false'})




        
if __name__ == '__main__':
    app.run()