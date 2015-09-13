import requests
import json

customerId = '55f4762a35e65015006ceed7'
apiKey = 'e409c6159fcf5ed6f1f32aa87344fa29'

responseAction = {
	201 : lambda : print('It worked'),
	400 : lambda : print('Uh oh, something in your payload is wrong'),
}

def move_money(account_id_payer, account_id_payee, amount_to_pay):
    make_house_url = 'http://api.reimaginebanking.com/accounts/' + account_id_payer + '/transfers?key=e409c6159fcf5ed6f1f32aa87344fa29'.format(customerId,apiKey)
    payload = {
          "medium": "balance",
          "payee_id": account_id_payee,
          "amount": amount_to_pay,
          "transaction_date": "string",
          "status": "pending",
          "description": "string"
    }
    req = requests.post(make_house_url, data=json.dumps(payload),headers={'content-type':'application/json'})
## as a proof of concept, the following payee and payer account ID info is used. SmartShower will assemble the account ID's with timeline data.
## payer account ID: 55f4791e35e65015006ceee9
## payee account ID: 55f57f6535e65015006d5a75







