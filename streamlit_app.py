import streamlit as st
from title_extractor import extract_title
from transcriber import transcribe_video
from translator import translate_script
from docx_creator import create_docx
import os
from datetime import datetime
from io import BytesIO
from dotenv import load_dotenv


# 웹페이지 설정
st.set_page_config(
    page_title="유튜브 스크립트 변환기",
    page_icon="🎬",
    layout="centered"
)

load_dotenv()

# API 키 설정
# os.environ['YOUTUBE_API_KEY'] = st.secrets.get('YOUTUBE_API_KEY', os.getenv('YOUTUBE_API_KEY'))
# os.environ['GEMINI_API_KEY'] = st.secrets.get('GEMINI_API_KEY', os.getenv('GEMINI_API_KEY'))

# API 키 설정 (로컬)
os.environ['YOUTUBE_API_KEY'] = os.getenv('YOUTUBE_API_KEY')
os.environ['GEMINI_API_KEY'] = os.getenv('GEMINI_API_KEY')


st.title("🎬 유튜브 영상 → Word 변환기")
st.divider()

# 본문
tab1, tab2 = st.tabs(['🎬 영상 링크로 스크립트 및 번역 작성', '📝 스크립트 번역'])

with tab1:
    # st.header("YouTube 영상 스크립트 추출 및 번역")
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
                    file_name = f"{datetime.now().strftime('%Y%m%d')}_{title}.docx"
                    doc = create_docx(title, script, translation, video_url)
                
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

with tab2:
    # st.header("스크립트 번역")
    script = st.text_area("여기에 스크립트를 붙여넣으세요:", placeholder="请输入视频的脚本。")
    if st.button("번역", type="primary"):
        if not script:
            st.warning("스크립트를 먼저 입력해주세요!")
        else:
            with st.spinner("스크립트를 번역하는 중..."):
                translation = translate_script(script)
                if not translation:
                    st.error("번역에 실패했습니다.")
                    st.stop()
                
                st.success("번역 완료!")
                
                # 번역 결과 출력
                st.write('번역 결과:\n')
                # container = st.container(border=True)
                # container.write(translation)
                
                st.code(translation)

                