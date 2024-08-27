import requests
import base64

# Replace with your own Client ID and Client Secret
CLIENT_ID = '4a7a347e036e4033bcc2b91dea0e5acd'
CLIENT_SECRET = '951b39cc0660451cafce93ae18514096'

# Base64 encode the client ID and client secret
client_credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
client_credentials_base64 = base64.b64encode(client_credentials.encode())

# Request the access token
token_url = 'https://accounts.spotify.com/api/token'
headers = {
    'Authorization': f'Basic {client_credentials_base64.decode()}'
}
data = {
    'grant_type': 'client_credentials'
}
response = requests.post(token_url, data=data, headers=headers)

if response.status_code == 200:
    access_token = response.json()['access_token']
    print(access_token)
    print("Access token obtained successfully.")
else:
    print("Error obtaining access token.")
    exit()
