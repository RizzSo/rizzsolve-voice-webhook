from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)

@app.route("/voice", methods=['POST'])
def voice():
    response = VoiceResponse()
    response.say("Thanks for calling Rizzsolve! We'll be with you shortly.", voice='alice')
    response.play("http://demo.twilio.com/docs/classic.mp3")
    return Response(str(response), mimetype='text/xml')

@app.route("/")
def index():
    return "Rizzsolve Voice Webhook is live!", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
