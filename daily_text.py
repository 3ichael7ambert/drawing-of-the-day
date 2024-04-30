# daily_text.py

import random
from twilio.rest import Client
import psycopg2
from psycopg2 import sql
from datetime import datetime

# Twilio credentials
account_sid = 'YOUR_TWILIO_ACCOUNT_SID'
auth_token = 'YOUR_TWILIO_AUTH_TOKEN'
twilio_phone_number = 'YOUR_TWILIO_PHONE_NUMBER'
client = Client(account_sid, auth_token)

# PostgreSQL database configuration
db_config = {
    'dbname': 'draw_day',
    'user': 'username',
    'password': 'password',
    'host': 'localhost'
}

def send_daily_sms():
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    # Query free tier users
    cursor.execute("SELECT * FROM users WHERE role = 'free'")
    free_users = cursor.fetchall()

    for user in free_users:
        phone_number = user[1]  # Assuming phone number is stored in the second column
        noun = get_random_word('nouns.txt')
        message = f"Daily Text Prompt: {noun}! MyDailyPrompt.com"
        send_sms(phone_number, message)

    # Query paid users
    cursor.execute("SELECT * FROM users WHERE role = 'paid'")
    paid_users = cursor.fetchall()

    for user in paid_users:
        phone_number = user[1]  # Assuming phone number is stored in the second column
        noun = get_random_word('nouns.txt')
        verb = get_random_word('verbs.txt')
        adjective = get_random_word('adjectives.txt')
        location = get_random_word('locations.txt')
        media = get_random_word('media.txt')
        message = f"Daily Text Prompt: {adjective} {noun} {verb} at {location}! ~{media}~ MyDailyPrompt.com"
        send_sms(phone_number, message)

    cursor.close()
    conn.close()

def get_random_word(filename):
    with open(filename, 'r') as file:
        words = file.readlines()
        return random.choice(words).strip()

def send_sms(phone_number, message):
    client.messages.create(
        body=message,
        from_=twilio_phone_number,
        to=phone_number
    )

if __name__ == '__main__':
    # Run the function to send daily SMS
    send_daily_sms()
