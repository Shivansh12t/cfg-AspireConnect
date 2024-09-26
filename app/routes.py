from flask import request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import VoiceResponse, Gather, Pause

from .intents import get_intent
from .utils import send_whatsapp
from .voice import handle_sponsor_choice_flow

def init_routes(app):

    @app.route("/whatsapp", methods=['POST'])
    def whatsapp():
        incoming_msg = request.values.get('Body', '').strip().lower()
        from_number = request.values.get('From', '').replace('whatsapp:', '')
        response = MessagingResponse()
        msg = response.message()

        intent = get_intent(incoming_msg)

        # Handle intents
        if intent == 'sponsor child':
            msg.body(intents[intent])
        elif intent == 'support infrastructure':
            send_whatsapp(from_number, intents[intent])
        else:
            msg.body(intents.get(intent, intents['greet']))

        return str(response)

    @app.route("/voice", methods=['POST'])
    def voice():
        response = VoiceResponse()
        gather = Gather(numDigits=1, action="/gather", method="POST")
        gather.say("Thank you for calling Aspire and Glee...")
        gather.say("If you want to sponsor a child, press 1...")
        response.append(gather)
        response.pause(length=5)
        response.redirect("/gather")
        return str(response)

    @app.route("/gather", methods=['POST'])
    def gather():
        digits = request.form['Digits']
        response = VoiceResponse()

        if digits == '1':
            response = handle_sponsor_choice_flow(response)
        else:
            response.say("Sorry, I don't understand that choice.")
            response.redirect("/voice")

        return str(response)
