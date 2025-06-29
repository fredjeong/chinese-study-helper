import streamlit as st
from title_extractor import extract_title
from transcriber import transcribe_video
from translator import translate_script
from docx_creator import create_docx
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


# --- 웹페이지 설정 ---
st.set_page_config(
    page_title="유튜브 스크립트 변환기",
    page_icon="🎬",
    layout="centered"
)

# --- API 키 설정 ---
# Streamlit 배포 시에는 'Secrets'를 사용해야 합니다. 
# st.secrets['YOUTUBE_API_KEY'] 와 st.secrets['GEMINI_API_KEY'] 처럼요.
# 이 부분은 배포 단계에서 자세히 설명합니다.
# 지금 당장 테스트할 때는 기존 .env 파일을 그대로 사용해도 됩니다.
# os.environ['YOUTUBE_API_KEY'] = st.secrets.get('YOUTUBE_API_KEY', os.getenv('YOUTUBE_API_KEY'))
# os.environ['GEMINI_API_KEY'] = st.secrets.get('GEMINI_API_KEY', os.getenv('GEMINI_API_KEY'))

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')


# --- 본문 ---
st.title("🎬 유튜브 영상 → Word 변환기")
st.divider()

# 유튜브 링크를 입력받는 부분
video_url = st.text_input("여기에 유튜브 영상 링크를 붙여넣으세요:", placeholder="https://www.youtube.com/watch?v=...")

# '변환 시작' 버튼을 누르면 아래 코드가 실행됩니다.
if st.button("Word 파일 만들기", type="primary"):
    if not video_url:
        st.warning("유튜브 링크를 먼저 입력해주세요!")
    else:
        try:
            # 처리 과정을 사용자에게 보여주기 위한 UI
            with st.spinner("영상 제목을 가져오는 중..."):
                title = extract_title(video_url)
                if not title:
                    st.error("영상 제목을 가져오는 데 실패했습니다. 링크를 확인해주세요.")
                    st.stop() # 오류 발생 시 중단
                st.success(f"제목: {title}")

            with st.spinner("영상 스크립트를 추출하는 중... (시간이 걸릴 수 있습니다)"):
                script = transcribe_video(video_url)
                if not script:
                    st.error("스크립트 추출에 실패했습니다.")
                    st.stop()
                st.success("스크립트 추출 완료!")

            with st.spinner("스크립트를 한국어로 번역하는 중..."):
                translation = translate_script(script)
                if not translation:
                    st.error("번역에 실패했습니다.")
                    st.stop()
                st.success("번역 완료!")

            with st.spinner("Word 파일을 생성하는 중..."):
                # Word 파일을 직접 저장하는 대신, 메모리에서 바로 생성합니다.
                # docx_creator.py를 약간 수정해야 합니다. 아래 설명 참조.
                # 임시로 파일 이름을 만들고, 내용을 메모리에 저장합니다.
                file_name = f"{datetime.now().strftime('%Y%m%d')}_{title}.docx"
                doc = create_docx(title, script, translation) # docx_creator가 Document 객체를 반환하도록 수정
                
                # 메모리에 있는 Word 파일 데이터를 임시로 저장
                from io import BytesIO
                file_stream = BytesIO()
                doc.save(file_stream)
                file_stream.seek(0) # 스트림의 시작으로 포인터를 이동

            st.success(f"✅ '{file_name}' 파일 생성 완료!")
            
            # 다운로드 버튼 생성
            st.download_button(
                label="Word 파일 다운로드",
                data=file_stream,
                file_name=file_name,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

        except Exception as e:
            st.error(f"처리 중 오류가 발생했습니다: {e}")
            st.info("API 키 설정이 올바른지, 유튜브 링크가 정확한지 확인해주세요.")