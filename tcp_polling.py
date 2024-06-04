 # /app/anaconda3/bin/python3 /N_DATA/service/tcp_socket/tcp_polling.py

import requests
import json
import datetime

polling_data = '\x02' +'0000008' + 'P' + '\x03'
# 요청할 메시지 데이터z
data = {
    "input_str":  polling_data
}

# /send_message 엔드포인트에 POST 요청 보내기
response = requests.post("http://localhost:3999/send_message", json=data)
received_time =datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
print(response.text)
# 응답 출력
if json.loads(response.text)['result'] == True:
    print(f'{received_time} : ok')
else:
    print(f'{received_time} : polling error')
