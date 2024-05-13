# FastAPI TCP 서버 & 웹소켓 클라이언트 연동 프로젝트

## 개요

본 프로젝트는 FastAPI를 사용하여 구현된 TCP 서버와 WebSocket 클라이언트 간의 실시간 통신을 지원합니다. TCP 서버는 타부서와의 통신을 담당하며, WebSocket 클라이언트는 웹 브라우저를 통해 서버에 접속하여 데이터를 실시간으로 받아볼 수 있도록 합니다.

## 주요 기능

**TCP 서버:**

*   TCP 연결을 안정적으로 설정하고 유지합니다.
*   데이터를 수신하고, 유효성을 검증합니다.
*   유효한 데이터를 WebSocket 클라이언트에게 실시간으로 전달합니다.

**WebSocket 클라이언트:**

*   웹 브라우저를 통해 서버에 WebSocket 연결을 설정합니다.
*   서버로부터 실시간으로 전달되는 데이터를 수신합니다.

**FastAPI API 엔드포인트:**

*   `/send_message` 엔드포인트를 통해 클라이언트 메시지를 전송합니다.
*   전송된 메시지의 유효성을 검사하고, 결과를 반환합니다. 
    *   **성공:** \`{result:True, "result_detail": f"ACK data success, {received_time}"}`\`
    *   **실패:** \`{result:False, "result_detail": f"ACK data error, {received_time}"}`\`
    *   **요청 양식 오류:** \`{result:'Error',"result_detail": chk_validity['result_detail']}`\`

## 기술 스택

*   **FastAPI:** Python 기반의 고성능 웹 프레임워크
*   **WebSockets:** 실시간 양방향 통신 프로토콜
*   **asyncio:** Python의 비동기 I/O 처리 라이브러리
*   **Pydantic:** Python 데이터 모델 정의 및 검증 라이브러리
*   **TCP 소켓:** 네트워크 통신을 위한 저수준 프로토콜

## 설치 및 실행

1.  필요한 패키지를 설치합니다.

    ```bash
    pip install fastapi uvicorn pydantic websockets
    ```

2.  `main.py` 파일을 실행합니다.

    ```bash
    uvicorn main:app --reload --host localhost --port 3999
    ```

3.  웹 브라우저에서 `http://localhost:3999/docs`에 접속하여 API 문서를 확인하고 테스트합니다.

## 코드 구조

*   `main.py`: FastAPI 애플리케이션, TCP 서버, WebSocket 엔드포인트, API 엔드포인트 구현
*   `tcp_func.py`: 데이터 처리 함수 (별도 파일)

## 추가 설명

*   `connected_clients` 리스트: 연결된 WebSocket 클라이언트들을 관리합니다.
*   `loop`: 비동기 이벤트 루프를 저장하는 변수입니다.
*   `client_socket`: TCP 연결을 위한 소켓 객체를 저장하는 변수입니다.
*   `Message` 모델: API 요청 데이터의 형식을 정의합니다.

## 주의 사항

*   실제 통신을 위해서는 `tcp_func.py` 파일을 적절하게 구현해야 합니다.
*   본 예시 코드는 기본적인 기능만을 구현하고 있으며, 실제 서비스 환경에 맞게 수정 및 보완이 필요할 수 있습니다.
