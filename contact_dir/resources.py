from flask_restful import Resource, reqparse
from models import db, Contact
import re

# Define a regex pattern for valid email
email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

# Define a regex pattern for valid phone numbers (10 digits)
phone_pattern = r"^\d{10}$"

contact_parser = reqparse.RequestParser()
contact_parser.add_argument("name", required=True, help="Name cannot be blank")
contact_parser.add_argument("email", required=True, help="Email cannot be blank")
contact_parser.add_argument("phone", required=True, help="Phone cannot be blank")
contact_parser.add_argument("group", required=False)

def validate_email(email):
    if not re.match(email_pattern, email):
        raise ValueError("Invalid email format")

def validate_phone(phone):
    if not re.match(phone_pattern, phone):
        raise ValueError("Phone number must contain exactly 10 digits")

def validate_group(group):
    if not isinstance(group, str):
        raise ValueError("Group must be a string")

class ContactResource(Resource):
    def get(self, contact_id):
        contact = Contact.query.get_or_404(contact_id)
        return {
            "id": contact.id,
            "name": contact.name,
            "email": contact.email,
            "phone": contact.phone,
            "group": contact.group
        }, 200

    def put(self, contact_id):
        args = contact_parser.parse_args()
        validate_email(args["email"])
        validate_phone(args["phone"])
        if args["group"]:
            validate_group(args["group"])

        contact = Contact.query.get_or_404(contact_id)
        contact.name = args["name"]
        contact.email = args["email"]
        contact.phone = args["phone"]
        contact.group = args["group"]
        db.session.commit()
        return {"message": "Contact updated successfully"}, 200

    def delete(self, contact_id):
        contact = Contact.query.get_or_404(contact_id)
        db.session.delete(contact)
        db.session.commit()
        return {"message": "Contact deleted successfully"}, 200

class ContactListResource(Resource):
    def get(self):
        contacts = Contact.query.all()
        return [
            {
                "id": c.id,
                "name": c.name,
                "email": c.email,
                "phone": c.phone,
                "group": c.group
            } for c in contacts
        ], 200

    def post(self):
        args = contact_parser.parse_args()
        validate_email(args["email"])
        validate_phone(args["phone"])
        if args["group"]:
            validate_group(args["group"])

        new_contact = Contact(
            name=args["name"],
            email=args["email"],
            phone=args["phone"],
            group=args["group"]
        )
        db.session.add(new_contact)
        db.session.commit()
        return {"message": "Contact added successfully"}, 201