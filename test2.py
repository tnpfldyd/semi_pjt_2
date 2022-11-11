import json, requests

url = "https://kapi.kakao.com/v1/user/unlink"

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": "Bearer " + "it1PZ1fo4tIxXDGRXC6L6wYob4SX0peFGchUlg3ICj10EQAAAYRkCNGb",
}

response = requests.post(url, headers=headers)
print(response)
