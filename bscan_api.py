import requests, json, datetime, sys
import win32com.client as win32
from time import sleep

class RequestBscscan():
    
    def __init__(self, usdt_contract, wallet_address, api_key):
        self.usdt_contract = usdt_contract
        self.wallet_address = input(str('Digite a carteira da METAMASK: '))
        self.api_key = api_key

    def json_load(self):
        d = open('#PATH/FILE WITH INFORMATIONS: username (optional) and metamask wallet to verification')
        self.dt = json.load(d)
        return self.dt
    
    def requestApi(self):
        request = requests.get("https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress={}&address={}&tag=latest&apikey={}".format(
            self.usdt_contract, self.wallet_address, self.api_key))

        req_text = request.text
        self.data = json.loads(req_text)
    
    def getTokenAmount(self):
        small_token = float(self.data['result'])
        self.token_amount = small_token/1000000000000000000
        return self.token_amount

request = RequestBscscan("0x55d398326f99059ff775485246999027b3197955","","API_KEY")

def setOutlookInstance():
    global mailItem
    olApp = win32.Dispatch('Outlook.Application')
    olNS = olApp.GetNameSpace('MAPI')
    mailItem = olApp.CreateItem(0)

def sendMail():
    dt = request.json_load()
    for i in dt['account']:
        if request.wallet_address == i['metamask_wallet']:
            username = i['username']
   
    mailItem.Subject = 'USDT RECEIVED!'
    mailItem.BodyFormat = 1
    mailItem.Body = f'{username} ACCOUNT PAYMENT HAS BEEN SUCCESSFULLY DEPOSITED!\n\nAMOUNT RECEIVED: ${amount_received} USDT'
    mailItem.To = '' #email to send

    try:
        mailItem.Send()
        print('Email successfully sent!\n')
        sleep(3)
    except Exception as err:
        print(err)
    
def matchValues(now, last):
    global amount_received
    if now == last:
        return "No amount received yet..."
    elif now > last:
        amount_received = now - last
        print('\n======== READY TO SEND EMAIL AFTER NEW VALUE ALERT! ========\n')
        sendMail()
        amount.clear()
    
def main():
    setOutlookInstance()
    global amount
    amount = []
    print('\n==== STARTING PROGRAM =====\n')
    while True:
        request.requestApi()
        now_value = request.getTokenAmount()
        if len(amount) >= 2:
            last_value = amount[-1]
            res = matchValues(now_value, last_value)
            print(res)
            if len(amount) >= 100:
                amount.clear()
        else:
            print(f"Total USDT: ${now_value}")

        amount.append(now_value)
        sleep(1800)

main()
