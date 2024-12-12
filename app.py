from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Flaskアプリ設定
app = Flask(__name__)
CORS(app)

# SQLAlchemy設定
DATABASE_URL = os.getenv("MYSQL_CONNECT")
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# モデル定義
class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(255), unique=True, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)

# テーブル作成
Base.metadata.create_all(bind=engine)

@app.route('/')
def home():
    return jsonify({"message": "Flask app is running with Azure MySQL!"})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'user_name' not in data:
        return jsonify({"error": "Invalid input"}), 400

    db = SessionLocal()
    try:
        user = Users(user_name=data['user_name'])
        db.add(user)
        db.commit()
        return jsonify({"message": "User created successfully", "user_name": user.user_name}), 201
    except IntegrityError:
        db.rollback()
        return jsonify({"error": "User already exists"}), 400
    finally:
        db.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)





from openai import OpenAI
from flask import Flask, jsonify, request
from flask_cors import CORS

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

import os
from datetime import datetime, timedelta
from dotenv import load_dotenv


load_dotenv()
mysql_connect = os.getenv("MYSQL_CONNECT")


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})  # CORS設定を更新

db = SQLAlchemy(app)

#Table定義

# employeesテーブルの定義
class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255), nullable=False, unique=True)
    data = db.Column(db.DateTime, default=db.func.current_timestamp())

# MySQLデータベースの接続設定
app.config['SQLALCHEMY_DATABASE_URI'] = mysql_connect
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.route('/', methods=['GET'])
def hello():
    return jsonify({'message': 'Flask start!'})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()  # JSONデータを取得
    if data is None:
        return jsonify({"error": "Invalid JSON"}), 400
    # 'message' プロパティが含まれていることを確認
    user_name = data.get('user_name', 'No user_name provided')

    now = datetime.now()

    try:
        # トークンを生成
        user_data = {
            "user_name": user_name,
            "date":now
        }

        # トークンをユーザー情報に保存
        user_data.user_name = user_name
        user_data.data = now

        # ユーザー情報をデータベースに保存
        db.session.add(user_data)
        db.session.commit()
        db.session.refresh(user_data)

    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"detail": "Database error occurred", "error": str(e)}), 500

    return jsonify({
        "access_token": user_name
    }), 201

if __name__ == '__main__':
    app.run(debug=True)










from flask import Flask, request
from flask import jsonify
import json
from flask_cors import CORS

from db_control import crud, mymodels

import requests

# Azure Database for MySQL
# REST APIでありCRUDを持っている
app = Flask(__name__)
CORS(app)
 

@app.route("/")
def index():
    return "<p>Flask top page!</p>"
 
@app.route("/customers", methods=['POST'])
def create_customer():
    values = request.get_json()
    # values = {
    #     "customer_id": "C005",
    #     "customer_name": "佐藤Aこ",
    #     "age": 64,
    #     "gender": "女"
    # }

    # Validate customer_id before insertion
    customer_id = values.get("customer_id")
    
    if not customer_id or customer_id.strip() == "":
        return jsonify({"error": "customer_id is required and cannot be blank"}), 400

    tmp = crud.myinsert(mymodels.Customers, values)
    result = crud.myselect(mymodels.Customers, values.get("customer_id"))
    return result, 200

@app.route("/customers", methods=['GET'])
def read_one_customer():
    model = mymodels.Customers
    target_id = request.args.get('customer_id') #クエリパラメータ
    result = crud.myselect(mymodels.Customers, target_id)
    return result, 200

@app.route("/allcustomers", methods=['GET'])
def read_all_customer():
    model = mymodels.Customers
    result = crud.myselectAll(mymodels.Customers)
    return result, 200

@app.route("/customers", methods=['PUT'])
def update_customer():
    print("I'm in")
    values = request.get_json()
    values_original = values.copy()
    model = mymodels.Customers
    # values = {  "customer_id": "C004",
    #             "customer_name": "鈴木C子",
    #             "age": 44,
    #             "gender": "男"}
    tmp = crud.myupdate(model, values)
    result = crud.myselect(mymodels.Customers, values_original.get("customer_id"))
    return result, 200

@app.route("/customers", methods=['DELETE'])
def delete_customer():
    model = mymodels.Customers
    target_id = request.args.get('customer_id') #クエリパラメータ
    result = crud.mydelete(model, target_id)
    return result, 200

@app.route("/fetchtest")
def fetchtest():
    response = requests.get('https://jsonplaceholder.typicode.com/users')
    return response.json(), 200
