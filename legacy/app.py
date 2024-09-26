from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import VoiceResponse, Gather, Pause
from twilio.rest import Client
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import string
import numpy as np

nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

app = Flask(__name__)

# Your Twilio account SID and auth token
account_sid = '$yourssid'
auth_token = '$yourapikey'
client = Client(account_sid, auth_token)

# Your Twilio WhatsApp number and phone number
twilio_whatsapp_number = 'whatsapp:+youtwillionumber'
twilio_number = '+youcallingnumber'

# Predefined intents and responses
intents = {
    'greet': "Welcome to Aspire and Glee! How can we help you today? You can say things like 'I want to sponsor a child' or 'I want to donate clothes'.",
    'sponsor child': "Sure, do you want to sponsor a kindergarten child, an elementary school child, or a high school child?",
    'sponsor kindergarten child': "You will soon receive a WhatsApp message explaining the next steps to sponsor a kindergarten child. Please visit http://localhost:3000/eduparent/Donor/donateAmount.",
    'sponsor elementary school child': "You will soon receive a WhatsApp message explaining the next steps to sponsor an elementary school child. Please visit http://localhost:3000/eduparent/Donor/donateAmount.",
    'sponsor high school child': "You will soon receive a WhatsApp message explaining the next steps to sponsor a high school child. Please visit http://localhost:3000/eduparent/Donor/donateAmount.",
    'support infrastructure': "You will soon receive a WhatsApp message explaining the next steps to support our infrastructure. Please visit aspireandglee.com/donate-for-school.",
    'donate clothing': "Please visit aspireandglee.com/donate-clothes for more information on donating used clothing. Thank you.",
    'volunteer': "This feature will be implemented in the future. Thank you.",
}

# Function to preprocess text
def preprocess_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stopwords.words('english')]
    return ' '.join(tokens)

# Function to get intent
def get_intent(user_input):
    user_input = preprocess_text(user_input)
    corpus = list(intents.keys()) + [user_input]
    vectorizer = TfidfVectorizer().fit_transform(corpus)
    vectors = vectorizer.toarray()
    cosine_similarities = cosine_similarity(vectors[-1].reshape(1, -1), vectors[:-1])
    best_match = np.argmax(cosine_similarities)
    return list(intents.keys())[best_match]

# Function to send WhatsApp message
def send_whatsapp(to_number, message):
    client.messages.create(
        body=message,
        from_=twilio_whatsapp_number,
        to=f'whatsapp:{to_number}'
    )

# WhatsApp bot endpoint
@app.route("/whatsapp", methods=['POST'])
def whatsapp():
    incoming_msg = request.values.get('Body', '').strip().lower()
    from_number = request.values.get('From', '').replace('whatsapp:', '')
    response = MessagingResponse()
    msg = response.message()

    intent = get_intent(incoming_msg)

    if intent == 'sponsor child':
        msg.body(intents[intent])
    elif intent == 'support infrastructure':
        send_whatsapp(from_number, intents[intent])
        #msg.body("You will soon receive a WhatsApp message explaining the next steps. Thank you.")
    elif intent == 'donate clothing':
        msg.body(intents[intent])
    elif intent == 'volunteer':
        msg.body(intents[intent])
    elif intent == 'sponsor kindergarten child':
        send_whatsapp(from_number, intents[intent])
        #msg.body("You will soon receive a WhatsApp message explaining the next steps to sponsor a kindergarten child.")
    elif intent == 'sponsor elementary school child':
        send_whatsapp(from_number, intents[intent])
        #msg.body("You will soon receive a WhatsApp message explaining the next steps to sponsor an elementary school child.")
    elif intent == 'sponsor high school child':
        send_whatsapp(from_number, intents[intent])
        #msg.body("You will soon receive a WhatsApp message explaining the next steps to sponsor a high school child.")
    else:
        msg.body(intents['greet'])

    return str(response)

# Voice bot endpoint
@app.route("/voice", methods=['POST'])
def voice():
    response = VoiceResponse()
    gather = Gather(numDigits=1, action="/gather", method="POST")
    gather.say("Thank you for calling Aspire and Glee. We're dedicated to creating brighter futures through education and providing essential clothing. How can we help you today?")
    gather.say("If you want to sponsor a child, press 1.")
    gather.say("If you want to support our infrastructure, press 2.")
    gather.say("If you want to donate used clothing, press 3.")
    gather.say("If you want to get connected to a volunteer, press 4.")
    response.append(gather)
    response.pause(length=5)
    response.say("If you want to repeat these options, press 9.")
    response.redirect("/gather")
    return str(response)

@app.route("/gather", methods=['POST'])
def gather():
    digits = request.form['Digits']
    response = VoiceResponse()

    if digits == '1':
        gather = Gather(numDigits=1, action="/handle-sponsor-choice", method="POST")
        gather.say("If you want to sponsor a kindergarten child, press 1.")
        gather.say("If you want to sponsor an elementary school child, press 2.")
        gather.say("If you want to sponsor a high school child, press 3.")
        gather.say("If you are not sure, please visit our website aspireandglee.com/donate-for-good.")
        response.append(gather)
        response.pause(length=5)
        response.say("If you want to repeat these options, press 9.")
        response.redirect("/handle-sponsor-choice")
    elif digits == '2':
        send_whatsapp(request.form['From'], "Thank you for supporting our infrastructure. Please visit aspireandglee.com/donate-for-school.")
        response.say("You will soon receive a WhatsApp message explaining the next steps. Thank you.")
    elif digits == '3':
        response.say("Please visit aspireandglee.com/donate-clothes for more information on donating used clothing. Thank you.")
    elif digits == '4':
        response.say("This feature will be implemented in the future. Thank you.")
    elif digits == '9':
        response.redirect("/voice")
    else:
        response.say("Sorry, I don't understand that choice.")
        response.redirect("/voice")

    return str(response)

@app.route("/handle-sponsor-choice", methods=['POST'])
def handle_sponsor_choice():
    digits = request.form['Digits']
    response = VoiceResponse()

    if digits == '1':
        send_whatsapp(request.form['From'], "Thank for showing your interest in us,Please visit http://localhost:3000/eduparent/Donor/donateAmount. for next steps")
        response.say("You will soon receive a WhatsApp message explaining the next steps. Thank you.")
    elif digits == '2':
        send_whatsapp(request.form['From'], "Thank for showing your interest in us,Please visit http://localhost:3000/eduparent/Donor/donateAmount. for next steps")
        response.say("You will soon receive a WhatsApp message explaining the next steps. Thank you.")
    elif digits == '3':
        send_whatsapp(request.form['From'], "Thank for showing your interest in us,Please visit http://localhost:3000/eduparent/Donor/donateAmount. for next steps")
        response.say("You will soon receive a WhatsApp message explaining the next steps. Thank you.")
    elif digits == '9':
        response.redirect("/voice")
    else:
        response.say("Sorry, I don't understand that choice.")
        response.redirect("/voice")

    return str(response)

if __name__ == "__main__":
    app.run(debug=True, port=6000)
