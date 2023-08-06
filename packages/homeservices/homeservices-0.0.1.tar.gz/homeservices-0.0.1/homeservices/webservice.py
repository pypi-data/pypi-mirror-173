from flask import Flask, request, jsonify
from flask_compress import Compress

class PiWWWaterflowService:

    def __init__(self,  template_folder, static_folder):
        self.app = Flask(__name__,  template_folder=template_folder, static_folder=static_folder)
        self.app.add_url_rule('/', 'index', self.index, methods=['GET'])
        self.app.add_url_rule('/alexaintent', 'alexaintent', self.alexa_intent, methods=['GET'])
        Compress(self.app)

    def getApp(self):
        return self.app

    def run(self):
        self.app.run()

    def index(self):
        return 'This is the Pi server.'

    def alexa_intent(self):
        if request.method == 'GET':
            response_dict = {'outputSpeech': {"type": "SSML", "ssml": "<speak>Esto viene del servidor</speak>"}}

            response = jsonify(response_dict)
            response.headers['Pragma'] = 'no-cache'
            response.headers["Expires"] = 0
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            return response


