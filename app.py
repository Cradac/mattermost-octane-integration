import settings, requests
from settings import wh_token as WEBHOOK_VERIFY_TOKEN, mm_webhook_url
from func import post_to_mattermost, format_message
from flask import Flask, request, abort, jsonify
from datetime import datetime, timedelta
import json

#Generate temp Token to secure the Webhook from intruders
def temp_token():
    import binascii, os
    temp_token = binascii.hexlify(os.urandom(24))
    return temp_token.decode('utf-8')

#Set default Flask Object
client = Flask(__name__)


@client.route('/webhook', methods=['POST'])
def webhook():
    #Post method  - Handle incoming Webhook Body
    if request.method == 'POST':
        #success, process posted data
        request_token = request.args.get('verify_token')
        if request_token is None:
            return jsonify({'status': 'not authorised'}), 401
        if request_token == WEBHOOK_VERIFY_TOKEN:
            message = format_message(request.json)
            if not message:
                return jsonify({'status': 'irrelevant update'}), 200
            post_to_mattermost(message, mm_webhook_url)
            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'status': 'bad token'}), 401

    #Abort if wrong method
    else:
        abort(400)


if __name__ == '__main__':
    if WEBHOOK_VERIFY_TOKEN is None:
        print('WEBHOOK_VERIFY_TOKEN has not been set in settings.py .\nGenerating random token...')
        token = temp_token()
        print(f'Token: {token}')
        WEBHOOK_VERIFY_TOKEN = token
    print('Example webhook adress: http://127.0.0.1:5000/webhook/?verify_token=TOKEN')
    client.run(host=settings.external_ip, port=settings.port)