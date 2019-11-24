import time
from telethon import TelegramClient, sync, events
from telethon.tl.functions.messages import GetHistoryRequest, GetBotCallbackAnswerRequest
from telethon.errors import SessionPasswordNeededError
from bs4 import BeautifulSoup
from time import sleep
import requests, json, re, sys, os
import colorama
from colorama import Fore, Back, Style


colorama.init(autoreset=True)
hijau = Style.RESET_ALL+Style.BRIGHT+Fore.GREEN
hijau2 = Style.NORMAL+Fore.GREEN
putih = Style.RESET_ALL
abu = Style.DIM+Fore.WHITE
ungu = Style.RESET_ALL+Style.BRIGHT+Fore.MAGENTA
ungu2 = Style.NORMAL+Fore.MAGENTA
yellow = Style.RESET_ALL+Style.BRIGHT+Fore.YELLOW
yellow2 = Style.NORMAL+Fore.YELLOW
red = Style.RESET_ALL+Style.BRIGHT+Fore.RED
red2 = Style.NORMAL+Fore.RED

if not os.path.exists('session'):
    os.makedirs('session')

nomer_hp = list()
num = input("Masukkan jumlah nomer HP yang anda inginkan : ")
print ('Masukkan Nomer HP : ')
for i in range(int(num)):
    n = input("No : ")
    nomer_hp.append(str(n))
print ('Nomer HP Anda: ',nomer_hp)
angka=0
for ulangpertama in range(int(num)):
    api_id = 1121458
    api_hash = '546ffed83f4c5a9c89a42f2e88f13d74'
    phone_number = nomer_hp[angka]

    client = TelegramClient('session/'+phone_number,api_id,api_hash)
    client.connect()
    if not client.is_user_authorized():
        try:
            client.send_code_request(phone_number)
            me = client.sign_in(phone_number,input('{}Masukan Code Anda {}>>{} '.format(hijau,abu,putih)))
        except SessionPasswordNeededError:
            password = input('{}Masukan Password 2fa Anda {}>>{} '.format(hijau,abu,putih))
            me = client.start(phone_number,password)

    myself = client.get_me()
    print(putih,'Selamat Datang @',myself.username)
    channel_username = '@Litecoin_click_bot'
    c = requests.session()
    ua = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'}

    channel_entity = client.get_entity(channel_username)
    try:
        for ulang in range(999999999):
            sys.stdout.write('\r                                                        \r')
            sys.stdout.write('\r{}Mencoba Mengambil URL'.format(yellow2))
            client.send_message(entity=channel_entity,message='🖥 Visit sites')
            sleep(3)
            message_history = client(GetHistoryRequest(peer=channel_entity,limit=1,offset_date=None,offset_id=0,max_id=0,min_id=0,add_offset=0,hash=0))
            channel_id = message_history.messages[0].id
            if message_history.messages[0].message.find('Sorry, there are no new ads available.') != -1:
                sys.stdout.write('\r                                                     \r')
                sys.stdout.write('\r{}Iklan Sudah Habis Silahkan Coba Lagi Nanti\n'.format(red2))

                t=17
                def countdown(t):
                    while t:
                        mins, secs = divmod(t, 10)
                        timeformat = '{:02d}:{:02d}'.format(mins, secs)
                        print(timeformat, end='\r')
                        time.sleep(1)
                        t -= 1
                sleep(3)
                angka = angka + 1
                break
            url = message_history.messages[0].reply_markup.rows[0].buttons[0].url
            sys.stdout.write('\r                                                     \r')
            sys.stdout.write('\r{}Visit To URL {}'.format(yellow2,putih)+url)

            r = c.get(url,headers=ua)
            soup = BeautifulSoup(r.text,"html.parser")

            if soup.find('div',class_='g-recaptcha') is None and soup.find('div',id='headbar') is None:
                sleep(2)
                message_history = client(GetHistoryRequest(peer=channel_entity,limit=1,offset_date=None,offset_id=0,max_id=0,min_id=0,add_offset=0,hash=0))
                message = message_history.messages[0].message
                sys.stdout.write('\r                                                     \r')
                sys.stdout.write('\r'+yellow+message)
                if message_history.messages[0].message.find('Please stay on') != -1 or message_history.messages[0].message.find('You must stay') != -1:
                    timer = re.findall(r'([\d.]*\d+)',message)
                    sleep(int(timer[0]))
                    sleep(3)
                    message_history = client(GetHistoryRequest(peer=channel_entity, limit=1, offset_date=None, offset_id=0, max_id=0, min_id=0,add_offset=0, hash=0))
                    sys.stdout.write('\r                                                     \r')
                    sys.stdout.write('\r{}'.format(hijau)+message_history.messages[0].message+'\n')

            elif soup.find('div',id='headbar') is not None:
                for data in soup.find_all('div',class_='container-fluid'):
                    code = data.get('data-code')
                    timer = data.get('data-timer')
                    token = data.get('data-token')
                    sleep(int(timer))
                    sleep(2)
                    r = c.post('https://dogeclick.com/reward',data={'code': code, 'token': token},headers=ua)
                    jsn = json.loads(r.text)
                    sys.stdout.write('\r                                                     \r')
                    sys.stdout.write(hijau+"\rYou earned "+jsn['reward']+" Litecoin for visiting sites\n")
            else:
                sys.stdout.write('\r                                                     \r')
                sys.stdout.write(red+'\rCaptcha detected')
                sleep(2)
                client(GetBotCallbackAnswerRequest(channel_username,channel_id,data=message_history.messages[0].reply_markup.rows[1].buttons[1].data))
                sys.stdout.write('\r                                                     \r')
                print (red+'\rBerhasil Skip Captcha\n')

    except:
        print(red+"ERROr Detected")
        sys.exit()