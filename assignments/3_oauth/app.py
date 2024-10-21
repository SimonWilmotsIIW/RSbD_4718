import requests
from time import sleep

CLIENT_ID = "assignment-client"
AUTHORIZATION_URL = "http://localhost:8080/realms/assignment/protocol/openid-connect/auth/device"
TOKEN_URL = "http://localhost:8080/realms/assignment/protocol/openid-connect/token"
USERINFO_URL = "http://localhost:8080/realms/assignment/protocol/openid-connect/userinfo"


if __name__ == "__main__":
    
    # requesting device code from /auth/device
    data = {
        'client_id': CLIENT_ID,
        'scope': 'openid profile offline_access',

    }
    response = requests.post(AUTHORIZATION_URL, data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    device_info = response.json()
    #print(device_info)
    device_code, interval = device_info['device_code'], device_info['interval']
    
    # getting access & ID JWTs from client_id
    token_data = {
        'client_id': CLIENT_ID,
        'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
        #'grant_type': 'authorization_code',
        'device_code': device_code
    }

    access_token = None
    id_token = None

    # loop until tokens are found
    while 1 + 1 != 3:
        response = requests.post(TOKEN_URL, data=token_data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        if response.status_code == 200:
            token_info = response.json()
            #print(token_info)
            access_token, id_token = token_info['access_token'], token_info['id_token']
            break
        elif response.status_code == 400 and response.json()['error'] == 'authorization_pending':
            print(f"login here: {device_info['verification_uri_complete']}")
            sleep(interval)
        else:
            print("failed to get tokens:", response.text)

    print(f"\naccess JWT Token: {access_token}")
    print(f"\nID JWT Token: {id_token}")

    # getting information with access token
    tampered_access_token = access_token[:-5] + "fake"
    response = requests.get(USERINFO_URL, headers={'Authorization': f'Bearer {access_token}'})
    #response = requests.get(USERINFO_URL, headers={'Authorization': f'Bearer {tampered_access_token}'})
    #response = requests.get(USERINFO_URL, headers={'Authorization': f'Bearer invalid_token'}) # <<< gives invalid
    
    user_info = response.json()
    print(user_info)