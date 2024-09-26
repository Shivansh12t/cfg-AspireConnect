from twilio.twiml.voice_response import VoiceResponse, Gather

def handle_sponsor_choice_flow(response):
    gather = Gather(numDigits=1, action="/handle-sponsor-choice", method="POST")
    gather.say("If you want to sponsor a kindergarten child, press 1.")
    gather.say("If you want to sponsor an elementary school child, press 2.")
    gather.say("If you want to sponsor a high school child, press 3.")
    response.append(gather)
    return response
