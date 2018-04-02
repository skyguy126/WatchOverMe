from twilio.rest import Client

def send_sms(account_sid, api_key, from_num, to_nums, message):
    client = Client(account_sid, api_key)
    for num in to_nums:
        client.api.account.messages.create(to=num, from_=from_num, body=message)
