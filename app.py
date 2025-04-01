from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
from twilio.twiml.voice_response import VoiceResponse, Dial, Record
from twilio.rest import Client
from datetime import datetime

app = Flask(__name__)

# --- Database setup ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reminders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Twilio setup ---
ACCOUNT_SID = 'your_account_sid_here'
AUTH_TOKEN = 'your_auth_token_here'
TWILIO_NUMBER = '+1yourtwilionumber'
client = Client(ACCOUNT_SID, AUTH_TOKEN)

# --- Reminder model ---
class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), nullable=False)
    message = db.Column(db.String(160), nullable=False)
    send_time = db.Column(db.DateTime, nullable=False)
    sent = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

# --- Voice routes ---
@app.route("/voice", methods=['POST'])
def voice():
    response = VoiceResponse()
    response.say("Thanks for calling Rizzsolve! Please hold while we connect you.", voice='alice')
    dial = Dial(timeout=20, action="/voicemail")
    dial.number("+1YOURPHONENUMBER")  # ← Replace with your actual number
    response.append(dial)
    return Response(str(response), mimetype='text/xml')

@app.route("/voicemail", methods=['POST'])
def voicemail():
    response = VoiceResponse()
    response.say("We couldn't connect you. Please leave a message after the tone.", voice='alice')
    response.record(max_length=60, action="/handle-recording", transcribe=True)
    return Response(str(response), mimetype='text/xml')

@app.route("/handle-recording", methods=['POST'])
def handle_recording():
    from_number = request.form.get("From")
    client.messages.create(
        body="Thanks for calling Rizzsolve! We’ll be in touch soon.",
        from_=TWILIO_NUMBER,
        to=from_number
    )
    return "Reminder text sent!", 200

# --- Reminder form & scheduling ---
@app.route("/add-reminder", methods=["POST"])
def add_reminder():
    phone = request.form.get("phone")
    message = request.form.get("message")
    send_time_str = request.form.get("send_time")  # e.g., "2025-04-01 14:30"
    send_time = datetime.strptime(send_time_str, "%Y-%m-%d %H:%M")
    reminder = Reminder(phone_number=phone, message=message, send_time=send_time)
    db.session.add(reminder)
    db.session.commit()
    return "Reminder scheduled!", 200

@app.route("/reminder-form")
def reminder_form():
    return '''
    <form action="/add-reminder" method="post">
        Phone: <input name="phone"><br>
        Message: <input name="message"><br>
        Send Time (YYYY-MM-DD HH:MM): <input name="send_time"><br>
        <input type="submit">
    </form>
    '''

@app.route("/")
def index():
    return "Smart Founder Line with Reminders is live!", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

