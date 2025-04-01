from flask_sqlalchemy import SQLAlchemy
from models import db, Reminder

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reminders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route("/voice", methods=['POST'])
def voice():
    response = VoiceResponse()
    
    response.say("Thanks for calling Rizzsolve! Please hold while we connect you.", voice='alice')

    dial = Dial(timeout=20, action="/voicemail")
    dial.number("+1YOURPHONENUMBER")  # ← Replace this with YOUR cell number
    response.append(dial)

    return Response(str(response), mimetype='text/xml')

@app.route("/voicemail", methods=['POST'])
def voicemail():
    response = VoiceResponse()
    
    response.say("We couldn't connect you. Please leave a message after the tone.", voice='alice')
    response.record(
        max_length=60,
        action="/handle-recording",
        transcribe=True
    )
    return Response(str(response), mimetype='text/xml')

@app.route("/handle-recording", methods=['POST'])
def handle_recording():
    # This is where you could email yourself the voicemail later!
    return "Recording received", 200

@app.route("/")
def index():
    return "Smart Founder Line is live!", 200

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

from datetime import datetime

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

