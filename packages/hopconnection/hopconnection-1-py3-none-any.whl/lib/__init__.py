from lib.hello import checkconnection

if 'Ok' in checkconnection('http://ip-api.com/json'):
    print('Connection OK')
else:
    print('No internet connection')