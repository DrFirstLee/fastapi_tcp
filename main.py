## uvicorn main:app --reload --host localhost --port 3999
####### HTS와 송수신을 위한 데이터 가공함수 ############################
import tcp_func
######################################################################

####### 필요 상용패키지  #############################################
import asyncio
import socket
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import datetime
import time
from pydantic import BaseModel
######################################################################

####### 필요 세팅들!!  #############################################
app = FastAPI()

# 클라이언트 연결 정보 저장
connected_clients = []
loop = None
client_socket = None
# 메시지 데이터 모델
class Message(BaseModel):
    input_str: str
######################################################################        
        
        
# 메시지 전송 API 엔드포인트
@app.post("/send_message")
async def send_message(message: Message):
    global loop
    sending_data = message.input_str
    received_time =datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    chk_validity =  tcp_func.check_sendingData_validity(sending_data)
    ## 보내는 데이터가 HTS 요청 양식 데이터가 아니면 에러!!
    if chk_validity['result']==False:
        print(f"Error details : {chk_validity['result_detail']}, {received_time}")
        return {'result':'Error',"result_detail": chk_validity['result_detail']}   
    ## 보내는 데이터가 HTS 요청 양식에 맞으면 인코딩해서 보낸다!!    
    sending_data_encoded = sending_data.encode('euc-kr')
    print(f"send data : {sending_data_encoded} target length : {len(connected_clients)}")
    for client in connected_clients:
        if client.fileno() == -1:
            print("소켓이 닫혔습니다.")
            connected_clients.remove(client)
            continue
        client.sendall(sending_data_encoded)
        
        ## 보내고 난 다음 정상 받았는지 확인하자!
        data = await loop.sock_recv(client_socket, 1024)
        if not data:
            print('data????')
            break
        message = data.decode('euc-kr')
        print(f"클라이언트로부터 받은 메시지: {message}")
        ## 클라이언트가 보낸 데이터가 무엇인지 체그!! 경우의수는 ACK 이거나 에러거나!!
        received_data_chk = tcp_func.check_ack(message)
        ## ACK가 이상할때
        if  received_data_chk['result'] == False:
            received_time =datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
            print(f"Error details : {received_data_chk['result_detail']}, {received_time}")
            return {'result':False, "result_detail": f"ACK data error, {received_time}"}
        ## ACK가 맞을떄
        else :
            ## 데이터 잘받았어!! 로그 찍고!!! 보내는거는, 나중에 api를 통해서 보낼수 있도록 대기상태!
            print(f"send data : {message}, data length : {len(message)} // {received_time}")
            return {'result':True, "result_detail": f"ACK data success, {received_time}"}
        
    

# TCP 서버 실행 (비동기)
async def run_tcp_server():
#     HOST = '0.0.0.0'  # 서버 IP 주소
#     PORT = 9900  # 서버 포트 번호
    HOST = 'localhost'
    PORT = 8010
    ## faspapi가 실행되면서 자동으로 소켓 연결!!!
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    server_socket.setblocking(False)  # Non-blocking 설정
    print(f"TCP 서버가 {HOST}:{PORT}에서 실행 중입니다.")
    while True:
        ## 이후 연결될때마다 다 연결해줌!!!
#         loop = asyncio.get_event_loop()
        try:
            global client_socket
            client_socket, addr = await loop.sock_accept(server_socket)
            print(f"클라이언트 {addr}가 연결되었습니다.")
            connected_clients.append(client_socket)
            loop.create_task(handle_client(client_socket,loop, connected_clients))
        except BlockingIOError:
            await asyncio.sleep(0.1)  # 짧은 시간 대기

# 클라이언트 처리 (비동기)
async def handle_client(client_socket,loop,connected_clients):
    while True:
        try:
            data = await loop.sock_recv(client_socket, 1024)
            if not data:
                break
            message = data.decode('euc-kr')
            print(f"클라이언트로부터 받은 메시지: {message}")
            ## 클라이언트가 보낸 데이터가 무엇인지 체그!! 경우의수는 ACK 이거나 에러거나!!
            received_data_chk = tcp_func.check_ack(message)
            ## ACK가 이상할때
            if  received_data_chk['result'] == False:
                received_time =datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
                print(f"Error details : {received_data_chk['result_detail']}, {received_time}")
            ## ACK가 맞을떄
            else :
                ## 데이터 잘받았어!! 로그 찍고!!! 보내는거는, 나중에 api를 통해서 보낼수 있도록 대기상태!
                print(f"send data : {message} // target length : {len(connected_clients)}")
                

        except (ConnectionResetError, BrokenPipeError):
            break
    client_socket.close()

# FastAPI 시작 시 TCP 서버 실행
@app.on_event("startup")
async def startup():
    global loop
    loop = asyncio.get_event_loop()
    asyncio.create_task(run_tcp_server())

# FastAPI 종료 시 TCP 서버 종료
@app.on_event("shutdown")
async def shutdown():
    print("서버가 종료되었습니다.")
