import requests
def check(url):
    try:
        requests.get(url).json()
        message = 'error'
        return message
    except:
        message = 'error'
        return message