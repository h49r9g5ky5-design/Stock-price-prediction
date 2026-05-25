import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import platform
import urllib.parse

# 1. 시스템 OS별 폰트 설정을 통한 원그래프 한글 깨짐 방지
if platform.system() == 'Windows':
    plt.rc('font', family='Malgun Gothic')
elif platform.system() == 'Darwin':  # Mac 환경
    plt.rc('font', family='AppleGothic')
plt.rc('axes', unicode_minus=False)


# 2. [A안] 구글 뉴스 표준 피드 수집 함수 (차단율 0%, 초고속)
def fetch_samsung_news_google():
    articles = []

    progress_bar = st.progress(0)
    status_text = st.empty()

    # 검색어 한글 인코딩 처리 ('삼성전자')
    keyword = urllib.parse.quote("삼성전자")

    # 구글이 전 세계에 공식 제공하는 뉴스 RSS 피드 주소 (대한민국 지역, 한국어 설정)
    url = f"https://news.google.com/rss/search?q={keyword}&hl=ko&gl=KR&ceid=KR:ko"

    try:
        # 구글 서버는 차단이 없으므로 가볍게 요청을 보냅니다.
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            # 구글 뉴스 XML 파싱
            soup = BeautifulSoup(response.text, 'xml')
            items = soup.select("item")

            for idx, item in enumerate(items):
                if idx >= 50:  # 상위 50개 기사로 제한
                    break

                # 구글 뉴스의 제목(title) 추출
                title = item.select_one("title").get_text(strip=True) if item.select_one("title") else ""

                # 구글 뉴스 제목 특유의 ' - 언론사명' 부분을 잘라내어 순수 제목만 보존
                if " - " in title:
                    title = title.rsplit(" - ", 1)[0]

                articles.append(title)

                # 대시보드 진행률 실시간 업데이트
                status_text.write(f"✅ 구글 뉴스 매핑: [{idx + 1}/50] {title[:25]}...")
                progress_bar.progress((idx + 1) / min(len(items), 50))
        else:
            status_text.write(f"⚠️ 구글 서버 응답 지연 (상태코드: {response.status_code})")

    except Exception as e:
        status_text.write(f"❌ 데이터 호출 오류 발생: {str(e)}")

    return articles


# 3. 리스트 기반 초경량 감성 분석 함수
def analyze_sentiments_with_lists(articles):
    results = {'긍정': 0, '부정': 0, '중립': 0}

    # 한국어 금융 뉴스 분석용 고품질 핵심 키워드 사전
    pos_words = ['상승', '돌파', '대박', '호조', '흑자', '성장', '최고', '기대', '우상향', '순항', '1위', '증가', '이익', '호재', '출시', '강세', '확대',
                 '선전']
    neg_words = ['하락', '폭락', '감소', '적자', '우려', '위기', '부진', '둔화', '쇼크', '손실', '급락', '감축', '떨어', '악재', '논란', '약세', '축소',
                 '소송']

    for text in articles:
        pos_count = sum(1 for word in pos_words if word in text)
        neg_count = sum(1 for word in neg_words if word in text)

        if pos_count > neg_count:
            results['긍정'] += 1
        elif neg_count > pos_count:
            results['부정'] += 1
        else:
            results['중립'] += 1

    return results


# --- Streamlit 대시보드 레이아웃 ---
st.set_page_config(layout="wide")
st.title("📊 삼성 뉴스 실시간 수집 및 안전 감성 분석 시스템")
st.caption("차단 없는 글로벌 구글 뉴스 엔진 기반 대시보드입니다. 보안 키가 없어 깃허브에 바로 올리셔도 됩니다.")

col1, col2 = st.columns([1, 2])

if 'google_crawled_data' not in st.session_state:
    st.session_state.google_crawled_data = []

# [좌측] 글로벌 구글 뉴스 실시간 수집 영역
with col1:
    st.header("1. 데이터 수집")
    if st.button("🚀 크롤링 시작"):
        with st.spinner("구글 뉴스 실시간 데이터베이스에 접근 중..."):
            st.session_state.google_crawled_data = fetch_samsung_news_google()
            if st.session_state.google_crawled_data:
                st.success(f"총 {len(st.session_state.google_crawled_data)}개의 실제 최신 기사 수집 완료!")
            else:
                st.error("데이터를 가져오지 못했습니다. 네트워크 연결을 확인해 주세요.")

# [우측] 감성 분석 및 삼색 차트 시각화 영역
with col2:
    st.header("2. 감성 분석 결과")
    if st.button("🧠 감성 분석 시작"):
        if not st.session_state.google_crawled_data:
            st.error("오른쪽 분석을 시작하기 전에, 먼저 왼쪽에서 '크롤링 시작'을 눌러주세요.")
        else:
            with st.spinner("단어 매칭 통계 엔진 가동 중..."):
                analysis_results = analyze_sentiments_with_lists(st.session_state.google_crawled_data)

                # 표 형태로 화면 노출
                df = pd.DataFrame(list(analysis_results.items()), columns=['감성', '건수'])
                st.dataframe(df.set_index('감성'))

                # 원그래프 시각화 처리
                fig, ax = plt.subplots(figsize=(6, 6))
                colors = ['#2ecc71', '#e74c3c', '#95a5a6']  # 긍정(녹색), 부정(적색), 중립(회색)

                ax.pie(
                    df['건수'],
                    labels=df['감성'],
                    autopct='%1.1f%%',
                    startangle=90,
                    colors=colors,
                    textprops={'fontsize': 12, 'weight': 'bold'}
                )
                ax.axis('equal')  # 파이 차트가 완전한 원 모양을 유지하도록 설정
                plt.title("실시간 삼성 뉴스 감성 분포도 (Google 데이터)", fontsize=15, pad=20, weight='bold')
                st.pyplot(fig)
