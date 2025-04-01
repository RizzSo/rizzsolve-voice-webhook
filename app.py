from flask import Flask
from twilio.rest import Client
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "App is running!"

@app.route("/send-reminder")
def send_reminder():
    client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
    message = client.messages.create(
        body="This is your reminder!",
        from_=os.getenv("TWILIO_PHONE_NUMBER"),
        to="+19876543210"  # Replace with recipient number
    )
    return f"Message sent: {message.sid}"

if __name__ == "__main__":
    app.run()

