from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE

from title_extractor import extract_title
from transcriber import transcribe_video
from translator import translate_script
from docx_creator import create_docx
import os

def main():
    print("=" * 60)
    print("유튜브 영상 → Word 변환기")
    print("=" * 60)

    # 유튜브 링크 입력받기
    video_url = input("유튜브 링크를 입력하세요: ").strip()
    
    if not video_url:
        print("링크를 입력해주세요.")
        return
    
    print("\n처리를 시작합니다...")
    print("-" * 40)

    try:
        # 1. 제목 추출
        print("1. 영상 제목 추출 중...")
        title = extract_title(video_url)
        if title:
            print(f"   제목: {title}")
        else:
            print("   제목 추출 실패")
            return
        
        # 2. 스크립트 추출
        print("\n2. 영상 스크립트 추출 중...")
        print("   (시간이 오래 걸릴 수 있습니다...)")
        script = transcribe_video(video_url)
        if script:
            print("   스크립트 추출 완료")
        else:
            print("   스크립트 추출 실패")
            return
        
        # 3. 번역
        print("\n3. 스크립트 번역 중...")
        translation = translate_script(script)
        if translation:
            print("   번역 완료")
        else:
            print("   번역 실패")
            return
        
        # 4. 워드 파일 생성
        print("\n4. Word 파일 생성 중...")
        
        output_filename = create_docx(title, script, translation)
        
        print(f"\n✅ 완료! Word 파일이 생성되었습니다")
        
    except KeyboardInterrupt:
        print("\n\n사용자에 의해 중단되었습니다.")
    
    # except Exception as e:
        # print(f"\n오류가 발생했습니다: {e}")
        # print("API 키가 올바르게 설정되어 있는지 확인해주세요.")

if __name__ == "__main__":
    main() 