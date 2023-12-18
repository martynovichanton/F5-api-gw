from flask import Flask, render_template
from flask import json
import requests
import getpass
from Crypto import Crypto
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)
crypto = Crypto()
token = crypto.encrypt_random_key(getpass.getpass('token '))

@app.route('/')
def index():
    global token
    headers = crypto.encrypt_random_key(json.dumps({
            'Content-Type': "application/json",
            'token': crypto.decrypt_random_key(token),
            'cache-control': "no-cache"
    }))
    payload = ""
    dataset = requests.get("https://localhost:5000/f5api/vippoolstatsallfiltered", data=payload, headers=json.loads(crypto.decrypt_random_key(headers)), verify=False)
    return render_template('index.html', dataset=dataset.json())

if __name__ == '__main__':
    app.run(port=5001)
