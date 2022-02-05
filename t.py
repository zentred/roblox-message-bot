import requests, ctypes, threading
req = requests.Session()

message = 'message you want to send here'
cookie = 'cookie here'
req.cookies['.ROBLOSECURITY'] = cookie

proxies = open('proxies.txt','r').read().splitlines()
proxies = [{'https':'http://'+proxy} for proxy in proxies]

info = req.get('https://www.roblox.com/mobileapi/userinfo').json()
username = info['UserName']
userid = info['UserID']

sent = 0
failed = 0
scraped = 0

def title():
    while True:
        ctypes.windll.kernel32.SetConsoleTitleW(f'Users Scraped: {scraped} | Messages Sent: {sent} | Messages Not Sent: {failed}')

def conversations():
    global scraped
    lst = []
    while True:
        try:
            r = req.get(f'https://chat.roblox.com/v2/get-user-conversations?pageNumber=1&pageSize=100', proxies=random.choice(proxies), timeout=4).json()
            if 'participants' in str(r):
                for x in r:
                    lst.append(x['id'])
                    scraped += 1
                if len(r) == 100:
                    while True:
                        try:
                            c = req.get(f'https://chat.roblox.com/v2/get-user-conversations?pageNumber=2&pageSize=100', proxies=random.choice(proxies), timeout=4).json()
                            if 'participants' in str(c):
                                for x in c:
                                    lst.append(x['id'])
                                    scraped += 1
                            elif 'is not available':
                                continue
                            else:
                                time.sleep(3)
                                continue
                        except:
                            continue
                        else:
                            break
            elif 'is not available' in str(c):
                continue
            else:
                time.sleep(3)
                continue
        except:
            continue
        else:
            send(lst)
            break

def token():
    csrf = req.post('https://auth.roblox.com/v1/logout').headers['X-CSRF-TOKEN']
    return csrf

def send(lst):
    global sent, failed
    for cid in lst:
        while True:
            try:
                csrf = token()
                r = req.post('https://chat.roblox.com/v2/send-message', json={"conversationId":int(cid),"message":message}, headers={'X-CSRF-TOKEN': csrf}, proxies=random.choice(proxies), timeout=4)
                if 'resultType' in r.text:
                    if r.json()['resultType'] == 'Success':
                        sent += 1
                    else:
                        failed += 1
                elif 'is not available':
                    continue
                else:
                    break
            except:
                continue
            else:
                break

threading.Thread(target=title).start()
conversations()
