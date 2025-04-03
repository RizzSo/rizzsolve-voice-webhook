from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse
import os

app = Flask(__name__)

@app.route("/voice", methods=["POST"])
def voice():
    response = VoiceResponse()
    gather = response.gather(num_digits=1, action="/handle-key", method="POST")
    gather.say("Hello from Rizzsolve. Press 1 to confirm your appointment. Press 2 to reschedule.")
    response.redirect("/voice")  # If no input, repeat
    return Response(str(response), mimetype='text/xml')

@app.route("/handle-key", methods=["POST"])
def handle_key():
    digit = request.form.get("Digits")
    response = VoiceResponse()
    if digit == "1":
        response.say("Appointment confirmed. Thank you.")
    elif digit == "2":
        response.say("We'll send you a link to reschedule.")
    else:
        response.say("Sorry, I didn't get that.")
        response.redirect("/voice")
    return Response(str(response), mimetype='text/xml')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

