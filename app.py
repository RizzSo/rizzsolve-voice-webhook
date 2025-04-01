from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Dial, Say, Record

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
