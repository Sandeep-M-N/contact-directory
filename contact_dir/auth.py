# from flask_restful import Resource, reqparse
# from models import db, User
# from flask import jsonify, Flask, request
# from werkzeug.security import generate_password_hash, check_password_hash
 

# class RegisterResource(Resource):
#     def post(self):
#         data = request.get_json()
#         username = data.get('username')
#         password = data.get('password')

#         # Check if passwords match
#         if not username or not password:
#             return {"message": "missing username or password"}, 400

#         # Check if username already exists
#         if User.query.filter_by(username=username).first():
#             return {"message": "Username already exists"}, 400

#         # Hash the password before storing it
#         hashed_password = generate_password_hash(password)

#         # Create new user
#         new_user = User(username=username, password=hashed_password)
        
#         db.session.add(new_user)
#         db.session.commit()

#         return {"message": "User registered successfully"}, 201


# class LoginResource(Resource):
#     def post(self):
#         data = request.get_json()
#         username = data.get('username')
#         password = data.get('password')

#         # Check if username exists
#         user = User.query.filter_by(username=username).first()
#         if user and check_password_hash(user.password, password):
#             return {"message": "User login successful"}, 200

#         return {"message": "Invalid credentials"}, 400

from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
import re

# Registration resource
class RegisterResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return {"message": "Missing username or password"}, 400

        if User.query.filter_by(username=username).first():
            return {"message": "Username already exists"}, 400

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        
        db.session.add(new_user)
        db.session.commit()

        return {"message": "User registered successfully"}, 201

# Login resource
class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            return {"message": "User login successful"}, 200

        return {"message": "Invalid credentials"}, 400