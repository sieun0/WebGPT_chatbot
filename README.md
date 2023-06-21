# MOA Chatbot (모아챗봇)

이 프로젝트는 사용자의 입력을 받아오고 gpt의 응답을 이용하여 '홈쇼핑모아' 사이트에 대한 대화 시스템 챗봇을 구현하는 것을 목표로 합니다. 아래는 프로젝트에 대한 상세한 설명과 실행 방법을 안내합니다.


## System Architecture

![moachatbot (1)](https://github.com/sieun0/WebGPT_chatbot/assets/85726398/cc365f2b-e94c-4ac4-9427-ab48858ad1fa)



## 주요 기능

1. 원하는 가격대 상품 검색 : 사용자가 입력한 메시지에 따라 원하는 가격대의 상품을 출력한다.
2. 리뷰 요약 : 원하는 상품을 선택하면 리뷰를 요약해주는 기능을 제공합니다.


## 설치

이 프로젝트를 실행하기 위해서는 다음과 같은 단계를 따라야 합니다.

1. 저장소를 클론(clone)합니다.
2. npm을 이용하여 플라스크를 설치합니다.
3. .env 파일을 만들어 openai에서 발급받은 api키를 저장합니다.
4. 터미널에 "FLASK_APP=main.py flask run" 명령어를 입력하여 챗봇을 실행합니다.


## 라이선스

이 프로젝트는 MIT 라이선스에 따라 배포됩니다. 자세한 내용은 'LICENSE'파일을 참조하세요.


## 시연 영상 캡쳐

![image](https://github.com/sieun0/WebGPT_chatbot/assets/85726398/e3a4edb9-c5b5-4c2a-a3c8-ebbb654c5149)

