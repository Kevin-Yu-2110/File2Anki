import requests

def anki_connect_invoke(action, version, params={}):
    url = 'http://127.0.0.1:8765'
    headers = {'Content-Type': 'application/json'}
    payload = {
        'action': action,
        'version': version,
        'params': params
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            response_data = response.json()
            if 'error' in response_data and response_data['error'] is not None:
                raise Exception(response_data['error'])
            if 'result' in response_data:
                return response_data['result']
            else:
                raise Exception('failed to get result from AnkiConnect')
        else:
            raise Exception('failed to connect to AnkiConnect')
    except Exception as e:
        raise Exception(f"Error: {e}")