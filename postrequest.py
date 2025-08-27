import requests
import base64

# Fitbit API Credentials
CLIENT_ID = 'client id'  # Replace with your actual Client ID
CLIENT_SECRET = 'actual id'  # Replace with your actual Client Secret
REDIRECT_URI = 'redirect url'  # Your Redirect URI
AUTHORIZATION_CODE = 'url'  # The code you got in the URL

# Token Request URL
TOKEN_URL = 'token url'

# Prepare the Basic Authorization header
credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
headers = {
    'Authorization': f'Basic {encoded_credentials}',
    'Content-Type': 'application/x-www-form-urlencoded',
}

# Prepare the data to send in the POST request
data = {
    'grant_type': 'authorization_code',
    'code': AUTHORIZATION_CODE,
    'redirect_uri': REDIRECT_URI
}

# Make the POST request to get the access and refresh tokens
response = requests.post(TOKEN_URL, data=data, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    tokens = response.json()
    access_token = tokens['access_token']
    refresh_token = tokens['refresh_token']
    
    print(f'Access Token: {access_token}')
    print(f'Refresh Token: {refresh_token}')
else:
    print(f"Error: {response.status_code}")
    print(f"Response: {response.json()}")
