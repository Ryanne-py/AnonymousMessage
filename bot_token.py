import os

def get_token():
    return os.environ['BOT_TOKEN']

def get_payment_token():
    return os.environ['PAYMANT_TOKEN']
