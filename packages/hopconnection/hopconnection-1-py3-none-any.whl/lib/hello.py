import requests
def checkconnection(link):
    try:
        check = requests.get(link).text
        message = 'Ok'
        return message
    except:
        message = 'Cp'
        return message