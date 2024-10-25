from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from config import Config
from models import db
from resources import ContactResource, ContactListResource
from auth import RegisterResource, LoginResource

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
db.init_app(app)

with app.app_context():
    db.create_all()  # Create tables

api = Api(app)

# Routes
api.add_resource(ContactListResource, '/contacts')
api.add_resource(ContactResource, '/contacts/<int:contact_id>')
api.add_resource(RegisterResource, '/register')  # Register route
api.add_resource(LoginResource, '/login')        # Login route

if __name__== '__main__':
    app.run(debug=True)