import requests
import simplejson
import re
#CactusMC module
def auth(mojangAcc, mcPassword):
    global aToken
    global cToken
    r = requests.post('https://authserver.mojang.com', json={"key": "value"})
    r.status_code
    url = 'https://authserver.mojang.com/authenticate' # Set destination URL here
    data = {
    "username": mojangAcc,
    "password": mcPassword
    }
    data_json = simplejson.dumps(data)
    headers = {'Content-type': 'application/json'}
    payload = {'json_payload': data_json}
    r = requests.post(url, data_json, headers=headers)
    if str(r) == "<Response [200]>":
        aToken=re.search('{"accessToken":"(.*?)","clientToken":"', r.text).group(1)
        cToken=re.search('","clientToken":"(.*?)"}', r.text).group(1)
    else:
        print("Whoops, you either entered the wrong password or there's a bug!")
