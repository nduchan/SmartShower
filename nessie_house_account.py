import requests
import json

customerId = '55f4762a35e65015006ceed7'
apiKey = 'e409c6159fcf5ed6f1f32aa87344fa29'

responseAction = {
	201 : lambda : print('It worked'),
	400 : lambda : print('Uh oh, something in your payload is wrong'),
}

def make_house_account():
    make_house_url = 'http://api.reimaginebanking.com/customers/55f4762a35e65015006ceed7/accounts?key=e409c6159fcf5ed6f1f32aa87344fa29'.format(customerId,apiKey)
    payload = {
          "type": "Savings",
          "nickname": "SmartShower",
          "rewards": 0,
          "balance": 100
    }
    req = requests.post(make_house_url, data=json.dumps(payload),headers={'content-type':'application/json'})

make_house_account()







