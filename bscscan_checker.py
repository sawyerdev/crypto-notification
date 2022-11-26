import os, requests, json, smtplib, ssl
from time import sleep
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Requester:
    def __init__(self, token_contract, wallet_address, api_key):
        self.token_contract = token_contract
        self.wallet_address = wallet_address
        self.api_key = api_key

    def request_api(self):
        request = requests.get("https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress={}&address={}&tag=latest&apikey={}".format(
            self.token_contract, self.wallet_address, self.api_key))

        req_text = request.text
        data = json.loads(req_text)

        small_token = float(data['result'])
        token_amount = small_token / (10 ** 18)
        return token_amount

class TheProgram:
    def __init__(self):
        self.amount = []
        self.amount_received = 0
        
    #Using Microsoft Outlook as example
    def send_mail(self):
        load_dotenv()
        msg = MIMEMultipart()
        msg['From'] = os.getenv("FROM_EMAIL")
        password = os.getenv("PASSWORD")
        msg['To'] = os.getenv("TO_EMAIL")
        msg['Subject'] = 'USDT RECEIVED!'
        message_content = f'ACCOUNT PAYMENT HAS BEEN SUCESSFULLY DEPOSITED!\n\nAMOUNT RECEIVED: ${self.amount_received}!'

        msg.attach(MIMEText(message_content, 'plain'))

        server = smtplib.SMTP('smtp.office365.com: 587')
        server.starttls()
        
        try:
            server.login(msg['From'], password)
            server.sendmail(msg['From'], msg['To'], msg.as_string())
        except Exception as err:
            print(err)
            
    def match_values(self, now, last):
        if now == last:
            return "No new transactions..."
        if now > last:
            self.amount_received = now - last
            print('\n======== READY TO SEND EMAIL AFTER NEW VALUE ALERT! ========\n')
            self.send_mail()
            self.amount.clear()

    def main(self):
        print('\n==== STARTING PROGRAM =====\n')
        while True:
            now_value = do_request.request_api()
            if len(self.amount) >= 2:
                last_value = self.amount[-1]
                res = self.match_values(now_value, last_value)
                print(res)
                if len(self.amount) >= 100:
                    self.amount.clear()
                    continue
            else:
                print(f"Total USDT: ${now_value}")

            self.amount.append(now_value)
            sleep(1800) #checking every 30 minutes

#Using USDT contract as example
do_request = Requester("0x55d398326f99059ff775485246999027b3197955","WALLET_ADDRESS","BSCSCAN_API_KEY")
main = TheProgram()
main.main()
