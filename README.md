# 현대차 출고 상황 알림판
내 차 출고가 현재 어떤 상태인지 5분 간격으로 업데이트하여 띄워줍니다.

## 스크린샷
![스크린샷](https://github.com/gimdh/hyundai_progress/blob/master/screenshot/sample.png?raw=true)


## 사용법
### 주의
> 기본적인 파이썬 지식이 있어야 합니다.

### 과정
0. 파이어폭스를 설치합니다.

1. `config_sample.json`을 `config.json`으로 복사하거나 이름을 바꿉니다.

2. `config.json`을 메모장으로 열어 `이메일 주소`와 `비밀 번호`를 지우고 본인의 현대 계정 이메일 주소와 비밀 번호를 입력합니다.

3. `pip install -r requirements.txt`로 필요한 패키지를 설치합니다. 다른 패키지 매니저를 사용할 경우 다음의 패키지를 설치합니다.
>* selenium-wire
>* PyQt5

4. `python main.py`로 실행합니다.


## 커스텀


### 다른 브라우저 사용
`webdriver.Firefox`와 `webdriver.FirefoxOptions`를 해당 브라우저용으로 고치고, `config.json`의 `driver_path`에 해당하는 드라이버 파일 경로를 추가하면 될겁니다... 아마도?


### 정보 추가 
`HyundaiProgress.info`에는 더 많은 계약 정보가 담겨있습니다. 원하는 정보를 추가해보세요. 차량 등급명과 색상명을 코드에 주석으로 남겨 두었으니 참고하세요.


## 모두의 빠른 출고를 기원합니다
<details><summary></summary>
<p>
현대야 내 차 좀 빨리 만들어줘라
</p>
</details>