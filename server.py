from flask import Flask,request, jsonify
from whatsapp import *
import json


app = Flask(__name__)


@app.route('/', methods=['POST'])
def home():
    if request.method == 'POST':
        bot = Wa(request.json)
        bot.processing()
        return "200 OK"

@app.route('/hi/')
def hi():
    return "hello abhishek"

if(__name__) == '__main__':
    app.run()
