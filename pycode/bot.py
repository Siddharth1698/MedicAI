"""from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals """

import os
from sys import argv
from wit import Wit
from flask import Flask, request
from pymessenger.bot import Bot

# Wit.ai parameters
WIT_TOKEN = "XMRYLMHN2EDYADESNE2FYRAOHAIF6BYQ"#os.environ.get('WIT_TOKEN')
# Messenger API parameters
FB_PAGE_TOKEN = "EAACyN8TSLV8BADVKBonN676lSt0r6JBzfWg0RcngUOxgwypV1A99Wx5Jw0htBH90RfqQcV6l9ZA9IbSEjwE8KQgZByZBegs86hDRglR7ZCC8PiLm5qPqNcEvvismK3LVomBvBqnSM3pS8k5FWZAeuKXlyueE3syA5Q3NAcgsa3dnuiCoiszyF"
# A user secret to verify webhook get request.
VERIFY_TOKEN = 'hello'

# Setup Bottle Server

app = Flask(__name__)
bot = Bot(FB_PAGE_TOKEN)


@app.route('/', methods=['GET'])
def varifyToken():
    token_sent = request.args.get("hub.verify_token")
    return verify_fb_token(token_sent)

def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


# Facebook Messenger POST Webhook
@app.route('/', methods=['POST'])
def messenger_post():
    output = request.get_json()
    for event in output['entry']:
        messaging = event['messaging']
        for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    response_sent_text = "hooooooo"
                    send_message(recipient_id, response_sent_text)
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    response_sent_text = "attachments hoo"
                    send_message(recipient_id, response_sent_text)
    return "Message Processed"


#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"



# Setup Wit Client
client = Wit(access_token=WIT_TOKEN)

if __name__ == '__main__':
    # Run Server
    app.run(port=5000)