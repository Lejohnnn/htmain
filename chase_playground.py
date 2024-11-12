# chase playground

import request

url = 'https://accounts.spotify.com/api/token'
headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}
data = {
    "grant_type": "client_credentials",
    "client_id": "81c4f515b6ae4a0aa0ea2ea75c460169", 
    "client_secret": "f59cb9f4164a40318678018c01dced42"
}

response = requests.post(url, headers=headers, data=data)

# Check if the request was successful
if response.status_code == 200:
    token_info = response.json()
    access_token = token_info.get("access_token")
    print("Access token:", access_token)
else:
    print("Failed to retrieve access token:", response.status_code, response.text)