import json, requests, os

url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

# 사용자 토큰
headers = {"Authorization": "Bearer " + "it1PZ1fo4tIxXDGRXC6L6wYob4SX0peFGchUlg3ICj10EQAAAYRkCNGb"}


data = {
    "template_object": json.dumps(
        {"object_type": "text", "text": "메세지요", "link": {"web_url": "www.naver.com"}}
    )
}

response = requests.post(url, headers=headers, data=data)
print(response)
print(response.status_code)
if response.json().get("result_code") == 0:
    print("메시지를 성공적으로 보냈습니다.")
else:
    print("메시지를 성공적으로 보내지 못했습니다. 오류메시지 : " + str(response.json()))
