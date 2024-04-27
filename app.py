from flask import Flask, request
from twilio.rest import Client
import random

app = Flask(__name__)

# Twilio credentials
account_sid = 'YOUR_TWILIO_ACCOUNT_SID'
auth_token = 'YOUR_TWILIO_AUTH_TOKEN'
twilio_phone_number = 'YOUR_TWILIO_PHONE_NUMBER'
client = Client(account_sid, auth_token)

# PostgreSQL database configuration
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/databasename'
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), unique=True)

# Route for user signup
@app.route('/signup', methods=['POST'])
def signup():
    phone_number = request.json.get('phone_number')

    # Check if the phone number is already registered
    if User.query.filter_by(phone_number=phone_number).first():
        return 'Phone number already registered', 400

    # Create a new user
    new_user = User(phone_number=phone_number)
    db.session.add(new_user)
    db.session.commit()

    return 'Signup successful', 201

# Function to send daily SMS
def send_daily_sms():
    users = User.query.all()
    words_lists = {
        'nouns': ['list', 'of', 'nouns'],
        'activities': ['list', 'of', 'activities'],
        'mediums': ['list', 'of', 'mediums'],
        'adjectives': ['list', 'of', 'adjectives']
    }
    for user in users:
        random_message = ' '.join(random.choice(words) for words in words_lists.values())
        send_sms(user.phone_number, random_message)

# Function to send SMS using Twilio
def send_sms(phone_number, message):
    client.messages.create(
        body=message,
        from_=twilio_phone_number,
        to=phone_number
    )

if __name__ == '__main__':
    app.run(debug=True)

