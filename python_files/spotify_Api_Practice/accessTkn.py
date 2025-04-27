# spotify playground


# grant auth code ---
import requests
import urllib.parse

client_id = "81c4f515b6ae4a0aa0ea2ea75c460169" 
redirect_uri = "http://localhost:3000"  
scopes = "user-read-private user-read-email"   # Scopes needed for accessing user info

auth_url = (
    "https://accounts.spotify.com/authorize?"
    + urllib.parse.urlencode({
        "response_type": "code",
        "client_id": client_id,
        "scope": scopes,
        "redirect_uri": redirect_uri,
    })
)

print("Go to the following URL to authorize:", auth_url)




# grant access token --- 

auth_code = "AQA1xbvm-ZXYbkXsseE8_OgCVQyRN1ipjWU5t9mgN1cXvZATmAkZ7uz8t_2alfB1Avwstt3mpauGDmrI09xtbts6_yL3N_r3IoEh2zLT7V9bOIVJvnLysoZpmwHdJLMixYyvw4Pkap-lbvV3jDO2F02Rb7_YaGiR0OVXmKDZO6pmcHNAi2Ic8XaYYjlgYmI8uQXPKulqbXGjF2TrJg"

url = 'https://accounts.spotify.com/api/token'
headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}
data = {
    "grant_type": "authorization_code",
    "code": auth_code,
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
