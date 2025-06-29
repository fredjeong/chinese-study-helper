# YouTube 영상 → PDF 변환기

유튜브 영상의 제목, 스크립트, 번역본을 자동으로 추출하여 PDF 파일로 생성하는 도구입니다.

## 기능

- 🎬 유튜브 영상 제목 자동 추출
- 📝 영상 스크립트 자동 추출 (Gemini AI 활용)
- 🌐 스크립트 한국어 번역 (Gemini AI 활용)
- 📄 모든 내용을 하나의 PDF 파일로 생성

## 설치 방법

### 1. 저장소 클론
```bash
git clone <repository-url>
cd gemini-cli
```

### 2. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 또는
venv\Scripts\activate  # Windows
```

### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

### 4. 환경 변수 설정
`.env` 파일을 생성하고 다음 내용을 추가하세요:

```env
GEMINI_API_KEY=your_gemini_api_key_here
YOUTUBE_API_KEY=your_youtube_api_key_here
```

#### API 키 발급 방법

**Gemini API 키:**
1. [Google AI Studio](https://makersuite.google.com/app/apikey)에 접속
2. API 키 생성
3. 생성된 키를 `GEMINI_API_KEY`에 설정

**YouTube API 키:**
1. [Google Cloud Console](https://console.cloud.google.com/)에 접속
2. 새 프로젝트 생성 또는 기존 프로젝트 선택
3. YouTube Data API v3 활성화
4. 사용자 인증 정보에서 API 키 생성
5. 생성된 키를 `YOUTUBE_API_KEY`에 설정

## 사용 방법

### 기본 사용법
```bash
python youtube_to_pdf.py
```

프로그램을 실행하면:
1. 유튜브 링크 입력 프롬프트가 나타납니다
2. 링크를 입력하면 자동으로 처리됩니다:
   - 영상 제목 추출
   - 스크립트 추출 (시간이 오래 걸릴 수 있음)
   - 한국어 번역
   - PDF 파일 생성

### 지원하는 URL 형식
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/watch?v=VIDEO_ID`

### 출력 파일
- 파일명: `제목_YYYYMMDD_HHMMSS.pdf`
- 위치: 현재 작업 디렉토리

## 파일 구조

```
gemini-cli/
├── youtube_to_pdf.py      # 메인 프로그램
├── title_extractor.py     # 제목 추출 모듈
├── transcriber.py         # 스크립트 추출 모듈
├── translator.py          # 번역 모듈
├── requirements.txt       # 의존성 목록
├── .env                   # 환경 변수 (사용자 생성)
└── README.md             # 이 파일
```

## 개별 모듈 사용

각 모듈은 독립적으로도 사용할 수 있습니다:

### 제목 추출
```python
from title_extractor import extract_title
title = extract_title("https://youtu.be/VIDEO_ID")
print(title)
```

### 스크립트 추출
```python
from transcriber import transcribe_video
script = transcribe_video("https://youtu.be/VIDEO_ID")
print(script)
```

### 번역
```python
from translator import translate_script
translation = translate_script("번역할 텍스트")
print(translation)
```

## 주의사항

- Gemini API와 YouTube API의 사용량 제한이 있을 수 있습니다
- 긴 영상의 경우 스크립트 추출에 시간이 오래 걸릴 수 있습니다
- API 키는 안전하게 보관하고 공개하지 마세요
- `.env` 파일은 `.gitignore`에 추가하여 버전 관리에서 제외하세요

## 문제 해결

### API 키 오류
- `.env` 파일이 올바른 위치에 있는지 확인
- API 키가 정확히 입력되었는지 확인
- API 키의 권한이 올바르게 설정되었는지 확인

### 스크립트 추출 실패
- 영상이 공개되어 있는지 확인
- 영상에 음성이 포함되어 있는지 확인
- Gemini API 할당량을 확인

### 번역 실패
- 입력 텍스트가 올바른 형식인지 확인
- Gemini API 할당량을 확인

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.
