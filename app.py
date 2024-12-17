#pip install pymysql flask-cors
import pymysql
from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql.cursors


app = Flask(__name__)
cors = CORS(app)

conn = pymysql.connect(host="localhost", port=3306, user = "root", password="12345678", db="ums")


@app.route('/users', methods=['GET'])
def get_users():
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM users")
    output= cur.fetchall()
    return jsonify(output)

@app.route('/users/get_one_user', methods=['GET'])
def get_one_users():
    id = int(request.args.get('id'))
    cur =  conn.cursor(pymysql.cursors.DictCursor)
    cur.execute(f"SELECT * FROM users where id = {id}")
    output = cur.fetchone()

    return jsonify(output)


@app.route('/users', methods=['POST'])
def insert_users():
    raw_json = request.get_json()
    name = raw_json['name']
    age = raw_json['age']
    address = raw_json['address']

    sql = f"INSERT INTO users (name, age, address) VALUES ('{name}', {age}, '{address}')"
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    return { "status":"Record inserted Sucessfully"}

@app.route('/users', methods=['DELETE'])
def delete_users():
    id  = int(request.args.get('id'))
    sql = f"DELETE FROM users WHERE id = {id}"
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    return {"message":"Record Delete Sucessfully"}

@app.route('/users', methods=['PUT'])
def update_users():
    id = int(request.args.get('id'))
    
    raw_json = request.get_json()
    name = raw_json['name']
    age = raw_json['age']
    address = raw_json['address']
    
    sql = f"UPDATE users SET name = '{name}', age = {age}, address = '{address}' WHERE id = {id}"
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    return {"message":"Update Record Sucessfully"}

@app.route('/', methods=['GET'])
def home():
    return "Welcome to our Home Page"


@app.route('/sqr', methods=['POST'])
def sqr():
    raw_json = request.get_json()
    num1 = int(raw_json['num1'])
    return f"{num1} square is {num1 * num1}"

if __name__ == "__main__":
    app.run(debug = True)
