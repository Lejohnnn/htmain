import requests
from accessTkn import access_token

url = "https://api.spotify.com/v1/me"
headers = {
    "Authorization": "Bearer BQAdRysDK5gSnY6Oa893mDfygAYID-Y-Yoyhd9kXrRf6bZYAhcn_68iVaUo_M2RFHh6AewzAs6bT3e9YsALFNPk5pPxnoTi9OWyU95CtwwyG1i_cDzI"
}

response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    user_info = response.json()
    print("User Info:", user_info)
else:
    print("Failed to retrieve user info:", response.status_code, response.text)
