import requests, os, uuid, json
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, redirect, url_for, request, render_template, session

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def index_post():

    # read values from the form
    original_text = request.form['text']
    target_language = request.form['language']

    # loading .env values
    key = os.environ['KEY']
    endpoint = os.environ['ENDPOINT']
    location = os.environ['LOCATION']

    # API version
    path = '/translate?api-version=3.0'
    #target language param
    target_language_parameter = '&to=' + target_language
    # full URL
    constructed_url = endpoint + path + target_language_parameter

    # header info
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # request body
    body = [{ 'text': original_text }]

    # call
    translator_request = requests.post(constructed_url, headers=headers, json=body)
    # json response
    translator_response = translator_request.json()
    # retrieved translation
    translated_text = translator_response[0]['translations'][0]['text']

    return render_template(
        'results.html',
        translated_text=translated_text,
        original_text=original_text,
        target_language=target_language
    )
