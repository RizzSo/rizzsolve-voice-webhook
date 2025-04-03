from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse
from twilio.twiml.messaging_response import MessagingResponse
import os

app = Flask(__name__)

# Health check route (optional)
@app.route("/", methods=["GET"])
def index():
    return "Rizzsolve webhook is live!"

# Voice webhook
@app.route("/voice", methods=["POST"])
def voice():
    response = VoiceResponse()
    response.say("Hello from Rizzsolve! Thanks for calling.", voice='alice')
    return Response(str(response), mimetype='text/xml')

# SMS webhook (optional, for future use)
@app.route("/sms", methods=["POST"])
def sms():
    incoming_msg = request.form.get("Body")
    response = MessagingResponse()
    response.message(f"Rizzsolve received your message: {incoming_msg}")
    return Response(str(response), mimetype='text/xml')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

