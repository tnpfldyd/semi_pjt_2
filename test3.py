import json, requests, os

url = "https://kauth.kakao.com/oauth/token"

data = {
    "grant_type": "refresh_token",
    "client_id": "7e02c2ba46031deb86bc9cd7d6e507f3",
    "refresh_token": "9y1A_gNs2DHMDxpAGOBFQ8rnflEdnKkDgV6oFVz-Cilw0QAAAYRlN9MP",
    "client_secret": "ovM5S70qOwngB09GUY2etQgYPTccX8ub",
}

response = requests.post(url, data=data).json()
print(os.getenv("KAKAO_ID"))
print(response)
