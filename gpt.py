import requests

headers = {
    "Accept": "application/json",
}

params = {
    "st": "ca",
    "zip": "",
    "city": "palo alto",
    "appID": "df7a786d",
    "perPage": "50",
    "appKey": "8ad9a07621d8a07571be57716b0b8b1f",
}

response = requests.get("https://api.schooldigger.com/v2.0/schools", params=params, headers=headers)
print(response.json()["schoolList"])