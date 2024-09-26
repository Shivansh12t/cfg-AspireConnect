# Aspire Connect - Twilio Bot Integration

Aspire Connect is a communication and engagement platform designed to assist social initiatives such as Aspire and Glee Society in automating and streamlining communication. The platform integrates with **Twilio's WhatsApp** and **Voice services**, enabling users to interact with Aspire Connect via WhatsApp messages or voice calls. This bot assists users in sponsoring children, donating clothing, supporting infrastructure, and volunteering.

## Features
- **WhatsApp Bot**: Responds to user queries and sends predefined messages based on intents (e.g., sponsoring a child, donating).
- **Voice Bot**: Provides an interactive voice menu allowing users to navigate through options like sponsoring children, supporting infrastructure, and donating clothes.
- **Intelligent Intent Matching**: Uses natural language processing to determine user intent based on their input.
- **Automated Responses**: Automatically sends follow-up messages with details about sponsoring or donating via WhatsApp.

---

## Project Structure
- **Twilio Integration**: Handles WhatsApp and voice calls via Twilio’s API.
- **NLP for Intent Matching**: Uses TF-IDF vectorization and cosine similarity to understand user messages and provide appropriate responses.
- **WhatsApp Messaging**: Automatically sends messages through WhatsApp for specific intents.
- **Voice Response System**: Users interact with voice prompts to get the desired information.

---

## Getting Started

### Prerequisites

Before you begin, ensure you have met the following requirements:

1. **Python 3.8+**: Ensure Python is installed. You can download it from [here](https://www.python.org/downloads/).
2. **Flask**: Flask is the web framework used to handle the server and routes. Install Flask using pip:
    ```bash
    pip install flask
    ```
3. **Twilio**: You’ll need a Twilio account and credentials for interacting with WhatsApp and voice services. Set up an account [here](https://www.twilio.com/).
4. **Ngrok**: Ngrok is used to expose your local Flask server to the internet for Twilio to send messages and voice requests to. You can install Ngrok via Chocolatey:
    ```bash
    choco install ngrok
    ```

### Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/AspireConnect.git
    cd AspireConnect
    ```

2. **Install Required Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure Twilio**:
    - Sign up for Twilio and create a project for WhatsApp and Voice.
    - Replace the placeholders in the code (`$yourssid`, `$yourapikey`, `+youtwillionumber`, `+youcallingnumber`) with your actual Twilio credentials.

4. **Run the Flask Server**:
    Start the Flask server:
    ```bash
    flask run --port 6000
    ```
    By default, Flask will start the server at `http://127.0.0.1:6000`.

5. **Expose Local Server via Ngrok**:
    Open a new terminal and start Ngrok to expose your Flask server to the internet:
    ```bash
    ngrok http 6000
    ```
    Ngrok will provide a public URL that you can use to configure Twilio Webhooks (for both WhatsApp and Voice).

6. **Configure Twilio Webhooks**:
    - Go to your Twilio console and configure the **Webhook URLs**:
        - For WhatsApp, use `http://<ngrok-url>/whatsapp`
        - For Voice, use `http://<ngrok-url>/voice`

### How it Works

- **WhatsApp Bot**:
    1. Users send a message via WhatsApp to the Twilio number.
    2. The message is processed by the Flask server, which determines the user's intent using natural language processing (NLP) techniques.
    3. The bot replies with a predefined response based on the detected intent (e.g., sponsorship options or donation info).
  
- **Voice Bot**:
    1. Users call the Twilio voice number.
    2. They hear a menu of options such as sponsoring children or donating clothes.
    3. The user can press digits corresponding to their choice, and the system will provide more details or send a WhatsApp message with the next steps.

---

## Intent Matching

The bot uses **TF-IDF vectorization** to match user input with predefined intents. The process involves:
1. **Text Preprocessing**: Lowercasing, removing punctuation, tokenizing words, and filtering stopwords.
2. **Cosine Similarity**: The user input is compared against predefined intents to determine the closest match.

### Supported Intents:
- **greet**: A welcome message.
- **sponsor child**: Offers sponsorship options for kindergarten, elementary, or high school children.
- **donate clothing**: Provides instructions for donating clothes.
- **support infrastructure**: Sends information on how to support Aspire & Glee's infrastructure.
- **volunteer**: Informs the user about future volunteer opportunities.

---

## Contribution Guidelines

If you'd like to contribute to this project, feel free to fork the repository and submit a pull request. Make sure to create issues for any feature requests or bug reports.

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---