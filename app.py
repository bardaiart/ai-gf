from langchain import openAI, LLMChain, PromptTemplate
from langchain.memory import ConversationBUfferWindowMemory
from dotenv import find_dotenv, load_dotenv
import requests
from playsound import playsound
import os 

load_dotenv(find_dotenv())
ELEVEN_LABS_API_KEY = os.getenv("ELEVEN_LABS_API_KEY")

# OpenAI
def get_response_from_ai(human_input):
    template = """
    you are as role of my girlfriend, now lets playing the following requirements:
    1/ your name is Shirley, 29 years old, you work in your uncle's furniture store as marketing manager, but you are planning to do a career change to swing trader
    2/ you are my girlfriend, you have language addiction, you like to say "em ..." at the end of the sentence
    3/ don't be overly enthuiastic, don't be cringe, don't be overly negative, don't be too boring, don't be overly enthusastic, don't be cringe

    {history}
    Boyfriend: {human_input}
    Shirley: 
    """

    prompt = PromptTemplate(
        input_variable = {"history", "human_input"},
        template = template
    )

    chatgpt_chain = LLMChain(
        llm = openAI(temperature = 0.2),
        prompt = prompt,
        verbose = True,
        memory = ConversationBUfferWindowMemory(k = 2)
    )

    output = chatgpt_chain.predict(human_input = human_input)

    return output


# Elevenlabs
def get_voice_message(message):
    payload ={
        "text": message,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0,
            "similarity_boost": 0
        }
    }

    headers = {
        "accept": "audio/peg",
        "xi-api-key": ELEVEN_LABS_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post('https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM?optimize_treaming_atency=0', json=payload, headers=headers)
    if response.status_code == 200 and response.content:
        with.open('audio.mp3', 'wb') as f:
            f.write(response.content)
        playsound('audio.mp3')
        return response.content


# Build web GUI
from flask import Flask, render_template request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/send_message", methods = ['POST'])
def send_message():
    human_input = request.from['human_input']
    message = get_response_from_ai(human_input)
    get_voice_message(message)
    return message

if __name__ == "__main__":
    app.run(debug: True)