from requests import post
from json import dumps

def generate_key(randomorg_key: str):
    uri = "https://api.random.org/json-rpc/4/invoke"
    headers = {'content-type': 'application/json'}

    payload = {
        "jsonrpc": "2.0",
        "method": "generateIntegerSequences",
        "params": {
            "apiKey": randomorg_key,
            "n": 4,
            "length": [16, 1, 1, 1],
            "min": [0, 1, 1, 1],
            "max": [255, 2, 4, 2],
            "base": [16, 16, 16, 16]
        },
        "id": 45673
    }

    response = post(uri, data=dumps(payload), headers=headers).json()
    
    key = response["result"]["random"]['data'][0]
    algorithm = response["result"]["random"]['data'][1]
    x_operation = response["result"]["random"]['data'][2]
    y_operation = response["result"]["random"]['data'][3]
    
    result = ""
    for i in key:
        result += i
    result += f"0{algorithm[0]}"
    result += f"0{x_operation[0]}"
    result += f"0{y_operation[0]}"
    
    return result