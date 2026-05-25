team 11 - 단일 팩터 모델을 활용한 각 주식 섹터별(예: 반도체 섹터, 생필품 섹터 등) 기대 수익률, 변 동성, 샤프 비율을 예측하고 시각화
(팀원) 202642174 정한결, 202642132 박윤진, 202642161 이준서

프로젝트 소개 - 단일팩터 모델을 이용하여 주식 기사들을 통해 그 주식의 수익률과 변동성, 샤프 비율이 어떻게 되는지 예측해보는 것입니다. 
수집한 주식기사들을 사용하여 웹 크롤링, 정형 데이터 시각화 및 감정 분석 기법을 통해 실제 경제 데이터를 읽어보고 복잡한 주식 시장 현상을
이해해보고자 하는 프로젝트입니다. 

## 실행 방법

1. 가상환경 활성화 (Windows)
.venv\Scripts\activate

2. 가상환경 활성화 (macOS / Linux)
source .venv/bin/activate

3. 필수 라이브러리 설치
pip install streamlit requests beautifulsoup4 lxml pandas matplotlib

5. Streamlit 대시보드 구동
streamlit run app.py

사용라이브러리 
streamlit, requests, beautifulsoup4, lxml, pandas, matplotlib
