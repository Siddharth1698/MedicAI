import os
from sys import argv
from wit import Wit
from flask import Flask, request
from pymessenger.bot import Bot 


# Wit.ai parameters
WIT_TOKEN = "-----"#os.environ.get('WIT_TOKEN')
# Messenger API parameters
FB_PAGE_TOKEN = "-----"
# A user secret to verify webhook get request.
VERIFY_TOKEN = '-----'

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
                    msg = message['message'].get('text')
                    response_sent_text = handle_message(msg)
                    print(response_sent_text)
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


def first_entity_value(entities, entity):
    if entity not in entities:
        return None
    val = entities[entity][0] # to get the second entity
    if not val:
        return None
    return val



def first_trait_value(traits, trait):
    if trait not in traits:
        return None
    val = traits[trait][0]['value']
    if not val:
        return None
    return val


    
def handle_message(msg):
    resp = client.message(msg)
    print(resp)
    print("-------------------------------------")
    traits = resp['traits']
    greetings = first_trait_value(traits, 'wit$greetings')
    medic_purchase = first_entity_value(resp['entities'], 'medic_purchase:medic_purchase')
    stores_list = first_entity_value(resp['entities'],'stores_list:stores_list')
    address_list = first_entity_value(resp['entities'], 'address_list:address_list')
    medical_products = first_entity_value(resp['entities'], 'Medical_products:Medical_products')
    mode_pay = first_entity_value(resp['entities'], 'mode_pay:mode_pay')
    medic_condition = first_entity_value(resp['entities'],'medical-condition:medical-condition')
    COVID19 = first_entity_value(resp['entities'], 'COVID19:COVID19')
    chickenpox = first_entity_value(resp['entities'], 'chicken_pox:chickenpox')
    symptoms = first_entity_value(resp['entities'], 'symotoms_list:symotoms_list')

    if medic_purchase:
        return 'Enter the name of the store Where would you prefer to order from \n Enter \n \t 1) store A \n \t 2) store b \n \t 3) store c '
    elif greetings:
        return ' Hey ! How do you like to have MedicAI support ? \n 1) Enter purchase to purchase medical items \n 2) Enter check health condition to know your health condition'
    elif stores_list:
        return 'Where do you want your kit to be delivered ? \n Enter \n \t 1) Address1 to deliver to address1 \n \t 2) address2 to deliver it to address2'
    elif medical_products:
        return 'please enter the payment method \n Enter \n \t 1) wallet \n \t 2) Credit card \n \t 3) Debit card'    
    elif address_list:
        return 'enter the items you want to buy and also select the no of items you want to purchase \n Enter the option like this \n \t Eg:- band aid - 1'
    elif mode_pay:
        return 'Thanks for making the payment'

    elif medic_condition:
        return 'Please start typing the medical symptom which you are currently experiencingt to know whether you have \n 1) COVID19 \n 2) Chickenpox'
    elif COVID19:
        return 'You are having COVID19 symptoms'    
    elif chickenpox:
        return "You have chickenpox symptoms"  
    elif symptoms:
        return "Please consult nearby doctor near you"                          
    else:
        return "sorry. i did'nt understant what you have said"

# Setup Wit Client
client = Wit(access_token=WIT_TOKEN)

if __name__ == '__main__':
    # Run Server
    app.run(port=5000)