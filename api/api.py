import pymysql
import flask
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request
from werkzeug import generate_password_hash, check_password_hash



app = flask.Flask(__name__)
app.config["DEBUG"] = True

books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]

@app.route('/signup',methods=['POST'])
def signUp():
    # open connection

    # read request from UI
    _avatar  = request.form['avatar']
    _username   = request.form['username']
    _email 		= request.form['email']
    _password 	= request.form['password']
    _prodi		= request.form['prodi']
    _verifed	= request.form['verifed']

    if  _avatar and _username and _email and _password and _prodi and _verifed:
        insert(_avatar,_username,_email,_password,_prodi,_verifed)
        return json.dumps({'html':'<span>Data Inserted </span>'})
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})


def insert(_avatar,_username,_email,_password,_prodi,_verifed):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO User(avatar, username, email, password, prodi, verifed)
            VALUES (%s,%s,%s,%s,%s,%s)""",(avatar, username, email, password, prodi, verifed))
    conn.commit()
    conn.close()


@app.route('/add', methods=['POST'])
def add_user():
	try:
		_json = request.json
		_id_user = _json['id_user']
		_avatar = _json['avatar']
		_username = _json['username']
		_email = _json['email']
		_password = _json['password']
		_prodi = _json['prodi']
		_verifed = _json['verifed']
		# validate the received values
		if _id_user and _avatar and _username and _email and _password and _prodi and _verifed and request.method == 'POST':
			#do not save password as a plain text
			#_hashed_password = generate_password_hash(_password)
			# save edits
			conn = mysql.connect()
			cursor = conn.cursor()
			sql = "INSERT INTO User(id_user, avatar, username, email, password, prodi, verifed) VALUES(%s, %s, %s, %s, %s, %s, %s)"
			data = (_id_user, _avatar, _username , _email, _password, _prodi, _verifed)
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('User added successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/', methods=['GET'])
def home():
    return "<h1>Under Development API Learning</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

# A route to return all of the available entries in our catalog.
@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    return jsonify(books)

@app.route('/api/v1/resources/books', methods=['GET'])
def api_id():
	if 'id' in request.args:
		id = int(request.args['id'])
	else:
		return "Error: No id fields provided. Please specify an id."

	# Create an empty list for our result
	results = []

	# Loop though the data and match result that fit the requested ID.
	# IDs are unique, but other fields might return many results
	for book in books:
		if book['id'] == id:
			results.append(book)

	# Use the jsonify function form Flask to convert out list of
	# Python disctionaries to the JSON format.
	return jsonify(results)

app.run()

