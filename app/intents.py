import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Predefined intents and responses
intents = {
    'greet': "Welcome to Aspire and Glee!",
    'sponsor child': "Do you want to sponsor a kindergarten, elementary, or high school child?",
    'sponsor kindergarten child': "You will soon receive a WhatsApp message explaining the next steps to sponsor a kindergarten child. Please visit http://localhost:3000/eduparent/Donor/donateAmount.",
    'sponsor elementary school child': "You will soon receive a WhatsApp message explaining the next steps to sponsor an elementary school child. Please visit http://localhost:3000/eduparent/Donor/donateAmount.",
    'sponsor high school child': "You will soon receive a WhatsApp message explaining the next steps to sponsor a high school child. Please visit http://localhost:3000/eduparent/Donor/donateAmount.",
    'support infrastructure': "You will soon receive a WhatsApp message explaining the next steps to support our infrastructure. Please visit aspireandglee.com/donate-for-school.",
    'donate clothing': "Please visit aspireandglee.com/donate-clothes for more information on donating used clothing. Thank you.",
    'volunteer': "This feature will be implemented in the future. Thank you.",
}

# Preprocess text input
def preprocess_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stopwords.words('english')]
    return ' '.join(tokens)

# Get intent based on user input
def get_intent(user_input):
    user_input = preprocess_text(user_input)
    corpus = list(intents.keys()) + [user_input]
    vectorizer = TfidfVectorizer().fit_transform(corpus)
    vectors = vectorizer.toarray()
    cosine_similarities = cosine_similarity(vectors[-1].reshape(1, -1), vectors[:-1])
    best_match = cosine_similarities.argmax()
    return list(intents.keys())[best_match]
