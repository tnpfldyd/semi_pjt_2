import json, requests, os

url = "https://kauth.kakao.com/oauth/token"
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
}

data = {
    "grant_type": "refresh_token",
    "client_id": os.getenv("KAKAO_SECRET"),
    "refresh_token": "JE0TWb5mlX3SdRGSM29rpKObc4etwUh91HH0DnFnCinJYAAAAYRlCGyr",
}

response = requests.post(url, headers=headers, data=data)
print(response)
